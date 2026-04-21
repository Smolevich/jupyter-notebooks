# HH.ru API Tools & Notebooks

This project helps you collect and analyze job data from HeadHunter (HH.ru). It uses Jupyter Notebooks and Python scripts.

## How to Start

### 1. Get API Access
You need to get access from HH.ru:
1.  Go to [api.hh.ru](https://api.hh.ru/).
2.  Register and create a "New Application".
3.  Wait for approval. You will get a `client_id` and `client_secret`.

### 2. Files you need
Create these files in the main folder (they are hidden from Git):
*   `config.json` — your API keys and database password.
*   `token.json` — your login token.
*   `search_config.json` — what jobs you want to search for.

## Tools

### Jupyter Notebooks
*   **`hh_api_loader.ipynb`** — downloads jobs and saves them to ClickHouse database.
*   **`hh_api_updating.ipynb`** — updates job info (like if a job was deleted).
*   **`hh_data_visualizer.ipynb`** — shows charts and analysis.
*   **`telegram_stats.ipynb`** — analyzes Telegram data.

### Python Scripts
*   **`hh_api_tool.py`** — an interactive tool to quickly check jobs or companies in your terminal.
*   **`check_hh_api.py`** — checks if your API token works.

## Rules
*   **Clean Code**: Easy to read without many comments.
*   **No Results in Git**: Notebooks are saved without output (clean cells).
*   **Simple**: Use standard Python tools when possible.

---
*Created for labor market analysis.*