from dao.base import BaseDao
from models.role import Role


class RoleDao(BaseDao):
    @property
    def model(self):
        return Role
