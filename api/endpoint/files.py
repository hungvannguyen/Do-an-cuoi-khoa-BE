from fastapi import Depends, UploadFile, File, APIRouter, status

from upload.upload import uploadFile, return_img

router = APIRouter()


@router.post("/upload")
def upload(file: UploadFile = File(...)):
    filename = uploadFile(file)
    return {"filename": filename}


@router.get("/img/{name}")
def get_img(name: str):
    return return_img(name=name)
