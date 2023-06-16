from fastapi import Depends
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from fastapi.responses import JSONResponse


from ..service import Service, get_service
from . import router


@router.get("/favorites/shanyraks", status_code=201)
def get_from_favorites(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    user_id = jwt_data.user_id
    favorites = svc.repository.get_all_from_database_favorites(user_id)
    list_of_tweet_ids = [str(favorite["tweet_id"]) for favorite in favorites]

    tweets = []
    for tweet_id in list_of_tweet_ids:
        tweet = svc.repository.get_tweet_by_tweet_id(tweet_id)
        tweet["_id"] = str(tweet["_id"])  # Convert ObjectId to string
        tweets.append(tweet)

    return JSONResponse(content={"tweets": [str(tweet) for tweet in tweets]}, 
                        status_code=200)
