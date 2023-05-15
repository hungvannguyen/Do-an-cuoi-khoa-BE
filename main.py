import os

from fastapi import FastAPI, Depends, UploadFile, File
from passlib.context import CryptContext

from login import LoginRequest
from security.security import gen_token, reusable_oauth2, check_token

app = FastAPI()

fake_db = []

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


def get_hashed_pass(password: str):
    return pwd_context.hash(password)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/regis")
def regis(request: LoginRequest):
    hashed_pass = get_hashed_pass(request.password)
    obj_in = {
        "username": request.username,
        "hashedpassword": hashed_pass
    }
    fake_db.append(obj_in)
    print(fake_db[0].get('username'))

@app.post("/login")
def login(request: LoginRequest):
    if request.username == fake_db[0].get('username') and pwd_context.verify(request.password,fake_db[0].get('hashedpassword')):
        return gen_token(request.username)
    return {"Not"}


@app.get("/test", dependencies=[Depends(check_token)])
def test():
    return {
        'title': "abc",
        'content': "content"
    }


@app.post("/upload")
def upload(file: UploadFile = File(...)):
    try:
        os.makedirs("test_folder")
    except Exception as e:
        print(e)
    filename = os.getcwd() + "/test_folder/" + file.filename.replace(" ", "-")
    with open(filename, "wb+") as f:
        f.write(file.file.read())
        f.close()

    return {"filename": filename}
