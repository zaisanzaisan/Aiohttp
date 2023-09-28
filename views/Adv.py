import json

from aiohttp import web
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from database import Advertisements


class Adv(web.View):

    @property
    def session(self):
        return self.request["session"]

    @property
    def user_id(self):
        return int(self.request.match_info["user_id"])

    async def get(self):
        json_data = await self.request.json()
        if not int(json_data.get("user_id")):
            raise web.HTTPConflict(text=str({"error": "user provide"}), content_type="application/json")
        q = select(Advertisements).where(Advertisements.owner_id == int(json_data["user_id"]))
        result = await self.session.execute(q)
        db_resp = result.fetchall()
        context = dict()
        context["status"] = "ok"
        for cnt, adv in enumerate(db_resp):
            adv = adv[0]
            context[str(cnt)] = {
                "id": adv.id,
                "owner_id": adv.owner_id,
                "title": adv.title,
                "description": adv.description,
            }
        return web.json_response(context)

    async def post(self):
        json_data = await self.request.json()
        try:
            adv = Advertisements(
                title=json_data["title"],
                description=json_data["description"],
                owner_id=int(json_data["owner_id"]),
            )
            self.session.add(adv)
            await self.session.commit()
        except IntegrityError as e:
            raise web.HTTPConflict(text=json.dumps({"error": str(e.args).split("DETAIL:", 2)[1]}),
                                   content_type="application/json")
        context = {
            "status": "ok",
            "adv_id": adv.id,
            "created_at": str(adv.created_at)
        }
        return web.json_response(context)

    async def patch(self):
        json_data = await self.request.json()
        q = select(Advertisements) \
            .where(Advertisements.id == int(self.request.match_info["ad_id"])) \
            .where(Advertisements.owner_id == self.user_id)
        result = await self.session.execute(q)
        adv = result.scalar()
        if not adv:
            raise web.HTTPNotFound()
        if json_data.get("title"):
            adv.title = json_data.get("title")
        if json_data.get("description"):
            adv.description = json_data.get("description")
        # self.session.add(adv)
        await self.session.commit()
        context = {
            "status": "ok",
            "adv_id": adv.id,
            "created_at": str(adv.created_at)
        }
        return web.json_response(context)

    async def delete(self):
        json_data = await self.request.json()
        q = select(Advertisements).filter(Advertisements.id == int(json_data["id"]),  # validation required
                                          Advertisements.owner_id == int(json_data["owner_id"]))
        result = await self.session.execute(q)
        result = result.fetchall()
        if not result:
            raise web.HTTPNotFound()
        for x in result:
            x = x[0]
            await self.session.delete(x)
        await self.session.commit()
        context = {
            "status": "ok",
        }
        return web.json_response(context)
