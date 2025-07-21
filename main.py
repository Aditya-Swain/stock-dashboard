from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/stock/{symbol}")
def get_stock(symbol: str):
    try:
        stock = yf.Ticker(symbol)

        # Historical prices for chart (1 month)
        hist = stock.history(period="1mo", interval="1d")
        if hist.empty:
            return {"error": "No data found"}

        # 52-week data
        full_hist = stock.history(period="1y")
        week_52_high = round(full_hist['High'].max(), 2)
        week_52_low = round(full_hist['Low'].min(), 2)

        # Average volume (last 30 days)
        avg_volume = round(hist['Volume'].mean(), 2)

        # Technical indicators - 20-day and 50-day moving average
        moving_avg_20 = round(hist['Close'].rolling(window=20).mean().iloc[-1], 2)
        

        return {
            "dates": hist.index.strftime("%Y-%m-%d").tolist(),
            "prices": hist["Close"].fillna(0).round(2).tolist(),
            "52_week_high": week_52_high,
            "52_week_low": week_52_low,
            "avg_volume": avg_volume,
            "ma_20": moving_avg_20,
            
        }

    except Exception as e:
        return {"error": str(e)}
