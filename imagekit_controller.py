import uuid

import dotenv
import imagekitio
import os

dotenv.load_dotenv()  # Load environment variables from .env file

imagekit_instance = imagekitio.AsyncImageKit(
    private_key=os.getenv("IMAGEKIT_PRIVATE_KEY"),
)

# API contract: frontend nén trước; backend vẫn chặn request vượt ngưỡng.
MAX_IMAGE_BYTES = 50 * 1024  # 50 KiB


async def upload_image(data=None, filename="hello", imagekit_instance=imagekit_instance):
    if hasattr(data, "read"):
        data = await data.read(MAX_IMAGE_BYTES + 1)
    if not isinstance(data, (bytes, bytearray)) or not data:
        raise ValueError("Image upload is empty")
    if len(data) > MAX_IMAGE_BYTES:
        raise ValueError("Image must be 50 KiB or smaller")

    data = bytes(data)
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        extension = "png"
    elif data.startswith(b"RIFF") and data[8:12] == b"WEBP":
        extension = "webp"
    else:
        extension = "jpg"
    unique_filename = f"{uuid.uuid4().hex}_{filename}.{extension}"

    upload_response = await imagekit_instance.files.upload(
        file=data,
        file_name=unique_filename,
    )

    if upload_response.url:
        return upload_response.url
    raise RuntimeError("ImageKit upload failed: no url in response")