import unittest
from datetime import UTC, datetime, timedelta
from recurring import TERMS, cancel, connect, enroll, process


class TestBank:
    def __init__(self):
        self.charges = {}
        self.state = "confirmed"

    def charge(self, *, mandate, cents, currency, key):
        self.charges.setdefault(key, (mandate, cents, currency))
        return self.state, "test-reference"

    def lookup(self, key):
        return ("confirmed", "test-reference") if key in self.charges else ("pending", "")


class BillingTest(unittest.TestCase):
    def setUp(self):
        self.db = connect(":memory:")
        self.bank = TestBank()
        self.start = datetime(2027, 1, 17, 9, tzinfo=UTC)
        self.due = self.start + timedelta(days=14)

    def signup(self, plan="buyer"):
        enroll(self.db, "company", plan, "test-token", "test-consent-reference", self.start, self.due, TERMS)

    def test_trial_price_and_calendar(self):
        self.signup()
        self.signup()
        process(self.db, self.bank, self.due - timedelta(seconds=1))
        self.assertFalse(self.bank.charges)
        process(self.db, self.bank, self.due)
        process(self.db, self.bank, self.due)
        self.assertEqual(list(self.bank.charges.values()), [("test-token", 10000, "USD")])
        process(self.db, self.bank, datetime(2027, 2, 28, 9, tzinfo=UTC))
        self.assertTrue(self.db.execute("select due from subscription").fetchone()[0].startswith("2027-03-31"))

    def test_cancel_during_trial(self):
        self.signup()
        cancel(self.db, "company", self.start)
        process(self.db, self.bank, self.due)
        self.assertFalse(self.bank.charges)

    def test_pending_then_cancel(self):
        self.signup("supplier")
        self.bank.state = "pending"
        process(self.db, self.bank, self.due)
        cancel(self.db, "company", self.due)
        process(self.db, self.bank, self.due)
        self.assertEqual(list(self.bank.charges.values()), [("test-token", 5000, "USD")])
        self.assertEqual(self.db.execute("select state from attempt").fetchone()[0], "confirmed")

    def test_refusal(self):
        self.signup()
        self.bank.state = "declined"
        process(self.db, self.bank, self.due)
        self.assertIsNotNone(self.db.execute("select stopped from subscription").fetchone()[0])

    def test_missing_mandate(self):
        with self.assertRaises(ValueError):
            enroll(self.db,"company","buyer","","proof",self.start,self.due,TERMS)


if __name__ == "__main__":
    unittest.main()
