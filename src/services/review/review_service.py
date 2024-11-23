from dataclasses import dataclass

from core.exceptions import BadRequestException
from core.uow import IUnitOfWork
from repositories.base import AlreadyExistsError
from schemas.pagination import PaginationResponse
from schemas.review import ReviewCreateRequest, ReviewResponse, ReviewCreateResponse, ReviewParams


@dataclass(frozen=True, slots=True)
class ReviewService:
    uow: IUnitOfWork

    async def add_review(self, schema: ReviewCreateRequest, user_id: int) -> ReviewCreateResponse:
        async with self.uow:
            try:
                review = await self.uow.review_repository.add_review(dict(**schema.model_dump(), user_id=user_id))
                return ReviewCreateResponse.model_validate(review, from_attributes=True)
            except AlreadyExistsError:
                raise BadRequestException

    async def get_reviews(self, params: ReviewParams) -> PaginationResponse[ReviewResponse]:
        async with self.uow:
            result = await self.uow.review_repository.get_reviews(**params.model_dump(exclude_none=True))
            return PaginationResponse[ReviewResponse].model_validate(result, from_attributes=True)

    async def delete_review(self, review_id: int, user_id: int) -> None:
        async with self.uow:
            review = await self.uow.review_repository.get_review_by_id(review_id=review_id)
            if not review or review.user_id != user_id:
                raise BadRequestException
            await self.uow.review_repository.delete_review(review_id=review_id, user_id=user_id)
