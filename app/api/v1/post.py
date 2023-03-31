import string
import uuid

from fastapi import APIRouter, Depends, status, Path
from sqlalchemy.orm.session import Session
from loguru import logger

from app import controller
from app import schemas
from app.api import deps
from app.api.v1.response_helper import parse_post_with_user_data, parse_post_with_user_data_list
from app.core.exception_handler import CustomException
from app.core.provider.previledge_checker import PreviledgeChecker
from app.models.user import User
from app.schemas.common import DataResponse, DataListResponse

router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(*,
                db: Session = Depends(deps.get_db),
                post: schemas.CreatePost,
                user: User = Depends(deps.get_current_user)):
    post.user_id = user.id
    new_post = controller.post.create(db, obj_in=post)
    return new_post


@router.get('/', response_model=DataListResponse[schemas.PostFullResponse], status_code=status.HTTP_200_OK)
def get_posts(*,
              db: Session = Depends(deps.get_db),
              limit: int = 10, skip: int = 0):

    posts = controller.post.get_multi(db, skip=skip, limit=limit)
    parse_posts = parse_post_with_user_data_list(posts)

    data = DataListResponse(success=True, count=len(parse_posts), data=parse_posts)
    return data


@router.get('/{post_id}', response_model=schemas.PostFullResponse, status_code=status.HTTP_200_OK)
def get_post(*,
             db: Session = Depends(deps.get_db),
             post_id: str,
             ):

    post = controller.post.get(db, uuid.UUID(post_id))
    return parse_post_with_user_data(post)


@router.get(
    '/{user_id}/posts', response_model=DataResponse[schemas.ListPostResponse], status_code=status.HTTP_200_OK)
async def get_my_posts(*, user_id: str = Path(title="Logged in user identification"),
                       db: Session = Depends(deps.get_db),
                       limit: int = 10, skip: int = 0, user: User = Depends(deps.get_current_user)):

    await PreviledgeChecker.owner_can_view_data(db, uuid.UUID(user_id), user)

    posts = controller.post.get_multi_posts(db, user_id=user.id, skip=skip, limit=limit)
    data = DataResponse(success=True, data=schemas.ListPostResponse(results=len(posts), posts=posts))
    return data


@router.put('/{post_id}', response_model=schemas.PostResponse, status_code=status.HTTP_200_OK)
async def update_post(
        *, db: Session = Depends(deps.get_db),
        post_id: str, post_in: schemas.UpdatePost, user: User = Depends(deps.get_current_user)):
    post = controller.post.get(db, post_id)

    await PreviledgeChecker.owner_can_view_data(db, post.user_id, user)

    updated_post = controller.post.update(db, db_obj=post, obj_in=post_in)
    return updated_post


@router.delete('/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_post(
        *, db: Session = Depends(deps.get_db),
        post_id: str, user: User = Depends(deps.get_current_user)):
    post = controller.post.get(db, post_id)

    await PreviledgeChecker.owner_can_view_data(db, post.user_id, user)

    updated_post = controller.post.delete(db, id=post_id)
    return updated_post
