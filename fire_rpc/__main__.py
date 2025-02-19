from . import start_rpc_server

def echo(*args):
    return args
start_rpc_server('/rpc', echo)