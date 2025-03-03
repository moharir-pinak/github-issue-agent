# 🚀 GitHub Issue Agent  

An **AI-powered assistant** that fetches, organizes, and retrieves GitHub issues intelligently, making issue tracking more efficient for developers and project maintainers.  

## 🔍 Features  
- **AI-Powered Search**: Quickly find relevant GitHub issues using natural language queries.  
- **LangChain & OpenAI Embeddings**: Converts issues into vectorized representations for accurate retrieval.  
- **AstraDB Vector Store**: Efficient storage and semantic search for large-scale GitHub issues.  
- **Automated Updates**: Dynamically pulls and updates issues to keep data fresh.  

## 📌 How It Works  
1. Fetches GitHub issues using the **GitHub API**.  
2. Embeds and stores issues in **AstraDB Vector Store** using **OpenAI Embeddings**.  
3. Uses **LangChain** to enable intelligent querying.  
4. Allows users to ask questions and retrieve the most relevant issues.  

## 🛠 Installation & Setup  

### 1️⃣ Clone the Repository  
```bash
git clone https://github.com/moharir-pinak/github-issue-agent.git
cd github-issue-agent
pip install -r requirements.txt
OPENAI_API_KEY=your_openai_api_key
ASTRA_DB_API_ENDPOINT=your_astra_db_endpoint
ASTRA_DB_APPLICATION_TOKEN=your_astra_db_token
ASTRA_DB_KEYSPACE=your_astra_db_keyspace
python main.py
