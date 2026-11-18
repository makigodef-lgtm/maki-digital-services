"""Run one scheduled billing pass. Requires the bank's installed production adapter."""
import os
from datetime import UTC, datetime
from pathlib import Path

from recurring import connect, process


def main():
    os.umask(0o077)
    path = Path(os.environ["MINERALINK_BILLING_DB"])
    if not path.is_absolute():
        raise SystemExit("Set an absolute private database path outside the website.")
    try:
        from mineralink_rawbank import merchant_gateway
    except ModuleNotFoundError as error:
        raise SystemExit("Rawbank merchant adapter unavailable; billing disabled.") from error
    gateway = merchant_gateway()
    db = connect(path)
    try:
        process(db, gateway, datetime.now(UTC))
    finally:
        db.close()


if __name__ == "__main__":
    main()
