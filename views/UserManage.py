import json

from aiohttp import web
from sqlalchemy.exc import IntegrityError

from database import User


class UsersManage(web.View):

    @property
    def session(self):
        return self.request["session"]

    @property
    def user_id(self):
        return int(self.request.match_info["user_id"])

    async def get(self):
        user = await self.session.get(User, self.user_id)
        if not user:
            raise web.HTTPNotFound()
        # q = select(User).filter(User.id == int(self.request.match_info["user_id"]))
        # result = await self.session.execute(q)
        # user = result.scalar()  # result.fetchall() result.scalars().one_or_none()
        context = {
            "uid": user.id,
            "name": user.name
        }
        return web.json_response(context)

    async def post(self):
        # validated_data = UserValidate(**request.json).dict()
        json_data = await self.request.json()
        try:
            usr = User(name=json_data["name"])
            self.session.add(usr)
            await self.session.commit()
        except IntegrityError as e:
            raise web.HTTPConflict(
                text=json.dumps({"error": e.args}),
                content_type="application/json",
            )
        context = {
            "status": "ok",
            "uid": usr.id,
            "name": usr.name
        }
        return web.json_response(context)

    def patch(self):
        pass

    def delete(self):
        pass
