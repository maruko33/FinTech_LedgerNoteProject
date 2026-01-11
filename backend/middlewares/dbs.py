from fastapi.requests import Request
from db.session import AsyncSessionFactory


async def create_session_middleware(request: Request,call_next):

    session = AsyncSessionFactory()
    request.state.session = session
    #The part before the watershed is the part executed before the request reaches the view function (written in the router as (add_user)).
    try:
        response = await call_next(request)#watershed-----------
         #The part after the watershed and before the `return` statement executes before the response is sent to the browser.
        await session.commit()
        return response
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()


