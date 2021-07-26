import numpy as np
import fastdeploy.myfunctions as fastdeploy
import external_file as ext
class MyService(fastdeploy.LambdaService):
    @fastdeploy.api_decorator(http_methods=["GET"])
    def printMessage(self, a: int, b: int):
        message = "this is a test run"
        return message

    @fastdeploy.api_decorator(http_methods=["POST"])
    def printSum(self):
        arr1 = np.array([3, 2, 1])
        arr2 = np.array([1, 2, 3])
        return np.add(arr1,arr2)
    
    @fastdeploy.api_decorator(http_methods=["GET"])
    def external(self):
        return ext.externalFunction()
    
