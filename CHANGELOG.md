# CHANGELOG

All notable changes to AI Hedge Fund project.

## [2.3.0] - 2026-01-19

### AGENTS.md Complete Integration

#### New Features
- **Agent Constitution Integration** (from `/home/mulky/Desktop/aturan agent.txt`)
  - Meta-Prinsip Agent (6 prinsip tertinggi)
  - Definisi & Tipe Agent (6 tipe: Core, Planner, Worker, Auditor, Archivist, Sentinel)
  - Hak, Batasan & Zona Kritikal
  - Siklus Kerja Agent (Lifecycle) - Bootstrap → Analisis → Perencanaan → Eksekusi → Validasi → Dokumentasi
  - Mode Operasi Agent (Normal, Audit, Lock, Recovery)
  - Sistem Session & Export (JSON, Markdown, TXT)
  - Logging & Audit System
  - Manajemen Konflik & Penyimpangan
  - Prinsip Berpikir Agent (Data > asumsi, Logika > opini)
  - Etika Kerja Agent
  - Janji Agent (7 janji untuk hedge fund)
  - Checklist Aksi Besar
  - Protokol "If in Doubt"

#### Enhancements
- **Complete AGENTS.md Rewrite** (23 sections, ~2,300 lines)
- All content in Indonesian language
- Merged existing AGENTS.md content with new agent constitution
- Updated version to 2.3.0
- Structured table of contents for easy navigation
- Complete file inventory updated (~10,000 files)
- Protocol for working with messy codebase
- Backup & Cleanup rules standardized

#### Documentation
- Single Source of Truth untuk semua agent
- Comprehensive agent lifecycle documented
- Conflict resolution protocols added
- Session export format standardized

## [2.2.2] - 2026-01-18

### RISET v2.2.2 Full Integration

#### New Features
- **RISET v2.2.2 Complete Integration**
  - Graham Value Investing Strategy (Benjamin Graham principles)
  - Turtle Trading Strategy (Richard Dennis system)
  - SEPA Strategy (Super Performance, CANSLIM, VCP)
  - Kelly Criterion Position Sizing
  - Risk Parity Portfolio Optimization
  - Value at Risk (VaR) - Parametric, Historical, Monte Carlo
  - VectorBT Backtesting Engine
  - Unified Strategy Orchestrator
  - Multi-Agent System (MAS) - 4 specialized agents
  - LLM7 API Client Integration

- **Comprehensive Test Suite** (29/31 tests passing)
  - Integration tests for all RISET components
  - Automated test result reporting
  - Performance metrics validation

- **System Integration**
  - RISET Integrator module (`src/integration/riset_integrator.py`)
  - Unified connection of all strategies, risk managers, and agents
  - Comprehensive backtesting script (`tests/comprehensive_backtest.py`)
  - Main menu updated with RISET strategy options

#### Bug Fixes
- Fixed Parabolic SAR implementation (`src/indicators/technical_indicators.py`)
  - Changed from pandas Series to numpy arrays to fix assignment error
  - Line 359-423: Fixed "setting an array element with a sequence" error
- Fixed Parametric VaR formula (`src/risk/var.py`)
  - Corrected mathematical formula for VaR calculation
  - Added `_calculate_expected_shortfall()` helper method
  - Line 108-175: Fixed math domain errors and incorrect formula
- Fixed MAS Orchestrator initialization test (now uses `create_mas()` function)
- Fixed AgentConfig attributes (uses `agent_type` instead of `role`, etc.)
- Fixed message queue assertion (uses `len()` instead of `qsize()`)
- Fixed CANSLIM score attribute (`total_score` instead of `total`)
- Fixed Kelly Method enum values (`FULL_KELLY`, `HALF_KELLY`, `ADAPTIVE_KELLY`)
- Fixed Monte Carlo VaR implementation (fixed `np.random.normal()` parameters)
- Fixed Risk Parity weights assertion (uses `sum(weights.values())`)
- Removed invalid logger attribute checks from strategy tests

#### Enhancements
- Main.py version updated to 2.2.2
- Feature version updated to "RISET - Full Integration"
- New menu options (11-17) for RISET strategies and tools
- Graham Value Strategy interactive analysis
- Turtle Trading Strategy interactive analysis
- SEPA Strategy interactive analysis
- RISET Comprehensive Backtesting with report generation
- RISET System Integration status display

#### Testing Results (2026-01-18 Session)
- **26/26 Indicator Tests PASSING** (100%)
- **29/31 Integration Tests PASSING** (93.5%)
  - 2 VectorBT tests skipped (optional dependency)
- **53/53 Strategies Registered** ✅
- **All Risk Modules VERIFIED** ✅
- **Data Providers: All Working** ✅
- **Core Utilities: All Working** ✅

#### Verified Modules
- Technical Indicators (RSI, MACD, BB, Stochastic, ATR, ADX, CCI, etc.)
- Risk Management (VaR, Kelly Criterion, Risk Parity)
- Backtesting Engine (Controller, Engine, Metrics, Portfolio)
- Strategy Registry (53 strategies across 9 categories)
- Data Providers (Enhanced, Free, Financial Datasets)
- Tools API (get_prices, get_financial_metrics)
- Automation & Modes (AIAutoTrader, ExecutionController)
- Analysis (Multi-Timeframe Analyzer)

## [2.2.1] - 2026-01-17

### Enhanced Data & LLM7

#### New Features
- **LLM7 Integration**
  - Primary LLM: gpt-5-nano
  - Fallback LLMs: OpenRouter, Groq, Gemini
  - Streaming support
  - Function calling support
  - Chat history management

- **Enhanced Free Data Provider**
  - Financial Datasets API (primary)
  - Yahoo Finance (fallback)
  - CoinGecko (crypto fallback)
  - ExchangeRate-API (forex fallback)
  - IDX Stock Data (Indonesian stocks)

## [2.1.0] - 2026-01-16

### Base Foundation

#### Initial Features
- Core trading system architecture
- 34+ Trading Strategies
- 3-Mode Operation (Manual, Semi-Auto, Full-Auto)
- Multi-Asset Support
- Memory System (SQLite + JSON)
- Paper Trading
- MetaTrader Browser Bridge
- Streamlit Dashboard
- CLI Terminal
- Auto-Heal System
