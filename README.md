# ResearchMind — Multi-Agent AI Research System
 
**Live demo:** [multi-agent-ai-research-system.streamlit.app](https://multi-agent-ai-research-system-sj3udxarrg2d7nhk3qmk7e.streamlit.app/)
 
ResearchMind is a multi-agent AI pipeline that autonomously searches the web, reads and extracts source content, writes a structured research report, and critiques its own output — all from a single topic prompt.
 
---
 
## How it works
 
Four stages run in sequence, each agent handing its output to the next:
 
| Stage | Component | Role |
|---|---|---|
| 01 | **Search Agent** | Uses the Tavily API to find recent, relevant sources on the topic |
| 02 | **Reader Agent** | Uses BeautifulSoup to scrape and extract deep content from the most relevant source |
| 03 | **Writer Chain** | An LCEL (LangChain Expression Language) pipeline drafts a structured report from the gathered research |
| 04 | **Critic Chain** | A second LCEL pipeline scores the report and gives constructive, specific feedback |
 
Both agents are powered by **Mistral** as the underlying LLM, orchestrated with **LangChain** and **LangGraph** (`create_react_agent`).
 
---
 
## Tech stack
 
- **LLM:** Mistral API (`mistral-small-latest`)
- **Orchestration:** LangChain, LangChain Core (LCEL / Runnables), LangGraph (ReAct agents)
- **Search tool:** Tavily API
- **Scraping tool:** BeautifulSoup4 + Requests
- **UI:** Streamlit
- **Deployment:** Streamlit Community Cloud
---
 
## Project structure
 
```
├── app.py            # Streamlit UI
├── pipeline.py        # Orchestrates the 4-stage agent pipeline
├── agents.py           # Builds the search & reader agents, writer & critic chains
├── tools.py             # Tavily search tool + BeautifulSoup scraping tool
├── requirements.txt      # Python dependencies
└── .gitignore              # Excludes .venv, __pycache__, and .env from version control
```
 
---

## Deployment
 
This app is deployed for free on **Streamlit Community Cloud**.
## Disclaimer
 
This is a personal / educational project demonstrating multi-agent LLM orchestration. Since the demo is public, it shares the developer's API rate limits — please be mindful of usage.
