from fastapi import Depends
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data


from ..service import Service, get_service
from . import router


@router.post("/favorites/shanyraks/{tweet_id}", status_code=201)
def add_to_favorites(
    tweet_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    user_id = jwt_data.user_id
    svc.repository.add_to_favorites(user_id, tweet_id)
