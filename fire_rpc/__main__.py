from . import start_rpc_server

def echo(*args, **kwargs):
    return {'args': args, 'kwargs': kwargs}

start_rpc_server('/echo', echo, secret='changeme')
