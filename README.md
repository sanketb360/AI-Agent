# AI Upskill Project

**Multi-agent news aggregation system with MCP integration**

A production-ready AI agent pipeline that fetches, filters, summarizes, and writes AI/ML news newsletters.

## Features

- 🚀 **Async News Fetching** from multiple sources (HackerNews, RSS)
- 🤖 **AI-Powered Filtering** via LiteLLM (default: Claude Haiku 4.5; swap providers via env var)
- 🔧 **MCP Integration** with reusable tools
- 📝 **Multi-Agent Pipeline** (Filter → Summarize → Write)
- 💾 **SQLite Database** for article storage
- 📊 **Evaluation Framework** for quality measurement
- ✅ **60%+ Test Coverage**

## Quick Start

### Prerequisites

- Python 3.11+
- One LLM provider API key (Anthropic recommended; OpenAI, Gemini, or any other [LiteLLM-supported provider](https://docs.litellm.ai/docs/providers) also works)

### Installation

```bash
# Clone repo
git clone https://github.com/BLEND360/AIUpskillProject.git
cd AIUpskillProject

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your provider API key