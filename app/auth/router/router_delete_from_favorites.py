from fastapi import Depends, HTTPException
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service
from . import router
from fastapi.responses import JSONResponse


@router.delete("/favorites/shanyraks/{tweet_id}", status_code=204)
def delete_from_favorites(
    tweet_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    user_id = jwt_data.user_id

    tweet = svc.repository.get_tweet_by_tweet_id(tweet_id)
    if not tweet:
        raise HTTPException(status_code=404, detail="Tweet not found")
    svc.repository.delete_from_favorites(user_id, tweet_id)

    return JSONResponse(content={"message": "Tweet deleted from favorites"}, status_code=204)
