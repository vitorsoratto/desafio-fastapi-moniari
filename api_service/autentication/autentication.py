from fastapi import Request, HTTPException, status, Header
from fastapi.security import HTTPBasic
import base64

# Basic authentication token: dXNlcjE6cGFzc3dvcmQ=
user_db = {
    "user1": {
        "username": "user1",
        "password": "password"
    },
}

security = HTTPBasic()


def authenticate(request: Request, authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Basic "):
        request.app.logger.error(f'401_UNAUTHORIZED / "Authorization header not found"')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Basic"},
        )

    try:
        credentials = base64.b64decode(authorization.split(" ")[1]).decode("utf-8")
        username, password = credentials.split(":")
    except Exception:
        request.app.logger.error(f'401_UNAUTHORIZED / "Invalid credentials"')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    user = user_db.get(username)

    if user is None or user["password"] != password:
        request.app.logger.error(f'401_UNAUTHORIZED / "username or password is incorrect"')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="username or password is incorrect",
            headers={"WWW-Authenticate": "Basic"},
        )

    return user
