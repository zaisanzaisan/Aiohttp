from aiohttp import web

from database import begin_s, end_s, get_session
from views.Adv import Adv
from views.UserManage import UsersManage

app = web.Application()


async def orm_context(app: web.Application):
    print("START")
    await begin_s()
    yield
    await end_s()
    print("SHUT DOWN")


@web.middleware
async def session_middleware(request: web.Request, handler):
    session = await get_session()
    request["session"] = session
    response = await handler(request)
    await session.close()
    return response


app.cleanup_ctx.append(orm_context)
app.middlewares.append(session_middleware)
app.add_routes(
    [
        web.get("/user/{user_id:\d+$}", UsersManage),
        web.post("/user", UsersManage),
        web.get("/adv", Adv),
        web.post("/adv", Adv),
        web.patch("/adv/{user_id:\d+}/{ad_id:\d+}", Adv),
        web.delete("/adv", Adv),
    ]
)

if __name__ == '__main__':
    web.run_app(app)
