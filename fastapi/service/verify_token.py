from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

import jwt
import logging
from dotenv import load_dotenv, find_dotenv
import os
from schema import Payload

load_dotenv(find_dotenv())

SECRET_KEY = os.getenv("SECRET_KEY")

security = HTTPBearer()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler('app.log')]
)
logger = logging.getLogger(__name__)

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Payload:
    """Verify jwt token

    Args:
        credentials: JWT token based on Authorization Bearer

    Exception:
        HTTPException: http_error_401 if token expired
        HTTPException: http_error_403 if invalid token

    Returns:
        dict: decode payload, field: ["iss", "sub", "iat", "exp"]
    """
    try:
        token = credentials.credentials
        decode_payload = jwt.decode(token, SECRET_KEY, ["HS256"])
        logger.info(f"Token valid: {decode_payload}")
        return Payload(**decode_payload)
    except jwt.ExpiredSignatureError as e:
        logger.error(f"Token expired {e}")
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError as e:
        logger.error(f"Invalid token {e}")
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Invalid token")