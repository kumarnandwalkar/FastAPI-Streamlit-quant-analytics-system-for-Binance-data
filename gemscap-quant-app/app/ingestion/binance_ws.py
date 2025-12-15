import asyncio
import json
import websockets
from datetime import datetime
from collections import defaultdict, deque
import logging

logger = logging.getLogger("binance_ws")

# in-memory hot buffer
TICK_BUFFER = defaultdict(lambda: deque(maxlen=10000))

def normalize_trade(msg: dict):
    return {
        "symbol": msg["s"].lower(),
        "ts": datetime.fromtimestamp(msg["T"] / 1000),
        "price": float(msg["p"]),
        "size": float(msg["q"])
    }

async def stream_symbol(symbol: str):
    url = f"wss://fstream.binance.com/ws/{symbol}@trade"
    logger.info(f"Connecting to {url}")

    async with websockets.connect(url) as ws:
        async for message in ws:
            data = json.loads(message)
            if data.get("e") == "trade":
                tick = normalize_trade(data)
                TICK_BUFFER[symbol].append(tick)

async def start_stream(symbols: list[str]):
    tasks = [stream_symbol(sym) for sym in symbols]
    await asyncio.gather(*tasks)
