from fastapi import HTTPException


def not_found(entity: str):
    raise HTTPException(404, f"{entity} not found")


def bad_request(msg: str):
    raise HTTPException(400, msg)


def forbidden():
    raise HTTPException(403, "Forbidden")
