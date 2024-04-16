from datetime import datetime, timedelta, timezone

now_utc = datetime.now(timezone.utc)
now_unix = now_utc.timestamp()
expire_utc = datetime.now(timezone.utc) + timedelta(minutes=15)
expire_unix = expire_utc.timestamp()
