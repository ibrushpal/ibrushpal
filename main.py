from fastapi import FastAPI
from api.detection import router as detection_router
from api.cleanliness import router as cleanliness_router
from api.recommendation import router as recommendation_router
from api.admin import router as admin_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="iBrushPal AI API",
    description="口腔健康AI分析系统API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(detection_router, prefix="/api/v1")
app.include_router(cleanliness_router, prefix="/api/v1")
app.include_router(recommendation_router, prefix="/api/v1")
app.include_router(admin_router, prefix="/api/admin")

@app.get("/")
async def root():
    return {"message": "iBrushPal AI Service"}