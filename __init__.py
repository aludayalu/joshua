"""
Import necessary libraries
"""
from wsgiref.validate import validator as vd
from wsgiref.simple_server import make_server as ms
import json,traceback

paths={}
headerz=[]

def custom_parser(data):
    """
    For parsing data in json.
    """
    funcs=[json.loads]
    for x in funcs:
        try:
            return x(data)
        except:
            continue
    return str(data)

def app(env, start_response):
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
    status = '200 OK'
    if path in paths:
        try:
            temp_res=paths[path](qs,env)
        except:
            import traceback
            traceback.print_exc()
            status = '404 Not Found'
        if temp_res!=b"":
            if type(temp_res)==type(""):
                res=temp_res.encode()
            elif type(temp_res)==type(b""):
                res=temp_res
            elif type(temp_res) in [type(1.0),type(1),type([]),type({})]:
                try:
                    res=json.dumps(temp_res).encode()
                except:
                    status = '404 Not Found'
            else:
                status = '404 Not Found'
    start_response(status, headerz)
    return [res]

def start_server(port=8080,routes={},headers=[('Content-type', 'text/text'),('Access-Control-Allow-Origin', '*')] ):
    """
    This functions starts a http rest api.
    # Arguments
    port: int (default 8080),
    routes: {path:function(query_string,env)} (default {}),
    headers: [(name,value),] (default [('Content-type', 'text/text'),('Access-Control-Allow-Origin', '*')])
    The functions for routes will be called when the api gets a request for the specified end point.
    # Function arguments
    i. Query String (dictionary)
    ii. Environment - Request Details (dictionary)
    """
    global paths,headerz
    paths=routes
    headerz=headers
    validator_app = vd(app)
    with ms('', port, validator_app) as httpd:
        httpd.serve_forever()