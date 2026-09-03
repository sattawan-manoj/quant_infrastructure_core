# 🏛️ IIT-Bombay Balanced Quant Research Apprenticeship
### 📋 Programmatic Masterplan Specification (Days 1–120)

This repository contains my step-by-step implementation of the 120-day institutional-grade algorithmic trading and quantitative research framework. Built entirely from scratch with zero initial coding background, focusing on data isolation, mathematical calibration, and fail-safe production architectures.

---

## 🚀 Operational Architecture Checklist (End-to-End Control Ledger)

| Runtime Risk Factor Matrix | Target System Metric Threshold | Core Implementation Status |
| :--- | :--- | :--- |
| **Data Loop Ingestion Bias** | 20% Absolute Untouched Holdout | 🛡️ Shield Deployed (Day 31 Base) |
| **Matrix Inversion Breakdown** | Near-Singular Data Matrix Filter | ⚙️ Moore-Penrose Pseudoinverse Active |
| **Kalman Covariance Explosion** | Tukey's Fences 1.5x IQR Rule | 📊 Dynamic Bounding Active |
| **WebSocket Stream Hangs** | Asynchronous Backoff Daemon | 🔄 Persistent Reconnect Engaged |
| **Server Memory Overflow** | Graceful Persistence Writing (>80%) | 💾 Auto-Telemetry Cache Deployed |
| **Crash Recovery Execution** | Post-Crash Position Harmonization | 🔌 Reconciliation Daemon Active |

---

## 📅 Apprenticeship Progression Ledger (Days 1-120)

### 📦 Month 1: Architecture Isolation & Probability Foundations (Days 1–30)
*Target Milestone: Establish unshakeable probability intuition, map native data structures, and isolate ingestion pipelines.*

- [x] **Week 1: Python Scoping, Memory Structures, & NumPy Arrays Engine Core**
  - *Day 1 - 7*: Mastered C-contiguous array allocations, vectorization layout blocks, and coded algebraic statistical moments from raw math without `.mean()` or `.var()` shortcuts. (`raw_moments.py`)
- [x] **Week 2: Core Probability Chain & Hypothesis Inference**
  - *Day 8 - 10*: Implemented continuous random variables expectation, Skewness, Excess Kurtosis indices, and multi-variable Joint Space Covariance metrics from scratch.
  - *Day 11 (Today)*: **The Central Limit Theorem Simulation Engine** -> Built an Object-Oriented, production-grade simulation sampling 5,000 independent chunks from highly skewed non-Gaussian paths to empirically verify convergence into a perfect Gaussian Bell Curve. (`clt_simulation.py`)
- [ ] **Week 3: Clean Ingestion Engines & Storage Cache Layers**
  - *Day 15 - 21*: *[Upcoming]* Architectural decoupling of data feeds, Polars DataFrame schema locks, datetime alignments, and Snappy compressed binary Parquet serialization.
- [ ] **Week 4: Survivorship Bias & Look-Ahead Isolation Shields**
  - *Day 22 - 30*: *[Upcoming]* Explicit ingestion of delisted assets and hardcoded Shift-1 look-ahead information leakage guardrails.

---

### 📐 Month 2: Dynamic Estimation Math & Component Design (Days 31–60)
*Target Milestone: Deploy stable matrix pseudoinversions with condition filtering and calibrate state-space Kalman filters.*
- [ ] **Week 5 & 6**: In-Sample 80/20 Data Partitioning Vault & Matrix Condition Number Filtering (`linear_regress_engine.py`).
- [ ] **Week 7 & 8**: Expectation-Maximization Noise Calibration & Tukey's Fences Bounding Matrix Protection (`kalman_filter_engine.py`).

---

### 🚫 Month 3: Alpha Falsification & True Rolling Backtesters (Days 61–90)
*Target Milestone: Enforce FDR multiple-testing filters to block selection bias and deploy sliding-window walk-forward simulations.*
- [ ] **Week 9 & 10**: Benjamini-Hochberg False Discovery Rate (FDR) Screening Controls (`selection_bias_shield.py`).
- [ ] **Week 11 & 12**: True Rolling Walk-Forward Backtest Simulator Engine (`vectorized_backtester.py`).

---

### 💸 Month 4: Microstructure Cost Accounting & Headless VPS Operations (Days 91–120)
*Target Milestone: Quantify realized friction drag, pass the holdout test gate, and activate persistent server daemons.*
- [ ] **Week 13**: Volatility-Adjusted Realized Friction, Latency Penalties, and Bid/Ask Consumption Models.
- [ ] **Week 14**: Exhaustive Strategy Selection Audits over 20% Absolute Untouched Holdout Database (`strategy_auditor.py`).
- [ ] **Week 15 & 16 (Extended)**: Headless Oracle/AWS Cloud VPS Deployment, Token Vaults, Chrony NTP Time Sync, Async WebSocket Daemons, Process Watchdogs, and Post-Crash Position Reconciliation (`reconciliation_daemon.py`).

---

## 🛠️ Local Environment & Dependencies
This environment is optimized for Ubuntu/Linux structures to avoid system dependency breakdown:
```bash
sudo apt update && sudo apt install python3-matplotlib python3-numpy -y
```

