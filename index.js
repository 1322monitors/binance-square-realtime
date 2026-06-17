// Real-time Binance Square monitor over WebSocket (Node).
// Streams new Binance Square posts (with coin pairs) as they publish.
// Set API_KEY and WS_URL from your 1322 dashboard. See README for details.

const WebSocket = require("ws")

const API_KEY = process.env.API_KEY
const WS_URL = process.env.WS_URL

if (!API_KEY || !WS_URL) {
  console.error("set API_KEY and WS_URL (see README)")
  process.exit(1)
}

function connect() {
  const ws = new WebSocket(WS_URL, { headers: { "X-Api-Key": API_KEY } })

  ws.on("open", () => console.log("connected: binance square feed"))

  ws.on("message", (raw) => {
    let event
    try {
      event = JSON.parse(raw)
    } catch {
      return
    }
    if (event.platform !== "binance") return
    const pairs = (event.coinPairs || []).join(",")
    console.log(`[${event.timestamp || ""}] @${event.handle || "?"} [${pairs}]: ${event.content || ""}`)
  })

  ws.on("close", () => {
    console.log("disconnected; reconnecting in 1s")
    setTimeout(connect, 1000)
  })

  ws.on("error", (err) => {
    console.log(`error (${err.message}); closing`)
    ws.close()
  })
}

connect()
