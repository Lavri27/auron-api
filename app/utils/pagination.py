from sqlalchemy.orm import Query


def paginate(query: Query, limit: int = 20, offset: int = 0):
    total = query.count()
    items = query.limit(limit).offset(offset).all()
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": items,
    }
