import uuid

from fastapi import APIRouter, Depends, status, Path
from sqlalchemy.orm.session import Session
from loguru import logger

from app import controller
from app import schemas
from app.api import deps
from app.core.provider.previledge_checker import PreviledgeChecker
from app.models.user import User
from app.schemas.comment import CommentResponse
from app.schemas.common import CommonQueryParams, DataResponse

router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.CommentResponse)
def create_comment(*,
                   post_id: str,
                   db: Session = Depends(deps.get_db),
                   comment: schemas.CreateComment,
                   user: User = Depends(deps.get_current_user)):

    comment.user_id = user.id
    comment.post_id = uuid.UUID(post_id)
    new_comment = controller.comment.create(db, obj_in=comment)
    return new_comment


@router.get(
    '/', response_model=DataResponse[schemas.ListCommentResponse],
    status_code=status.HTTP_200_OK)
def get_comments(*,
                 post_id: str,
                 common: CommonQueryParams = Depends(),
                 db: Session = Depends(deps.get_db)):

    comments = controller.comment.get_multi_comments(db, post_id=post_id, skip=common.skip, limit=common.limit)
    data = DataResponse(success=True, data=schemas.ListCommentResponse(results=len(comments), comments=comments))
    return data


@router.get('/{comment_id}', response_model=CommentResponse, status_code=status.HTTP_200_OK)
def get_comment(*,
                comment_id: str,
                db: Session = Depends(deps.get_db)):

    comment = controller.comment.get(db, id=comment_id)
    return comment


@router.put('/{comment_id}', response_model=schemas.CommentResponse, status_code=status.HTTP_200_OK)
async def update_comment(
        *, db: Session = Depends(deps.get_db),
        comment_id: str, comment_in: schemas.UpdateComment, user: User = Depends(deps.get_current_user)):
    comment = controller.comment.get(db, comment_id)

    await PreviledgeChecker.owner_can_view_data(db, comment.user_id, user)

    updated_comment = controller.comment.update(db, db_obj=comment, obj_in=comment_in)
    return updated_comment


@router.delete('/{comment_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
        *, db: Session = Depends(deps.get_db),
        comment_id: str, user: User = Depends(deps.get_current_user)):
    comment = controller.comment.get(db, comment_id)

    await PreviledgeChecker.owner_can_view_data(db, comment.user_id, user)

    return controller.comment.delete(db, id=comment_id)
