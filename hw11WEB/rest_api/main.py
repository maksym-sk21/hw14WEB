import redis.asyncio as redis
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter

from rest_api.src.routes import contacts, auth
from rest_api.src.conf.config import settings

app = FastAPI()

app.include_router(auth.router, prefix='/api')
app.include_router(contacts.router, prefix='/api')


@app.on_event("startup")
async def startup():
    r = await redis.Redis(host=settings.redis_host,
                          port=settings.redis_port,
                          password=settings.redis_password,
                          db=0,
                          encoding="utf-8",
                          decode_responses=True)
    await FastAPILimiter.init(r)


@app.get("/")
def read_root():
    return {"message": "Hello World"}
