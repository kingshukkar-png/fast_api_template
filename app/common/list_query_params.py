from pydantic import BaseModel, Field
from enum import Enum
from typing import TypeVar, Generic

T = TypeVar("T")

class SortOrder(str, Enum):
    ASCENDING = "asc"
    DESCENDING = "desc"

class ListQueryParamsSchema(BaseModel):
    page: int = Field(1, ge=1)
    page_size: int = Field(10, ge=1)
    search: str | None = Field(None)
    sort_by: str = Field("created_at")
    sort_order: SortOrder = Field(SortOrder.ASCENDING)

    def skip(self) -> int:
        return (self.page - 1) * self.page_size

    def limit(self) -> int:
        return self.page_size
        

class PaginatedResponseSchema(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_previous: bool

    @classmethod
    def build_response(cls, items: list[T], total: int, params: ListQueryParamsSchema) -> PaginatedResponseSchema[T]:
        total_pages = max(1, -(-total // params.page_size))
        return cls(
            items=items,
            total=total,
            page=params.page,
            page_size=params.page_size,
            total_pages=total_pages,
            has_next=params.page < total_pages,
            has_previous=params.page > 1
        )