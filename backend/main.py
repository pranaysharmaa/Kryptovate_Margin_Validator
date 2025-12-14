from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.assets import router as assets_router
from routes.margin import router as margin_router

app = FastAPI(title="Margin Requirement API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(assets_router)
app.include_router(margin_router)
