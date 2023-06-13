import os

from fastapi import File, UploadFile, HTTPException, status
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
    if not os.path.isfile(filename):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không thấy ảnh")
    return FileResponse(path=filename)
