import os

from fastapi import File, UploadFile
from fastapi.responses import FileResponse


def uploadFile(file: UploadFile = File(...)):
    if not os.path.isdir("img"):
        try:
            os.makedirs("img")
        except Exception as e:
            print(e)
    file_name_db = file.filename.replace(" ", "-")
    filename = os.getcwd() + "/img/" + file.filename.replace(" ", "-")
    with open(filename, "wb+") as f:
        f.write(file.file.read())
        f.close()
    return file_name_db


def return_img(name: str):
    filename = os.getcwd() + "/img/" + name
    return FileResponse(path=filename)
