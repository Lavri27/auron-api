from fastapi import Header, HTTPException


def require_api_key(x_api_key: str = Header(default=None)):
    if x_api_key != "secret-key":
        raise HTTPException(status_code=403, detail="Invalid API key")
