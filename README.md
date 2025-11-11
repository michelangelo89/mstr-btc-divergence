# 📈 MSTR–BTC Divergence Strategy  
*Mean-Reversion Model Between MicroStrategy and Bitcoin*

---

## 🧭 Overview  
This project builds a **mean-reverting trading model** between **MicroStrategy (MSTR)** and **Bitcoin (BTC)** to exploit **temporary divergences** between MSTR’s price and its BTC-implied fair value.  

MicroStrategy behaves like a **leveraged Bitcoin proxy** because it holds large BTC reserves financed via debt and equity. However, **company-specific events** (e.g., share dilutions, convertible bond issuances, or earnings surprises) often create short-term deviations from BTC performance.  
The strategy identifies and trades these divergences when they are likely to revert.

---

## 🎯 Objective  
Detect when MSTR becomes significantly **overvalued or undervalued** relative to Bitcoin and profit from the **mean-reversion** of this spread, while managing risk around major corporate events.

---

## ⚙️ Methodology

### 1. Time-Varying Regression Model  

We model **MSTR** as a leveraged function of **BTC** using log prices:

$$
\log(\text{MSTR}_t) = \alpha + \beta_t \cdot \log(\text{BTC}_t) + \epsilon_t
$$

- **βₜ** — dynamic hedge ratio (estimated via *rolling* or *exponentially weighted (EWMA)* regression on log-returns).  
- **εₜ** — residual spread representing short-term divergence.  


### 2. Mean-Reversion Logic  
- Compute **cumulative residuals** and standardize them with a **rolling z-score**.  
- Trade when spread exceeds threshold levels:  
  - **z < -Z_thr** → MSTR is cheap → *Long MSTR / Short BTC*  
  - **z > +Z_thr** → MSTR is rich → *Short MSTR / Long BTC*  
  - **Exit** when z ≈ 0  

---

## 🧩 Model Enhancements

| Feature | Description |
|----------|--------------|
| **Rolling / EWMA β** | Adapts the hedge ratio dynamically to market conditions. |
| **Event Integration** | Incorporates MSTR-specific corporate events (dilution, debt, earnings, etc.). |
| **Event Blocking** | Suspends trading during event windows to avoid structural breaks. |
| **Diagnostics** | Runs ADF test for stationarity, half-life for mean reversion speed, and JB test for normality. |
| **Backtesting Metrics** | Evaluates CAGR, volatility, Sharpe ratio, and maximum drawdown. |

---

## 📊 Data Sources

| Dataset | File Path | Description |
|----------|------------|--------------|
| **Prices** | `data/processed/prices.parquet` | Daily prices for MSTR and BTC-USD. |
| **Events** | `data/external/events_mstr.csv` | Company-specific events: ATM offerings, convertible notes, earnings reports, etc. |

---

## 🧠 Workflow Summary

1. Load and align MSTR & BTC prices.  
2. Compute log-returns and estimate β (rolling/EWMA).  
3. Build time-varying spread and rolling z-score.  
4. Import and flag event windows.  
5. Run trading simulation:
   - Baseline strategy (no event block)
   - Event-filtered strategy (avoid trading around events)
   - Compare vs BTC and MSTR buy-and-hold
6. Compute key metrics and visualize equity curves.

---

## 📈 Example Output

| Strategy | CAGR | Vol | Sharpe | MaxDD |
|-----------|------|-----|--------|--------|
| **Switch (event+beta block)** | 1.53 | 0.62 | 1.81 | -0.34 |
| **Switch (baseline)** | 1.53 | 0.62 | 1.81 | -0.34 |
| **BTC HODL** | 1.03 | 0.49 | 1.68 | -0.28 |
| **MSTR HODL** | 2.16 | 0.90 | 1.73 | -0.50 |

---

## 🚀 Roadmap

### ✅ Phase 1 — Baseline  
- Build β model (rolling & EWMA).  
- Implement spread/z-score & trading rules.  

### ✅ Phase 2 — Event Filtering  
- Add event dataset and block trades around dilution or debt events.  

### 🔜 Phase 3 — Intelligent Event Integration  
- Add **event dummies** to regression to allow α/β to shift during events.  
- Test **dual-regime β models** (normal vs event periods).  
- Explore **Bayesian or Kalman filter β updates**.  
- Add dashboard + reporting notebook.  

---

## 🧰 Tech Stack

- **Python**: pandas, numpy, statsmodels, matplotlib  
- **Data**: Yahoo Finance (via `yfinance`), SEC filings (custom event CSV)  
- **Environment**: Jupyter Notebooks + modular `src/` pipeline  
- **Versioning**: Git + `.venv` for reproducibility  

---

## 📂 Repository Structure

```
mstr-btc-divergence/
│
├── data/
│   ├── external/          # Event CSVs (dilution, debt, earnings)
│   ├── processed/         # Clean prices / merged data
│   └── raw/               # Yahoo Finance downloads
│
├── notebooks/
│   └── 01_eda_prices.ipynb     # Core notebook for exploration and backtests
│
├── src/
│   ├── events.py               # Event handling and mapping
│   ├── data_store.py           # Price loading and caching
│   ├── update_prices.py        # Daily price updates
│   ├── utils.py                # Statistical tools and diagnostics
│   └── fetch_events_edgar.py   # (Optional) SEC event scraper
│
└── README.md
```

---

## 🧩 Next Steps (Ideas)
- Introduce **event-conditioned β** (different coefficients during event windows).  
- Build **Bayesian β updater** for smoother transitions.  
- Use **weighted spread** correcting for event size (e.g., dilution %).  
- Create **Prefect / MLflow pipeline** for automated recalibration.  
- Optional: backtest extensions with **short-term sentiment / flow data**.

---

## 👤 Author  
**Michelangelo D’Alessandro**  
*Data Scientist — London*  
Focus areas: financial modeling, MLOps, and adaptive trading systems.  
