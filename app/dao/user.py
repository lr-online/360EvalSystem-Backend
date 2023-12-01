from dao.base import BaseDao
from models.user import User


class UserDao(BaseDao):
    @property
    def model(self):
        return User
