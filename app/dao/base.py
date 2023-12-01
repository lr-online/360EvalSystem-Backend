from typing import List

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import BaseModel


class BaseDao(object):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db[self.collection_name]

    @property
    def model(self):
        raise NotImplementedError

    @property
    def collection_name(self):
        return self.model.__name__.lower()

    async def drop_collection(self):
        await self.collection.drop()

    def convert_to_model(self, data: dict):
        if "_id" in data:
            data["_id"] = str(data["_id"])
        return self.model(**data) if data else None

    async def get_one_by_id(self, _id, fields: dict = None):
        """根据id获取数据

        :param _id:
        :param fields: dict eg: {"name": 1, "age": 1, "_id": 0}
        :return:
        """
        if isinstance(_id, str):
            _id = ObjectId(_id)
        assert isinstance(_id, ObjectId), "_id must be ObjectId or str"
        assert isinstance(fields, dict), "fields must be dict"
        data_in_db = await self.collection.find_one({"_id": _id}, projection=fields)
        return self.convert_to_model(data_in_db)

    async def get_one_by_condition(
        self, condition: dict, fields: dict = None
    ) -> BaseModel:
        """根据条件获取一条数据

        :param condition:
        :param fields: dict eg: {"name": 1, "age": 1, "_id": 0}
        :return:
        """
        assert isinstance(condition, dict), "condition must be dict"
        assert fields is None or isinstance(fields, dict), "fields must be dict"
        data_in_db = await self.collection.find_one(condition, projection=fields)
        return self.convert_to_model(data_in_db)

    async def get_many_by_ids(self, ids: list, fields: dict = None):
        """根据id列表获取数据

        :param ids:
        :param fields: dict eg: {"name": 1, "age": 1, "_id": 0}
        :return:
        """
        assert isinstance(ids, list), "ids must be list"
        assert isinstance(fields, dict), "fields must be dict"
        data_in_db = await self.collection.find(
            {"_id": {"$in": ids}}, projection=fields
        ).to_list(None)
        return [self.convert_to_model(data) for data in data_in_db]

    async def get_many_by_condition(
        self,
        condition: dict = None,
        fields: dict = None,
        sort: list = None,
        limit: int = 10,
    ) -> List[BaseModel]:
        """根据条件获取数据

        :param condition:
        :param fields: dict eg: {"name": 1, "age": 1, "_id": 0}
        :param sort: list eg: [("name", 1), ("age", -1)]
        :param limit: int
        :return:
        """
        condition = condition or {}
        fields = fields or {}
        assert isinstance(condition, dict), "condition must be dict"
        assert isinstance(fields, dict), "fields must be dict"
        data_in_db = await self.collection.find(
            condition, projection=fields, sort=sort, limit=limit
        ).to_list(None)
        return [self.convert_to_model(data) for data in data_in_db]

    async def create_one(self, data: BaseModel):
        """插入一条数据

        :param data:
        :return:
        """
        result = await self.collection.insert_one(data.model_dump(exclude={"id"}))
        return result.inserted_id

    async def update_one_by_id(self, _id, **new_data):
        """根据id更新一条数据

        :param _id:
        :param data:
        :return:
        """
        if isinstance(_id, str):
            _id = ObjectId(_id)
        assert isinstance(_id, ObjectId), "_id must be ObjectId or str"
        await self.collection.update_one({"_id": _id}, {"$set": new_data})
