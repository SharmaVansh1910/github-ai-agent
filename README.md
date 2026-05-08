# 🤖 GitHub AI Agent

An AI-powered GitHub assistant built with **Gemini + MCP (Model Context Protocol)**.
Chat naturally with your GitHub repositories, issues, and PRs.

## 🛠️ Tech Stack

- **LLM:** Google Gemini 2.0 Flash
- **Agent Framework:** MCP (Model Context Protocol)
- **GitHub Integration:** GitHub REST API
- **UI:** Streamlit + CLI
- **Language:** Python

## ✨ Features

- List and explore your GitHub repositories
- View open/closed issues for any repo
- Check pull requests status
- Get your GitHub profile summary
- Chat via CLI or web UI

## 🚀 How to Run

### CLI

```bash
python cli.py
```

### Web UI

```bash
streamlit run ui/app.py
```

## 🏗️ Architecture

User → Gemini LLM → MCP Client → MCP Server → GitHub API
