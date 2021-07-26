import inspect
import logging
import multiprocessing
import os
import re
import subprocess
import sys
import tempfile
import threading
import uuid
from datetime import datetime
from typing import List

# FastAPI file creation
template1 = """
from fastapi import FastAPI
from {path} import {class_name}
import uvicorn

app = FastAPI()

{func_name}={class_name}()

@app.get("/")
def hello_world():
    msg="Welcome to my FastAPI project!\
        Please visit the /docs to see the API documentation."
    return msg\n
    """
template2 = """
# WARNING:DO NOT EDIT THE BELOW LINE
app.add_api_route(
        path="/{route_path}",
        endpoint={endpoint},
        methods={http_methods},
    )\n
        """
template3 = """
if __name__ == "__main__":
    uvicorn.run(
            app=app,
            host='localhost',
            port=5000
        )\n"""


class InferenceAPI:
    
    def __init__(
        self,
        service,
        name,
        user_func: callable,
        route=None,
        http_methods=None,
        ):
        self._service = service
        self._name = name
        self._user_func = user_func
        self._http_methods = http_methods
        self.route = name if route is None else route

#api decorator which will be used by sub classes
def api_decorator(
    *args,
    api_name: str = None,
    route: str = None,
    http_methods: List[str] = None,
    **kwargs,
):
    
    def decorator(func):
        _api_name = func.__name__ if api_name is None else api_name
        _api_route = _api_name if route is None else route
        _http_methods = http_methods if http_methods else ['GET']
        setattr(func, "_is_api", True)
        setattr(func, "_api_name", _api_name)
        setattr(func, "_api_route", _api_route)
        setattr(func, "_http_methods", _http_methods)
        return func

    return decorator

class LambdaService:
    _api_list: List[InferenceAPI] = []
    _lambda_service_name: str = None
    
    def __init__(self):
        _lambda_service_name = None
        
    def create_fastapi_file(self,module_name):
        class_name = self.__name__
        apis_list = []
        
        #gets all the api functions in the current class
        for _, function in inspect.getmembers(
            self,
            predicate=lambda x: inspect.isfunction(x) or inspect.ismethod(x),
        ):
            if hasattr(function, "_is_api"):
                api_name = getattr(function, "_api_name")
                route = getattr(function, "_api_route", None)
                http_methods = getattr(function, "_http_methods")
                user_func = function.__get__(self)
                print(http_methods)
                apis_list.append(
                    InferenceAPI(
                        self,
                        api_name,
                        user_func=user_func,
                        http_methods=http_methods,
                        route=route,
                    )
                )
        
        store_path = os.path.abspath(os.curdir) + '\\build\\api.py'
        func_name = class_name.lower() + "_func"
        complete_template = template1.format(
            path=module_name,
            class_name=class_name,
            func_name=func_name 
        )
        #adds api endpoint for each api function
        for api in apis_list:
            print(api)
            complete_template += template2.format(
                route_path=api.route,
                endpoint=f"{func_name}.{api._name}",
                http_methods=api._http_methods
            )

        complete_template += template3.format(
            func_name=func_name
        )

        try:
            with open(store_path, "w") as f:
                f.write(complete_template)
        except FileExistsError:
            raise Exception("The FastAPI file already exists")




                
