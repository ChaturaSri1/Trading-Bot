Got it — here’s a clean, professional **rewritten `README.md`** that matches what reviewers want to see. You can replace your current file with this word-for-word 👇

---

## ✅ New `README.md`

```markdown
# Binance Futures Testnet Trading Bot

A lightweight Python CLI application for placing MARKET and LIMIT orders on **Binance Futures Testnet (USDT-M)** with structured architecture, logging, and error handling.

---

## Features

- Place **MARKET** and **LIMIT** orders  
- Supports **BUY / SELL** sides  
- CLI input validation  
- Automatic leverage initialization  
- Detailed logging of API requests and responses  
- Graceful handling of:
  - invalid input  
  - network failures  
  - Binance API errors

---

## Project Structure

```

trading_bot/
│
├── bot/
│   ├── client.py        # Binance REST API wrapper
│   ├── orders.py        # Order placement logic
│   ├── validators.py    # CLI input validation
│   └── logging_config.py
│
├── cli.py               # CLI entry point
├── requirements.txt
├── README.md
└── logs/
└── bot.log          # Execution logs

````

---

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
````

### 2. Configure environment variables

Windows (PowerShell):

```powershell
$env:BINANCE_API_KEY="your_key"
$env:BINANCE_API_SECRET="your_secret"
```

Linux / Mac:

```bash
export BINANCE_API_KEY="your_key"
export BINANCE_API_SECRET="your_secret"
```

---

## Usage Examples

### MARKET Order

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.003
```

### LIMIT Order

```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.003 --price 90000
```

---

## Logging

* All API requests and responses are written to:

```
logs/bot.log
```

* Errors are captured with full stack traces
* Signatures are excluded from logs for security

---

## Assumptions & Notes

* The application targets **Binance Futures Testnet (USDT-M)**
* Minimum notional on Testnet is **100 USDT**
* Fresh accounts require leverage to be set before first trade
* The client automatically sets leverage to **10x** to prevent `-2019 margin insufficient` errors
* LIMIT orders use **GTC** time in force

---

## Requirements

* Python 3.x
* requests

See `requirements.txt`

---

## Error Handling

The bot handles:

* Invalid CLI parameters
* Missing environment variables
* Network failures
* Binance API errors with descriptive messages

---

## Sample Log Evidence

The `logs/bot.log` file contains:

* One successful MARKET order
* One successful LIMIT order
* Full request/response details

---

## Future Improvements (Optional)

* Balance check before order
* Additional order types (Stop-Limit / OCO)
* Unit tests with mocked API
* Enhanced CLI UX

```

---

If you want, I can also:

👉 add a tiny **SECURITY section**  
👉 add a **How reviewers can test quickly** part  
👉 generate a polished GitHub repo description

Just tell me:

> “add security section”

and I’ll upgrade it 💪
```