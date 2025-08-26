from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer
from jose import jwt, JWTError

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            try:
                payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
                request.state.user = payload
            except JWTError:
                raise HTTPException(status_code=403, detail="Invalid token")
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code")

jwt_bearer = JWTBearer()
