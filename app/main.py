from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.responses import JSONResponse
from loguru import logger

import config

app = FastAPI()
app.mongodb_client = None


@app.on_event("startup")
async def startup():
    # 连接数据库
    app.mongodb_client = AsyncIOMotorClient(config.MONGODB_URL)
    app.db = app.mongodb_client[config.MONGODB_DB]
    logger.info("Startup completed!")
    await app.mongodb_client.server_info()


@app.on_event("shutdown")
async def shutdown():
    app.mongodb_client.client.close()
    logger.info("Shutdown completed!")


@app.get("/")
async def read_root():
    return {"message": "Welcome to 360EvalSystem!"}


@app.get("/favicon.ico")
async def favicon():
    return "123"


@app.get("/health")
async def health_check():
    try:
        # 尝试访问 MongoDB
        await app.mongodb_client.server_info()
        return JSONResponse(content={"status": "ok"}, status_code=200)
    except Exception as e:
        # 如果访问失败，返回错误信息
        return JSONResponse(
            content={"status": "error", "detail": str(e)}, status_code=500
        )


# 这里可以开始添加其他路由和功能，根据项目需求
# 可以参考 FastAPI 官方文档：https://fastapi.tiangolo.com/
