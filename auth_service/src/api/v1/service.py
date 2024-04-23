from fastapi import status, HTTPException, Request
from pydantic_core import ValidationError
from api.v1.schemas.auth import (
    TokenParams,
)


def get_tokens_from_cookie(request: Request) -> TokenParams.access_token:
    try:
        token = TokenParams(
            access_token=request.cookies.get("access_token"),
            refresh_token=request.cookies.get("refresh_token"),
        )
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tokens is not found"
        )
    return token
