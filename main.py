from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uuid, os
from converter import pdf_to_excel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/convert")
async def convert(file: UploadFile = File(...)):
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)

    pdf_path = f"uploads/{uuid.uuid4()}.pdf"
    excel_path = f"outputs/{uuid.uuid4()}.xlsx"

    with open(pdf_path, "wb") as f:
        f.write(await file.read())

    pdf_to_excel(pdf_path, excel_path)

    return FileResponse(
        excel_path,
        filename="Converted.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
