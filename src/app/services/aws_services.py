import boto3
from fastapi import HTTPException, UploadFile

from app.config.settings import app_config
from app.schemas.mcq_schemas import UserOutput


def upload_template(file: UploadFile, current_user: UserOutput):
    """
    Upload a .docx file to S3 as a certificate template.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=401, detail="Access denied. Admin role required."
        )

    if file.content_type != (
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ):
        raise HTTPException(
            status_code=400, detail="Invalid file type. Please upload a .docx file."
        )

    file_name = f"certificate_templates/{file.filename}.docx"
    s3_client = boto3.client("s3")
    s3_client.upload_fileobj(file.file, app_config["BUCKET_NAME"], file_name)

    return {"message": f"File uploaded successfully to {file_name}"}
