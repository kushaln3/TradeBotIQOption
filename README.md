# Binary Options Algorithmic Trading Bot & Simulation Engine

### A Python-based AlgoTrading bot and a backtesting and execution framework to optimize a custom capital-recovery strategy.

---

## Overview
This project is a quantitative analysis and automation tool built to test and deploy a **Custom Capital Recovery Strategy**.

Initially conceptualized based on a manual trading strategy proposed by my father, I sought to automate the execution to execute trades with high frequency and to remove emotional bias and latency. However, I quickly realized that the strategy carried inherent mathematical risks. To address this, I built a **Python Simulation Engine** to backtest lakhs of trade sequences, allowing me to mathematically tune the parameters for profitability before risking real capital.

---

### Understanding Binary Options (1-Minute Timeframe)
Binary options are financial estimates based on a simple "Yes/No" proposition. In the **1-minute timeframe** utilized by this project, the prediction focuses strictly on where the asset price (e.g., EUR/USD) will be exactly 60 seconds after the trade is executed.
* **Call (High):** Predicting the price will end *higher* than the entry point.
* **Put (Low):** Predicting the price will end *lower* than the entry point.
* **Outcome:** A correct prediction returns the investment plus a fixed payout percentage (typically 70%–90%). An incorrect prediction results in the loss of the trade amount.

---

## ⚙️ The Algorithm (My own Logic)

The core logic is a variation of a **Cost-Averaging/Recovery System** based on trade chains.

### ⛓️ The Trade Chain & Simple example
The strategy relies on a concept called the **Continuous Trade Chain**.
For simplified understanding, let us assume our return rate is 100%
>The chain starts with a base trade of suppose 1$ if the result is profit the chain is ended and a new chain starts.
>If a loss occurs, we double the trade amount $2 in the next trade, if this also suffers a loss, we continue applying the same logic.

So at any general trade, our lost amount will be 1+2+4+8...2^n and the final trade would be yielding a profit of 2^n+1
as 2^n+1 > 1+2+4+8...2^n, we get a net profit.

The logic suggests that by "going on" indefinitely, the bot maximizes the volume of trades, allowing probability to play out over time rather than relying on a single lucky guess.




### 1. The Core Equation
In a specific "Trade Chain," if a trade results in a loss, the subsequent trade's stake ($S_{next}$) is multiplied by a factor ($k$) to ensure that a single win recovers all previous losses in the chain plus a target profit.(Her instead of doubling we multiply the trade amount by k, and also consider payout rate not = 100%)

$$S_{next} = S_{current} \times k$$

*Where k is optimized to cover the broker's payout ratio.*



### 2. The Loop
1.  **Entry:** Trigger a trade based on signal.(I just took random call and put signals as we  had no aim of predicting.)
2.  **Win:** Reset stake to Base Amount ($S_{base}$).
3.  **Loss:** Multiply stake by $k$ and immediately re-enter.
4.  **Stop:** If the chain length exceeds $N$ trades (Stop Loss), reset to $S_{base}$ to preserve remaining capital.

---

## 🔧 Engineering Challenges & Solutions

### Challenge 1: The "Infinite Capital" Fallacy
**Problem:** The strategy theoretically guarantees a win *eventually*, but it requires infinite capital. In reality, an exponential growth of stakes ($S \times k^n$) quickly hits the account balance limit or the broker's maximum bet limit.
**My Observation:** I noticed that while the probability of winning *eventually* is 100%, the probability of *ruin* (losing the entire account) increases drastically with chain length.

### Challenge 2: Parameter Optimization
**Problem:** Picking arbitrary values for $k$ (multiplier) and $N$ (Stop Loss limit) was like gambling, not a probabilistic approach.
**Solution (The Simulation Engine):**
* I wrote a Python script using the `random` module to simulate millions of trade outcomes based on the broker's win/loss probability (i took approx. 50/50).
* **Optimization:** The engine tested various combinations of $k$ and $N$.
* **Result:** I tried to identify the "Sweet Spot"—a specific Stop Loss limit that maximized the probability of net profit while keeping the risk of "Account Blowout" statistically low (e.g., $< 1\%$).

---

## 📂 Verification & Data
I had tested my bot for around 3 days (1400 trades) continuosly before the optimization, and the results were quite astonishing, I started out with a $10,000 dummy account in IQOption with 1$ trades and then switched to $10 trades, I hit a max account balance of $33,000. But as I said, with upsides come downsides too, after the third day, I hit a tragic 8 continuos loss chain which ate up all my money. I had stopped working on it since then, but plan to continue to do so: To optimize the stop loss and k. 
I have included the raw trading history export from my IQOption account to demonstrate the real-world application of this logic.
* 📄 **View History:** [/trade_history/trading_history.html](https://kushaln3.github.io/TradeBotIQOption/trade_history/trading_history.html)

* I lost my Tradebot code which i initially used in my laptop hard drive failure. Bu t I have included the simulation engine jupyter notebook and trade history

---

## 🛠️ Tech Stack
* **Python** (Simulation & Logic)
* **IQOption API** (Execution Interface)
* **Statistical Analysis** (Probability tuning)

---

## 📝 Disclaimer
*This project was developed for educational and research purposes. Binary Options trading carries a high level of risk, and this code is not financial advice.*

---
