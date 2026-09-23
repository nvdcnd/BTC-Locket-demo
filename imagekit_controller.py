import uuid

import dotenv
import imagekitio
import os

dotenv.load_dotenv()  # Load environment variables from .env file

imagekit_instance = imagekitio.AsyncImageKit(
    private_key=os.getenv("IMAGEKIT_PRIVATE_KEY"),
)

async def upload_image(data=None, filename="hello", imagekit_instance=imagekit_instance):
    data = await data.read()  # Nhận data ảnh dạng bytes từ front-end (async read của UploadFile)
    unique_filename = f"{uuid.uuid4().hex}_{filename}.jpg"

    upload_response = await imagekit_instance.files.upload(
        file=data,
        file_name=unique_filename,
    )

    if upload_response.url:
        return upload_response.url
    raise RuntimeError("ImageKit upload failed: no url in response")