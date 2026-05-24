# Dependencies

## 📦 Core Dependencies

All dependencies are managed by **Poetry**. Install with:

```bash
poetry install
```

Or view/add dependencies in `pyproject.toml`.

---

## 🐍 Python Requirements

```
python >= 3.11
```

---

## 📥 Production Dependencies

### AI & LLM

| Package | Version | Purpose | Source |
|---------|---------|---------|--------|
| `langchain` | ^0.3.7 | AI framework | PyPI |
| `langgraph` | ^0.2.56 | Agent workflow | PyPI |
| `langchain-anthropic` | 0.3.5 | Anthropic Claude | PyPI |
| `langchain-openai` | ^0.3.5 | OpenAI GPT | PyPI |
| `langchain-groq` | ^0.2.3 | Groq API | PyPI |
| `langchain-deepseek` | ^0.1.2 | DeepSeek | PyPI |
| `langchain-ollama` | 0.3.6 | Ollama local | PyPI |
| `langchain-google-genai` | ^2.0.11 | Google Gemini | PyPI |
| `langchain-xai` | ^0.2.5 | xAI Grok | PyPI |
| `langchain-gigachat` | ^0.3.12 | GigaChat | PyPI |

### Data & Finance

| Package | Version | Purpose | Source |
|---------|---------|---------|--------|
| `yfinance` | ^1.0 | Stock data (Yahoo) | PyPI |
| `pandas` | ^2.1.0 | Data manipulation | PyPI |
| `numpy` | ^1.24.0 | Numerical computing | PyPI |
| `requests` | - | HTTP requests | PyPI |
| `httpx` | ^0.27.0 | Async HTTP | PyPI |

### CLI & UI

| Package | Version | Purpose | Source |
|---------|---------|---------|--------|
| `questionary` | ^2.1.0 | Interactive prompts | PyPI |
| `colorama` | ^0.4.6 | Terminal colors | PyPI |
| `rich` | ^13.9.4 | Rich text/tables | PyPI |
| `tabulate` | ^0.9.0 | Table formatting | PyPI |

### Web & API

| Package | Version | Purpose | Source |
|---------|---------|---------|--------|
| `fastapi` | ^0.104.0 | Web framework | PyPI |
| `pydantic` | ^2.4.2 | Data validation | PyPI |
| `sqlalchemy` | ^2.0.22 | Database ORM | PyPI |
| `alembic` | ^1.12.0 | Database migration | PyPI |

### Visualization

| Package | Version | Purpose | Source |
|---------|---------|---------|--------|
| `matplotlib` | ^3.9.2 | Plotting/charts | PyPI |

---

## 🛠️ Development Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `pytest` | ^7.4.0 | Testing |
| `black` | ^23.7.0 | Code formatting |
| `isort` | ^5.12.0 | Import sorting |
| `flake8` | ^6.1.0 | Linting |

---

## 🔧 Installation

### Option 1: Poetry (Recommended)

```bash
# Install Poetry if not installed
curl -sSL https://install.python-poetry.org | python3 -

# Navigate to project
cd /home/mulky/ai-hedge-fund

# Install all dependencies
poetry install

# Activate virtual environment
poetry shell

# Run the application
python launcher.py
```

### Option 2: pip

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -e .

# Run
python launcher.py
```

---

## 📦 Add New Dependency

```bash
# Add production dependency
poetry add package_name

# Add development dependency
poetry add --group dev package_name

# Update lock file
poetry lock

# Update all dependencies
poetry update
```

---

## 🐳 Docker (Optional)

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY pyproject.toml .
RUN pip install poetry && poetry config virtualenvs.in-project true
COPY . .
RUN poetry install --no-interaction

CMD ["python", "launcher.py"]
```

---

## 🔍 Environment Variables

Create `.env` file:

```env
# LLM APIs (if using paid services)
OPENAI_API_KEY=your-key
GROQ_API_KEY=your-key
GOOGLE_API_KEY=your-key

# Data APIs (if using paid services)
FINANCIAL_DATASETS_API_KEY=your-key

# Configuration
OPENCODE_NO_INTERACTION=1
```

**Note**: Core functionality works WITHOUT any API keys!

---

## 📊 Dependency Tree

```
ai-hedge-fund
├── langchain
│   ├── pydantic
│   ├── requests
│   └── langchain-core
├── langgraph
│   └── langchain-core
├── yfinance
│   ├── pandas
│   └── requests
├── fastapi
│   ├── pydantic
│   └── starlette
├── questionary
│   └── prompt_toolkit
└── colorama
```

---

## 🚨 Troubleshooting

### Installation Fails

```bash
# Clear cache and retry
pip cache purge
poetry clear
poetry install
```

### Missing Dependencies

```bash
# Reinstall all dependencies
poetry install --no-deps
poetry install
```

### Version Conflicts

```bash
# Update lock file
poetry lock --no-update

# Or update specific package
poetry update package_name
```

---

## ✅ Verified Working Versions

```bash
# Python
Python 3.11.x

# Key packages (verified 2026-01-14)
langchain == 0.3.x
langgraph == 0.2.x
yfinance == 1.0.x
poetry == 1.x
```

---

## 📝 Notes

1. **yfinance** is the primary data source for stocks - no API key needed
2. **OpenCode CLI** handles LLM - no API key needed  
3. **exchangerate-api** provides forex - no API key needed
4. **CoinGecko** provides crypto data - no API key needed (rate limited)

This project is designed to work with **ZERO** paid API subscriptions!

---

> **Contact:** Mulky Malikul Dhaher — [mulkymalikuldhaher@email.com](mailto:mulkymalikuldhaher@email.com)
>
> **Disclaimer:** This project is for Education Purpose only. Risiko apapun tidak kita tanggung. (We are not responsible for any risks or damages.)
