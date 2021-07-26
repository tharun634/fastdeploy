
from fastapi import FastAPI
from myservice import MyService
import uvicorn

app = FastAPI()

myservice_func=MyService()

@app.get("/")
def hello_world():
    msg="Welcome to my FastAPI project!        Please visit the /docs to see the API documentation."
    return msg

    
# WARNING:DO NOT EDIT THE BELOW LINE
app.add_api_route(
        path="/external",
        endpoint=myservice_func.external,
        methods=['GET'],
    )

        
# WARNING:DO NOT EDIT THE BELOW LINE
app.add_api_route(
        path="/printMessage",
        endpoint=myservice_func.printMessage,
        methods=['GET'],
    )

        
# WARNING:DO NOT EDIT THE BELOW LINE
app.add_api_route(
        path="/printSum",
        endpoint=myservice_func.printSum,
        methods=['POST'],
    )

        
if __name__ == "__main__":
    uvicorn.run(
            app=app,
            host='localhost',
            port=5000
        )
