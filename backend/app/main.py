from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.analyze import router as analyze_router

app = FastAPI(title="BeNobilis API", description="AI/NLP Powered ATS Resume Analyzer")

# CORS configuration allowing production Netlify frontend and local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze_router)


@app.get("/")
def root():
    return {
        "status": "online",
        "service": "BeNobilis Resume Analyzer API",
        "endpoints": {
            "analyze": "POST /analyze",
            "health": "GET /health"
        }
    }


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "BeNobilis"}