from fastapi import FastAPI
from app.routes.router import router as flower_router
import app.database as db
from app.seed import seed_flowers
from fastapi.middleware.cors import CORSMiddleware

db.start_db()
seed_flowers()

app = FastAPI()
app.include_router(flower_router, prefix="/flowers", tags=["Flowers"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3055"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)