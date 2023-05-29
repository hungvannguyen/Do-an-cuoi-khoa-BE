import os

from fastapi import File, UploadFile


def uploadFile(file: UploadFile = File(...)):
    try:
        os.makedirs("img")
    except Exception as e:
        print(e)
    filename = os.getcwd() + "/img/" + file.filename.replace(" ", "-")
    with open(filename, "wb+") as f:
        f.write(file.file.read())
        f.close()
    return filename
