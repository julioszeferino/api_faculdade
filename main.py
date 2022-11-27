from fastapi import FastAPI
from core.configs import settings
from api.v1.api import api_router as api_router_v1

app = FastAPI(title="Curso API - Seguranca")

app.include_router(api_router_v1, prefix=settings.API_V1_STR)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="0.00.0.0", port=8000, reload=True, log_level="info")