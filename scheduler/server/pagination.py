from typing import Any, List, Optional

from pydantic import BaseModel


class PaginatedResponse(BaseModel):
    count: int
    next: Optional[str]
    previous: Optional[str]
    results: List[Any]


def create_next_url(request, offset: int, limit: int, count: int) -> Optional[str]:
    if offset + limit <= count:
        return str(request.url.include_query_params(limit=limit, offset=offset + limit))

    return None


def create_previous_url(request, offset: int, limit: int) -> Optional[str]:
    if offset - limit >= 0:
        return str(request.url.include_query_params(limit=limit, offset=offset - limit))

    return None


def paginate(items: List[Any], count: int, offset: int, limit: int) -> PaginatedResponse:
    return PaginatedResponse(
        count=count,
        results=items,
    )
