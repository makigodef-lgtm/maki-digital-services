"""Monthly USD billing for one server with durable, private SQLite storage."""
import calendar
import sqlite3
from contextlib import contextmanager
from datetime import UTC, datetime, timedelta
from typing import Protocol

PRICES = {"supplier": 5000, "buyer": 10000}  # USD cents
TERMS = "monthly-usd-14d-v1"


def stamp(dt):
    if dt.tzinfo is None:
        raise ValueError("Timezone required")
    return dt.astimezone(UTC).replace(microsecond=0).isoformat()


def anniversary(first, month):
    year, offset = divmod(first.year * 12 + first.month - 1 + month, 12)
    day = min(first.day, calendar.monthrange(year, offset + 1)[1])
    return first.replace(year=year, month=offset + 1, day=day)


class Gateway(Protocol):
    def charge(self, *, mandate, cents, currency, key) -> tuple[str, str]:
        """Return ('confirmed', bank reference), ('declined', reason), or ('pending', reference).
        Repeated keys must retrieve the original result without a second charge.
        Confirmation must come from the authenticated provider and match the order.
        """
        ...

    def lookup(self, key) -> tuple[str, str]:
        """Read an existing attempt without initiating a charge; unknown => pending."""
        ...


def connect(path):
    db = sqlite3.connect(path, isolation_level=None, timeout=30)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys=ON")
    db.executescript("""
        CREATE TABLE IF NOT EXISTS subscription (
            company TEXT PRIMARY KEY, plan TEXT NOT NULL, mandate TEXT UNIQUE NOT NULL,
            evidence TEXT NOT NULL, terms TEXT NOT NULL, accepted TEXT NOT NULL,
            first_due TEXT NOT NULL, due TEXT NOT NULL, period INTEGER NOT NULL DEFAULT 0,
            stopped TEXT
        );
        CREATE TABLE IF NOT EXISTS attempt (
            company TEXT NOT NULL REFERENCES subscription(company), period INTEGER NOT NULL,
            key TEXT NOT NULL UNIQUE, cents INTEGER NOT NULL, state TEXT NOT NULL,
            reference TEXT, PRIMARY KEY(company,period)
        );
    """)
    return db


@contextmanager
def write(db):
    db.execute("BEGIN IMMEDIATE")
    try:
        yield
        db.commit()
    except BaseException:
        db.rollback()
        raise


def enroll(db, company, plan, mandate, evidence, accepted, first_due, terms):
    """Trusted callback only. The bank adapter must verify mandate, company, terms,
    amount, currency and first_due against the offer explicitly accepted at checkout.
    Existing free trials must never be converted by this function without a new mandate.
    """
    if plan not in PRICES or terms != TERMS or not all((company, mandate, evidence)):
        raise ValueError("Incomplete billing agreement")
    if stamp(first_due) != stamp(accepted + timedelta(days=14)):
        raise ValueError("Incorrect trial expiry")
    values = (company, plan, mandate, evidence, terms, stamp(accepted), stamp(first_due))
    with write(db):
        old = db.execute("SELECT company,plan,mandate,evidence,terms,accepted,first_due FROM subscription WHERE company=?", (company,)).fetchone()
        if old:
            if tuple(old) != values:
                raise ValueError("Existing agreement differs")
            return
        db.execute("INSERT INTO subscription(company,plan,mandate,evidence,terms,accepted,first_due,due) VALUES(?,?,?,?,?,?,?,?)", (*values, stamp(first_due)))


def cancel(db, company, now):
    """Called only after verifying that the requester manages this company."""
    with write(db):
        db.execute("UPDATE subscription SET stopped=COALESCE(stopped,?) WHERE company=?", (stamp(now), company))


def process(db, gateway, now):
    current = stamp(now)
    rows = db.execute("""SELECT company FROM subscription s WHERE due<=?
        AND (stopped IS NULL OR EXISTS (SELECT 1 FROM attempt a WHERE a.company=s.company
        AND a.period=s.period AND a.state='pending'))""", (current,)).fetchall()
    for row in rows:
        company = row["company"]
        # Persist an attempt before contacting the bank so that a crash cannot lose its identity.
        with write(db):
            s = db.execute("SELECT * FROM subscription WHERE company=?", (company,)).fetchone()
            if s["due"] > current:
                continue
            key = f'mineralink:{company}:{s["period"]}'
            if not s["stopped"]:
                db.execute("INSERT OR IGNORE INTO attempt VALUES(?,?,?,?,?,NULL)",
                           (company, s["period"], key, PRICES[s["plan"]], "pending"))
        with write(db):
            # Serialize payment and cancellation for this small single-host worker.
            a = db.execute("SELECT * FROM attempt WHERE key=?", (key,)).fetchone()
            s = db.execute("SELECT * FROM subscription WHERE company=?", (company,)).fetchone()
            if not a or a["state"] != "pending" or a["period"] != s["period"]:
                continue
            try:
                if s["stopped"]:
                    state, reference = gateway.lookup(key)
                else:
                    state, reference = gateway.charge(mandate=s["mandate"], cents=a["cents"], currency="USD", key=key)
            except (TimeoutError, ConnectionError):
                continue
            if state not in {"declined", "pending", "confirmed"} or (state == "confirmed" and not reference):
                raise ValueError("Invalid gateway result")
            db.execute("UPDATE attempt SET state=?,reference=? WHERE key=?", (state, reference, key))
            if state == "declined":
                db.execute("UPDATE subscription SET stopped=COALESCE(stopped,?) WHERE company=?", (current, company))
            if state == "confirmed":
                first = datetime.fromisoformat(s["first_due"])
                period = s["period"] + 1
                while stamp(anniversary(first, period)) <= current:
                    period += 1  # do not collect a backlog after an outage
                db.execute("UPDATE subscription SET period=?,due=? WHERE company=?",
                           (period, stamp(anniversary(first, period)), company))
