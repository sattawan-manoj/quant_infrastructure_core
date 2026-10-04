# Quant Infrastructure Core

### Quantitative Research & Computational Infrastructure

A modular Python research codebase for implementing, analysing, and validating computational methods used in quantitative research.

The repository focuses on the intersection of **statistical modelling, numerical computing, time-series analysis, regression, dynamic state estimation, and quantitative model validation**.

The objective is to build reusable computational components that can be combined into coherent quantitative research workflows.

---

## Research Capabilities

The codebase covers the following areas:

- Statistical computation
- Probability and distribution analysis
- Statistical moments
- Monte Carlo simulation
- Regression and parameter estimation
- Time-series analysis
- Stationarity testing
- Residual analysis
- State-space modelling
- Kalman filtering
- Dynamic parameter estimation
- Parameter calibration
- Robust statistical bounds
- Model diagnostics
- Numerical and statistical validation

---

## System Architecture

```text
                         QUANT INFRASTRUCTURE CORE
                                  │
          ┌───────────────────────┼───────────────────────┐
          │                       │                       │
          ▼                       ▼                       ▼
   Numerical Computing     Statistical Analysis     Time-Series Analysis
          │                       │                       │
          │              ┌────────┴────────┐              │
          │              │                 │              │
          ▼              ▼                 ▼              ▼
      NumPy          Moments        Distributions    Diagnostics
          │              │                 │              │
          └──────────────┴─────────────────┴──────────────┘
                                  │
                                  ▼
                         Regression Engine
                                  │
                                  ▼
                       State-Space Modelling
                                  │
                                  ▼
                         Kalman Filter Engine
                                  │
                    ┌─────────────┴─────────────┐
                    ▼                           ▼
             Parameter Calibration       Robust Boundaries
                    │                           │
                    └─────────────┬─────────────┘
                                  ▼
                       Residual / Innovation
                              Analysis
                                  │
                                  ▼
                         Research Validation
```

---

## Core Research Components

### Statistical & Numerical Foundations

Computational implementations for statistical moments, distributions, sampling behaviour, and numerical experimentation.

The implementations translate mathematical definitions into explicit numerical procedures using array-oriented computation.

### Monte Carlo Simulation

Simulation-based analysis for examining sampling behaviour, empirical distributions, convergence, and statistical properties through repeated numerical experiments.

### Regression & Parameter Estimation

Modular regression components for estimating relationships between variables and extracting model parameters for subsequent quantitative analysis.

### Time-Series Analysis

Time-series components for analysing sequential observations, testing statistical properties, and evaluating model residual behaviour.

Statistical diagnostics are used as part of the broader model-validation process.

### State-Space Modelling

The codebase implements state-space concepts for representing systems in which underlying states evolve dynamically and observations contain noise.

```text
Latent State
     │
     ▼
State Transition
     │
     ▼
Observation Process
     │
     ▼
Observed Data
```

### Kalman Filtering

Dynamic state estimation using the Kalman filtering framework.

The implementation separates the two fundamental stages:

```text
Prediction
    │
    ▼
Predicted State
    │
    ▼
Measurement Update
    │
    ▼
Updated State Estimate
```

This provides a foundation for estimating evolving latent states and parameters from noisy observations.

### Parameter Calibration

Parameter-calibration components provide a mechanism for estimating model parameters from historical observations before applying dynamic estimation procedures.

This separates **parameter estimation** from **state estimation**, allowing the two stages to be analysed independently.

### Robust Parameter Control

Historical parameter estimates can be evaluated statistically to identify abnormal observations and unstable parameter behaviour.

The repository includes robust boundary construction using Tukey's IQR methodology:

```text
Q1 ───────────────── Q2 ───────────────── Q3
│                                         │
└──────────── IQR = Q3 − Q1 ──────────────┘

Lower Bound = Q1 − 1.5 × IQR
Upper Bound = Q3 + 1.5 × IQR
```

This provides a transparent statistical mechanism for identifying extreme parameter values.

### Residual & Innovation Analysis

Residuals and innovations are evaluated as part of model diagnostics.

The objective is to examine the unexplained component of the model and assess whether observed behaviour is consistent with the assumptions of the underlying estimation framework.

---

## Integrated Quantitative Workflow

The components can be combined into an end-to-end research workflow:

```text
Raw Observations
       │
       ▼
Data Preparation
       │
       ▼
Statistical Diagnostics
       │
       ▼
Regression / Parameter Estimation
       │
       ▼
Time-Series Analysis
       │
       ▼
State-Space Representation
       │
       ▼
Kalman Filtering
       │
       ▼
Parameter Calibration
       │
       ▼
Robust Parameter Boundaries
       │
       ▼
Residual / Innovation Analysis
       │
       ▼
Model Validation
       │
       ▼
Research Output
```

The architecture keeps **estimation, calibration, robustness, and validation** as distinguishable computational stages rather than combining them into a single monolithic implementation.

---

## Engineering Approach

### Modular Design

Research components are implemented as independent modules so that individual algorithms can be inspected, tested, and reused.

### Mathematical Traceability

The computational implementation is designed to maintain a clear relationship between the mathematical formulation and the corresponding numerical operations.

### Numerical Discipline

The implementation considers:

- Array dimensions and shapes
- Numerical transformations
- Parameter constraints
- Statistical assumptions
- Numerical stability
- Edge cases
- Invalid or extreme parameter behaviour

### Statistical Validation

Successful execution is not treated as sufficient evidence of correctness.

Outputs are evaluated through statistical diagnostics, residual behaviour, parameter distributions, and consistency checks.

### Reproducible Research

The repository is structured to support repeatable computational experiments and transparent inspection of the underlying methodology.

---

## Technology Stack

```text
Python
├── NumPy
├── SciPy
├── Statsmodels
├── PyKalman
└── Matplotlib
```

---

## Repository Structure

```text
quant_infrastructure_core/
│
├── raw_moments.py
├── clt_simulation.py
├── linear_regress_engine.py
├── kalman_filter_engine.py
├── ...
│
└── README.md
```

The repository structure evolves as additional quantitative research components are integrated.

---

## Research Focus

The codebase is being developed around a layered quantitative research architecture:

```text
Mathematical Foundations
          ↓
Statistical Computation
          ↓
Numerical Algorithms
          ↓
Regression & Modelling
          ↓
Time-Series Analysis
          ↓
Dynamic State Estimation
          ↓
Parameter Calibration
          ↓
Robustness
          ↓
Model Validation
          ↓
Quantitative Research Infrastructure
```

The long-term direction is to connect these components into reusable research systems for quantitative modelling, statistical experimentation, and systematic analysis.

---

## Status

**Active Quantitative Research & Engineering Project**

The repository is continuously evolving through the integration of additional computational models, statistical diagnostics, estimation methods, and validation components.