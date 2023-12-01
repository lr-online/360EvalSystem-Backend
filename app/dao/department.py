from dao.base import BaseDao
from models.department import Department


class DepartmentDAO(BaseDao):
    @property
    def model(self):
        return Department

    async def get_department_tree(self) -> dict:
        department_id_map = {}  # _id: document
        async for department in self.collection.find():
            department["_id"] = str(department["_id"])
            department["children"] = []
            department_id_map[department["_id"]] = department

        root_department = None
        for department in department_id_map.values():
            parent_id = department["parent_id"]
            if parent_id:
                department_id_map[parent_id]["children"].append(department)
            else:
                root_department = department
        return root_department

    # 其他操作...
