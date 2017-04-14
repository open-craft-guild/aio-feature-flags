from aiohttp.web_urldispatcher import View

from web_utils import async_json_out


class Index(View):
    @async_json_out
    async def get(self, request):
        """Return dummy json in response to HTTP GET request."""
        return {'content': 'feature-flags-api'}


class Flag(View):

    @async_json_out
    async def get(self, request):
        """React for GET request."""
        # TODO create get request

    @async_json_out
    async def post(self, request):
        """React for POST request."""
        # TODO create post request
