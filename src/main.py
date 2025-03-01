from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {'msg': 'Hello World'}


@app.get("/add/{a}/{b}")
def add(a: int, b: int):
    return {"result": a + b}