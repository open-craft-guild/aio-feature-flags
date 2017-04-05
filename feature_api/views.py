from aiohttp.web_urldispatcher import View

from web_utils import async_json_out



class Index(View):
    @async_json_out
    async def get(self, request):
        return {'content': 'feature-flags-api'}
