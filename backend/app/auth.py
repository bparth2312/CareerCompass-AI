from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError, JWTError, jwt
from sqlalchemy.orm import Session

from app.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    SECRET_KEY
)
from app.database import get_db
from app.models import User


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login"
)


# Keep users logged in for at least 24 hours in this
# student project. A larger configured value is respected.
DEFAULT_TOKEN_EXPIRE_MINUTES = max(
    int(ACCESS_TOKEN_EXPIRE_MINUTES or 0),
    24 * 60
)


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None
) -> str:
    """Create a signed JWT access token."""

    to_encode = data.copy()

    now = datetime.now(timezone.utc)

    expire = (
        now + expires_delta
        if expires_delta is not None
        else now + timedelta(
            minutes=DEFAULT_TOKEN_EXPIRE_MINUTES
        )
    )

    to_encode.update(
        {
            "iat": now,
            "exp": expire
        }
    )

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Decode the Bearer token and return its user."""

    invalid_credentials = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication token. Please log in again.",
        headers={"WWW-Authenticate": "Bearer"}
    )

    expired_credentials = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Your login session has expired. Please log in again.",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")

        if not isinstance(email, str) or not email.strip():
            raise invalid_credentials

    except ExpiredSignatureError:
        raise expired_credentials

    except JWTError:
        raise invalid_credentials

    user = (
        db.query(User)
        .filter(User.email == email.strip())
        .first()
    )

    if user is None:
        raise invalid_credentials

    return user