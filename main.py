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
        hist = stock.history(period="1mo", interval="1d")
        if hist.empty:
            return {"error": "No data found"}
        
        return {
            "dates": hist.index.strftime("%Y-%m-%d").tolist(),
            "prices": hist["Close"].fillna(0).round(2).tolist()
        }
    except Exception as e:
        return {"error": str(e)}
