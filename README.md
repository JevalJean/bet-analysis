# 📈 Sports Betting Arbitrage & Value Betting Bot

## 🎯 Overview
This Python project is an automated Value Betting scanner. It leverages real-time sports odds data to identify mathematically profitable betting opportunities (Expected Value > 0) across global bookmakers. 

Instead of relying on luck, this algorithm acts as a quantitative trading bot for sports markets. It calculates the true probability of an event using the "Wisdom of the Crowds" (market median) and applies strict bankroll management to recommend optimal bet sizing.

## 🚀 Key Features
* **Real-Time Data Extraction:** Connects to *The Odds API* to fetch live odds from dozens of bookmakers simultaneously.
* **The "Oracle" Model:** Calculates the true probability of an outcome by computing the median odds of the global market, effectively neutralizing individual bookmaker biases.
* **Expected Value (EV) Calculator:** Automatically flags bets where the implied probability offered by a specific bookmaker is lower than the calculated true probability.
* **Risk Management (Kelly Criterion):** Implements the "Quarter Kelly" formula to dynamically calculate the exact dollar amount to wager based on the total bankroll, the edge, and the odds, preventing mathematical ruin.

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **Libraries:** `requests` (API calls), `statistics` (Data analysis), `dotenv` (Environment variables management).
* **Architecture:** Procedural scripting, REST API integration, JSON data parsing.

## ⚠️ Disclaimer
This code is for educational and portfolio purposes only. It demonstrates API integration, data cleaning, and applied mathematics (statistics & probability). It is not financial advice.
