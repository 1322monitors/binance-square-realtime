"""Real-time Binance Square monitor over WebSocket.

Streams new Binance Square posts (with coin pairs) as they publish. Set API_KEY
and WS_URL from your 1322 dashboard. See README for details.
"""
import asyncio
import json
import os

import websockets

API_KEY = os.environ.get("API_KEY")
WS_URL = os.environ.get("WS_URL")


async def run():
    if not API_KEY or not WS_URL:
        raise SystemExit("set API_KEY and WS_URL (see README)")
    while True:
        try:
            async with websockets.connect(WS_URL, additional_headers={"X-Api-Key": API_KEY}) as ws:
                print("connected: binance square feed")
                async for raw in ws:
                    try:
                        event = json.loads(raw)
                    except ValueError:
                        continue
                    if event.get("platform") != "binance":
                        continue
                    pairs = ",".join(event.get("coinPairs") or [])
                    handle = event.get("handle", "?")
                    ts = event.get("timestamp", "")
                    print(f"[{ts}] @{handle} [{pairs}]: {event.get('content', '')}")
        except Exception as exc:  # noqa: BLE001 - keep the consumer alive
            print(f"disconnected ({exc}); reconnecting in 1s")
            await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(run())
