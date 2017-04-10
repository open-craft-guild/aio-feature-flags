from aiohttp.web_urldispatcher import View

from web_utils import async_json_out
import db

class Index(View):
    @async_json_out
    async def get(self, request):
        return {'content': 'feature-flags-api'}


class Flag(View):

    @async_json_out
    async def get(self, request):
        # TODO create get request

    @async_json_out
    async def post(self, request):
        # TODO create post request
