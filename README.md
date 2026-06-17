# binance-square-realtime

Real-time **Binance Square** post monitor over **WebSocket**. Minimal Node and
Python clients that stream new Binance Square posts (with the coin pairs they
mention) the moment they publish.

There is **no official Binance API for reading Binance Square posts in real
time** (the public Square endpoint is for *publishing* content, not monitoring).
The common workarounds are browser automation or scraping the Square web app on
a timer. This repo shows the alternative: a persistent WebSocket that pushes each
post as it is detected, so you are not polling.

These examples run against the [1322](https://1322.io) managed Binance Square
feed (real-time WebSocket + REST, roughly 150-250ms detection, with optional
Discord / Telegram / webhook delivery). The client pattern is generic, so you
can point it at any compatible WebSocket source.

- Binance Square monitoring (what it covers, pricing): https://1322.io/platforms/binance
- Guide: https://1322.io/blog/binance-square-api-guide
- Event schema / API docs: https://1322.io/docs

## What you get per event

Each message is a JSON object. Binance Square posts look like:

```json
{
  "platform": "binance",
  "handle": "cz_binance",
  "content": "Funding rates flipping. Stay sharp.",
  "coinPairs": ["BTCUSDT", "ETHUSDT"],
  "timestamp": "2026-06-16T12:00:00Z"
}
```

`coinPairs` is extracted for you, so you can filter straight to the tickers you
trade.

## Python

```bash
pip install websockets
API_KEY=your-key WS_URL=wss://1322.io/your-ws-path python main.py
```

## Node

```bash
npm install ws
API_KEY=your-key WS_URL=wss://1322.io/your-ws-path node index.js
```

Get an API key and your WebSocket path from the dashboard after signup
(plans from $250/mo): https://1322.io/pricing

## Why WebSocket instead of scraping or polling

Scraping the Square web app or polling an endpoint caps your worst-case latency
at the check interval and breaks whenever the page changes. A WebSocket pushes
the post the instant it is detected, which is what you want for trading,
breaking-news, and alerting. More on the trade-off:
https://1322.io/blog/binance-square-api-guide

## Related

Other real-time monitors in the same family:

- Twitter/X: https://github.com/SisoSol/twitter-websocket-client
- Truth Social: https://github.com/SisoSol/truthsocial-stream
- Instagram: https://github.com/SisoSol/instagram-realtime
- All six platforms: https://github.com/SisoSol/social-monitor-examples

MIT licensed.

## 中文

币安广场（Binance Square）没有官方的读取 API，公开的 Square 接口只能发布内容，无法监控他人帖子。常见做法是用无头浏览器定时抓取网页，速度慢且容易失效。

这个仓库提供精简的 Node 和 Python 客户端，通过 WebSocket 在帖子发布的瞬间把它推送给你，并自动解析出币种交易对（coinPairs），方便直接过滤你关注的交易对。

```bash
# Python
pip install websockets
API_KEY=你的密钥 WS_URL=wss://1322.io/你的ws路径 python main.py
```

示例运行在 [1322](https://1322.io/zh) 的托管数据流之上（同一个 WebSocket 还覆盖 X、Truth Social、Instagram、YouTube 和新闻），但客户端代码是通用的。

- 币安广场实时监控：https://1322.io/platforms/binance
- 中文总览：https://1322.io/zh
- 指南：https://1322.io/blog/binance-square-api-guide
