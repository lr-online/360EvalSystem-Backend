from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from models.user import User

router = APIRouter()


@router.post("/create_user", response_model=User)
async def create_user(user: User, db: AsyncIOMotorDatabase = Depends(get_mongo_db)):
    # 在这里将 Pydantic 模型映射到 MongoDB 文档
    user_doc = user.dict()
    # 在 MongoDB 中插入用户文档
    result = await db.users.insert_one(user_doc)
    # 获取插入后的用户文档
    created_user = await db.users.find_one({"_id": result.inserted_id})
    return created_user
