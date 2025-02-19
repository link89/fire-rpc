from aiohttp import web
import asyncio
import fire
import json


def make_rpc_server(base_url: str, cmd_entry, secret = None):
    if not base_url.endswith('/'):
        base_url += '/'

    async def handler(request: web.Request) -> web.Response:
        try:
            if secret is not None:
                auth_token = request.headers.get('X-Auth-Token')
                if auth_token != secret:
                    return web.json_response({'error': 'unauthorized'}, status=401)
            data = await request.json()
            args = data.get('args')
            if args is None:
                return web.json_response({'error': 'args not found'}, status=400)
            if not isinstance(args, list):
                return web.json_response({'error': 'args must be a list'}, status=400)
            ret = fire.Fire(cmd_entry, args)
            res = {'result': ret}
            return web.json_response(res)
        except (Exception, SystemExit) as e:
            return web.json_response({'error': str(e)}, status=400)

    app = web.Application()
    app.add_routes([web.post(base_url, handler)])
    return app


def start_rpc_server(base_url: str, cmd_entry, secret=None, host='localhost', port=8000):
    loop = asyncio.new_event_loop()
    app = make_rpc_server(base_url, cmd_entry, secret=secret)
    web.run_app(app, loop=loop, host=host, port=port)
