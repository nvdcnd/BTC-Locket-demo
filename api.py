# Thư viện để load biến môi trường từ file .env
import os
import dotenv

# Thư viện base cho FastAPI
from fastapi import FastAPI, File, UploadFile, Form
from typing import Optional
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Thư viện cho phân trang (Pagination)
from fastapi_pagination.cursor import CursorPage
from fastapi_pagination.ext.sqlmodel import paginate
from fastapi_pagination import add_pagination

# Thư viện cho cơ sở dữ liệu
from database.models import Image
from sqlmodel import Session, select
from database.database import create_db_and_tables, engine

# Thư viện cho ImageKit
from imagekit_controller import upload_image

# Thư viện cho chạy ứng dụng
import uvicorn

# Khai báo ứng dụng FastAPI & thêm phân trang
app = FastAPI()
add_pagination(app)

# Load biến môi trường từ file .env
dotenv.load_dotenv()  

# Cho phép front-end ở origin khác gọi API (Live Server, file://, v.v.)
cors_origins = os.getenv("CORS_ORIGINS", "*")  # Cho phép tất cả origin (có thể thay đổi để bảo mật hơn)
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins.split(","),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Check và tạo cơ sở dữ liệu khi khởi động ứng dụng
@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# API endpoint để upload ảnh (multipart/form-data: image, description?, name?)
@app.post("/upload/image/")
async def upload_image_api(
    image: UploadFile = File(...),
    description: Optional[str] = Form(None),
    name: str = Form("Người trải nghiệm"),
):
    upload_response = await upload_image(data=image, filename=name)

    # "" thay vì None để tương thích với bảng DB cũ (description NOT NULL)
    new_image = Image(url=upload_response, name=name, description=description or "")

    with Session(engine) as session:
        session.add(new_image)
        session.commit()
        session.refresh(new_image)

    return {"message": "Image uploaded successfully", "image": new_image}


# API endpoint để lấy danh sách ảnh với phân trang kiểu cursor (?cursor=&size=)
@app.get("/images/", response_model=CursorPage[Image])
def get_images():
    with Session(engine) as session:
        images = select(Image).order_by(Image.created_at.desc(), Image.id.desc())
        return paginate(session, images)

@app.get("/health/")
def check_health():
    return {"status": "ok"}

# Triển khai thực thế ko cần
# Phục vụ front-end tĩnh nếu thư mục frontend nằm cạnh backend (chạy full-stack local).
# Khi deploy API-only (VD: HF Space chỉ copy backend/), bỏ qua để không crash.
_frontend_dir = Path(__file__).parent.parent / "frontend"
if _frontend_dir.is_dir():
    app.mount(
        "/",
        StaticFiles(directory=str(_frontend_dir), html=True),
        name="frontend",
    )


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)