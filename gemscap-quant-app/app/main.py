import asyncio
import threading
from fastapi import FastAPI
from app.ingestion.binance_ws import start_stream
from app.config import SYMBOLS
from app.logger import setup_logger
from app.api.routes import router

setup_logger()

app = FastAPI()
app.include_router(router)

def start_ws():
    asyncio.run(start_stream(SYMBOLS))

@app.on_event("startup")
def startup():
    thread = threading.Thread(target=start_ws, daemon=True)
    thread.start()
