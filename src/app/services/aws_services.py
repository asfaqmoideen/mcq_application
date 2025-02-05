import boto3
import requests
from fastapi import HTTPException, UploadFile

from app.config.settings import app_config
from app.schemas.mcq_schemas import UserOutput

s3_client = boto3.client("s3")


def upload_template(file: UploadFile, current_user: UserOutput):
    """
    Upload a .jpg file to S3 as a certificate template.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=401, detail="Access denied. Admin role required."
        )

    if file.content_type != "image/jpeg":
        raise HTTPException(
            status_code=400, detail="Invalid file type. Please upload a .jpg file."
        )

    file_name = "image_template/template_ui.jpg"

    s3_client.upload_fileobj(file.file, app_config["BUCKET_NAME"], file_name)

    return {"message": f"File uploaded successfully to {file_name}"}


def generate_certificate(data: dict):
    """
    Sends a POST request to generate a certificate and retrieves the certificate URL.
    """
    response = requests.post(app_config["API_URL"], json=data)

    if response.status_code == 200:
        result = response.json()
        return result.get("body")

    else:
        raise HTTPException(
            status_code=response.status_code, detail="Certificate generation failed"
        )
