from fastapi.requests import Request
from db.session import AsyncSessionFactory


async def create_session_middleware(request: Request,call_next):

    session = AsyncSessionFactory()
    request.state.session = session
    #分水岭之前的 就是request到达视图函数（router里写的（add_user））之前执行的
    try:
        response = await call_next(request)#分水岭-----------
         #分水岭之后，return之前是response返回给浏览器之前执行的
        return response
    finally:
        await session.close()


