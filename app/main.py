from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def get_app():
    return "Hello dude"
