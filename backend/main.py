from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from middlewares import dbs
from starlette.middleware.base import BaseHTTPMiddleware
from routers.v1.router import router as api_router
from core import auth

app = FastAPI(title="LedgerNotes API")

# 允许本地前端访问（Vite 默认 5173 端口）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#DB session middleware（后端内部用）
app.add_middleware(BaseHTTPMiddleware, dispatch=dbs.create_session_middleware)

#路由
app.include_router(api_router)
app.include_router(auth.router)


#test 
@app.get("/health")
def health():
    return {"status": "ok"}




####docker & mysql####

#   docker start carenote-mysql                             pull up sql in docker 
#   docker ps                                               check docker status
#   mysql -h 127.0.0.1 -P 3307 -u fastapi -p                log in to mysql

#   docker stop carenote-mysql                              stop docker

####alembic ####

#alembic revision --autogenerate -m "init models"           execute alembic in root dict

#alembic upgrade head                                       alembic will connect to mysql and setup tables

#activate virtual environment
#source .venv/bin/activate

#fastAPI：
#uvicorn main:app --reload                         start fastAPI