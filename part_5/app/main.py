from fastapi import FastAPI
from app.router import spimex_result_router


app = FastAPI()

app.include_router(spimex_result_router)
