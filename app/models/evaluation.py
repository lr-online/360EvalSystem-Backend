from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class EvaluationStatusEnum(str, Enum):
    DRAFT = "draft"  # 刚创建，草稿状态
    PUBLISHED = "published"  # 已发布
    CLOSED = "closed"  # 已关闭
    DELETED = "deleted"  # 已删除


class Evaluation(BaseModel):
    _id: str
    deadline: datetime  # 截止日期
    title: str  # 主题
    status: EvaluationStatusEnum  # 状态
    created_by: str  # user_id
    created_at: datetime  # 创建时间
