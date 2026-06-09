# Binance Futures Testnet Trading Bot

A simple Python-based trading bot for placing MARKET and LIMIT orders on Binance Futures Testnet (USDT-M).

---

# Features

✅ Place MARKET Orders  
✅ Place LIMIT Orders  
✅ BUY and SELL Support  
✅ CLI-Based Input  
✅ Input Validation  
✅ Logging System  
✅ Error Handling  
✅ Binance Futures Testnet Integration  

---

# Tech Stack

- Python 3.x
- Binance API
- python-binance
- argparse
- logging
- dotenv

---

# Project Structure

```bash
trading_bot/
│
├── bot/
│   ├── __init__.py
│   ├── client.py
│   ├── orders.py
│   ├── validators.py
│   └── logging_config.py
│
├── logs/
│   └── trading.log
│
├── cli.py
├── requirements.txt
├── README.md
└── .env
