""" import jwt
from fastapi import HTTPException, status

payload = {
                "sub": 12345, #userid
                "role": "user" #определиться с тем, храним ли тут роли, одна ли роль или несколько
            }

encoded = jwt.encode(payload, "private_key", "HS256")

#print(encoded)
#decoded = jwt.decode(encoded, "private_keys", "HS256")
#encoded = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjEyMzQ1LCJyb2xlIjoidXNlciJ9.8fd213OF0NVsSSF0qMH1QIvzH6D7SL21WAui6m6YW3k"
encoded = b"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjEyMzQ1LCJyb2xlIjoidXNlciJ9.8fd213OF0NVsSSF0qMH1QIvzH6D7SL21WAui6m6YW3k"
try:
    decoded = jwt.decode(encoded, "private_key", "HS256")
except jwt.exceptions.DecodeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
except jwt.exceptions.InvalidAlgorithmError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token algorithm"
        )
except jwt.exceptions.InvalidSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token signature"
        )
print(decoded) """
""" from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
print() """

from datetime import datetime, timedelta


#print(datetime.now())
#print(datetime.now(timezone.utc))
print(datetime.timestamp(datetime.now()))
print(datetime.timestamp(datetime.now() + timedelta(minutes=15)))

""" if datetime.now(timezone.utc) > datetime.strptime('19:08:34.885792',):
    print("!!") """