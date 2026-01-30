from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.predict import router as predict_router

app = FastAPI(
    title="TCC Previsor de Renda",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

# ⬇️ ESTA LINHA É O QUE ESTAVA FALTANDO
app.include_router(predict_router)
