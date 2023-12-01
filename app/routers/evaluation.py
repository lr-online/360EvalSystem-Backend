from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from models.evaluation import Evaluation
from dependencies import get_mongo_db

router = APIRouter()


@router.post("/create_evaluation", response_model=Evaluation)
async def create_evaluation(
    evaluation: Evaluation, db: AsyncIOMotorDatabase = Depends(get_mongo_db)
):
    # 在这里将 Pydantic 模型映射到 MongoDB 文档
    eval_doc = evaluation.dict()
    # 在 MongoDB 中插入评价文档
    result = await db.evaluations.insert_one(eval_doc)
    # 获取插入后的评价文档
    created_evaluation = await db.evaluations.find_one({"_id": result.inserted_id})
    return created_evaluation
