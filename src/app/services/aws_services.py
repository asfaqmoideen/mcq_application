import json

import boto3
from fastapi import HTTPException, UploadFile

from app.config.settings import app_config
from app.schemas.mcq_schemas import UserOutput

s3_client = boto3.client("s3")
lambda_client = boto3.client("lambda", region_name=app_config["REGION_NAME"])


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
    try:
        response = lambda_client.invoke(
            FunctionName=app_config["LAMBDA_FUNCTION_NAME"],
            InvocationType="RequestResponse",
            Payload=json.dumps(data),
        )
        response_payload = json.loads(response["Payload"].read().decode("utf-8"))

        if response.get("StatusCode") == 200:
            return response_payload
        else:
            raise HTTPException(
                status_code=response.get("StatusCode"),
                detail="Certificate generation failed",
            )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Lambda invocation error: {str(e)}"
        )


def generate_presigned_url(file_key: str):
    """
    Fetches an object from S3 and returns its content.
    """
    try:
        presigned_url = s3_client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": app_config["CERTIFICATE_OUTPUT_BUCKET_NAME"],
                "Key": file_key,
            },
            ExpiresIn=300,
        )

        return {"message": "Presigned URL generated successfully", "url": presigned_url}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating presigned URL: {str(e)}"
        )
