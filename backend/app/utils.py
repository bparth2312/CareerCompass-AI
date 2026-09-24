from passlib.context import CryptContext
from passlib.exc import UnknownHashError


MAX_BCRYPT_PASSWORD_BYTES = 72


password_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12
)


def validate_password_length(password: str) -> None:
    """
    Validate the password before bcrypt hashing or verification.

    bcrypt supports a maximum of 72 bytes. A Unicode character
    can occupy more than one byte, so byte length must be checked.
    """

    if not isinstance(password, str):
        raise ValueError("Password must be a string.")

    if not password:
        raise ValueError("Password cannot be empty.")

    password_length = len(
        password.encode("utf-8")
    )

    if password_length > MAX_BCRYPT_PASSWORD_BYTES:
        raise ValueError(
            "Password is too long. "
            "It must not exceed 72 bytes."
        )


def hash_password(password: str) -> str:
    """
    Convert a plain-text password into a bcrypt hash.
    """

    validate_password_length(password)

    return password_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    """
    Compare a plain-text password with a stored bcrypt hash.
    """

    if not plain_password or not hashed_password:
        return False

    validate_password_length(plain_password)

    try:
        return password_context.verify(
            plain_password,
            hashed_password
        )
    except (
        ValueError,
        TypeError,
        UnknownHashError
    ):
        return False