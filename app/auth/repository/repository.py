from datetime import datetime
from typing import Optional

from bson.objectid import ObjectId
from pymongo.database import Database

from ..utils.security import hash_password


class AuthRepository:
    def __init__(self, database: Database):
        self.database = database
        
    def add_to_favorites(self, user_id: str, tweet_id: str):
        favorite = {
            "user_id": ObjectId(user_id),
            "tweet_id": ObjectId(tweet_id),
        }
        self.database["favorites"].insert_one(favorite)
        
    def delete_from_favorites(self, user_id: str, tweet_id: str):
        self.database["favorites"].delete_one(
            {"user_id": ObjectId(user_id), "tweet_id": ObjectId(tweet_id)}
        )
        
    def get_all_from_database_favorites(self, user_id: str):
        return self.database["favorites"].find({"user_id": ObjectId(user_id)})
    
    def get_tweet_by_tweet_id(self, tweet_id: str):
        return self.database["tweets"].find_one({"_id": ObjectId(tweet_id)})

    def create_user(self, user: dict):
        payload = {
            "email": user["email"],
            "password": hash_password(user["password"]),
            "created_at": datetime.utcnow(),
        }

        self.database["users"].insert_one(payload)

    def get_user_by_id(self, user_id: str) -> Optional[dict]:
        user = self.database["users"].find_one(
            {
                "_id": ObjectId(user_id),
            }
        )
        return user

    def get_user_by_email(self, email: str) -> Optional[dict]:
        user = self.database["users"].find_one(
            {
                "email": email,
            }
        )
        return user
