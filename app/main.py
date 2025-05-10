from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.database import engine
from app.models import user, obat, stock, penyakit, pemakaian
from app.api.routes import auth, stock, pemakaian, forecast, upload, debug

# Buat tabel
user.Base.metadata.create_all(bind=engine)

print("✅ FastAPI app is starting...")

app = FastAPI(
    title="Dashboard Prediksi Obat dan Penyakit",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # bisa disesuaikan
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(stock.router, prefix="/stok", tags=["Stok"])
app.include_router(pemakaian.router, prefix="/pemakaian", tags=["Pemakaian"])
app.include_router(forecast.router, prefix="/forecast", tags=["Forecast"])
app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(debug.router, prefix="/debug", tags=["Debug"])




@app.get("/")
def root():
    return {"message": "API is running"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
