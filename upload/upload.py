import os
from datetime import datetime
from fastapi import File, UploadFile, HTTPException, status
from fastapi.responses import FileResponse



def uploadFile(file: UploadFile = File(...)):
    if not os.path.isdir("img"):
        try:
            os.makedirs("img")
        except Exception as e:
            print(e)
    file_name_replace = file.filename.replace(" ", "-")
    dot_position = file_name_replace.find(".")
    extension = file_name_replace[dot_position:len(file.filename)]
    file_name = file_name_replace[0:dot_position]
    file_name_db = file_name + "_" + str(datetime.timestamp(datetime.now())) + extension
    filename = os.getcwd() + "/img/" + file_name_db
    with open(filename, "wb+") as f:
        f.write(file.file.read())
        f.close()
    return file_name_db


def return_img(name: str):
    filename = os.getcwd() + "/img/" + name
    if not os.path.isfile(filename):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không thấy ảnh")
    return FileResponse(path=filename)
