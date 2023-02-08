from wsgiref.validate import validator as vd
from wsgiref.simple_server import make_server as ms
import json,traceback

paths={}

def custom_parser(data):
    funcs=[json.loads]
    for x in funcs:
        try:
            return x(data)
        except:
            continue
    return str(data)

def app(env, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/html'),('Access-Control-Allow-Origin', '*')] 
    start_response(status, headers)
    path=env["PATH_INFO"]
    qs=env["QUERY_STRING"].split("&")
    if "" in qs:qs.remove("")
    qs_copy=qs.copy()
    qs={}
    for x in qs_copy:
        try:
            key=custom_parser(x.split("=")[0])
            val=custom_parser(x.split("=")[1])
            qs[key]=val
        except:
            pass
    res=b""
    temp_res=b""
    if path in paths:
        try:
            temp_res=paths[path](qs)
        except:
            traceback.print_exc()
        if temp_res!=b"":
            if type(temp_res)==type(""):
                res=temp_res.encode()
            if type(temp_res)==type(b""):
                res=temp_res
            if type(temp_res) in [type(1.0),type(1),type([]),type({})]:
                try:
                    res=json.dumps(temp_res).encode()
                except:
                    print(";/")
    return [res]

def start_server(port,routes):
    global paths
    paths=routes
    validator_app = vd(app)
    with ms('', port, validator_app) as httpd:
        httpd.serve_forever()