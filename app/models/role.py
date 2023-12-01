from enum import Enum
from typing import List, Optional

from models.base import BaseModel


class PermissionTypeEnum(str, Enum):
    """角色权限类型枚举

    基本原则：
    1. 所有角色都可以查看全部评选活动
    2. 组长
    """
    CREATE_EVALUATION = "create_evaluation"
    DELETE_EVALUATION = "delete_evaluation"
    GET_ALL_EVALUATION_LIST = "get_all_evaluation_list"
    GET_OWN_EVALUATION_LIST = "get_own_evaluation_list"


class Role(BaseModel):
    permissions: Optional[List[str]] = []
