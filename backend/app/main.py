from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def get_hello():
    print("hello")
    return {"message": "hello world"}