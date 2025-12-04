# 🤖 AI Support Assistant

> An intelligent support chatbot powered by LangChain, Ollama LLM, and FAISS vector search that provides contextual answers from your company's knowledge base and project documentation.

---

## 🌟 Features

- ✅ **RAG-Based Question Answering**: Retrieval-Augmented Generation using FAISS vector store
- ✅ **Multi-Source Context**: Integrates knowledge base articles and project information
- ✅ **Local LLM Integration**: Uses Ollama for privacy-focused, on-premise AI inference
- ✅ **Semantic Search**: Finds relevant information using sentence transformers
- ✅ **Interactive Chat Interface**: Command-line based conversational interface
- ✅ **MySQL Backend**: Structured data storage for knowledge base and projects
- ✅ **Smart Troubleshooting**: Context-aware suggestions based on SOPs and FAQs

---

## 📋 Prerequisites

- Python 3.10+
- MySQL  8.0+
- [Ollama](https://ollama.ai/) installed locally
- 8GB+ RAM recommended

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Nplite/ChatBot-MySQL
cd ChatBot-MySQL
```

### 2. Create Virtual Environment

```bash
conda create -p venv python==3.12 -y

# Windows
conda activate venv/
```

### 3. Install Dependencies

```bash
pip install langchain langchain-ollama langchain-community
pip install faiss-cpu sentence-transformers
pip install sqlalchemy pymysql python-dotenv
pip install scikit-learn numpy
```

**Or use requirements.txt:**

```bash
pip install -r requirements.txt
```


### 4. Install and Setup Ollama

**Download and install Ollama** from [ollama.ai](https://ollama.ai/)

**Pull the required model:**
```bash
ollama pull qwen3:8b
# OR
ollama pull llama3.1
```

**Verify installation:**
```bash
ollama list
```

### 5. Setup MySQL Database

**Create the database and tables:**

```sql
CREATE DATABASE ai_assistant;
USE ai_assistant;

-- Knowledge Base Table
CREATE TABLE knowledgebase (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    category VARCHAR(100),
    tags VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Projects Table
CREATE TABLE projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_name VARCHAR(255) NOT NULL,
    description TEXT,
    tech_stack TEXT,
    status VARCHAR(50),
    start_date DATE,
    metadata JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);


-- Sample Knowledge Base Data
INSERT INTO knowledgebase (title, content, category, tags) VALUES
('Milagro Offer Engine – Dynamic Rules',
 'Milagro\'s Offer Engine allows restaurants to create dynamic promotions using spend thresholds, visit frequency, and customer segments. Rules support auto-apply coupons, BOGO promotions, and scheduled offer campaigns.',
 'docs',
 'milagro,offers,promotions'),

('Utiliko CRM Lead Pipeline Setup',
 'To configure lead pipelines: create stages (New → Qualified → In Progress → Won/Lost), assign team access levels, enable notifications, and define automation triggers for stage transitions.',
 'sop',
 'utiliko,crm,leads');


-- Sample Projects Data
INSERT INTO projects (project_name, description, tech_stack, status, start_date) VALUES
('Milagro Loyalty Points Engine',
 'Tracks and manages customer loyalty points, redemptions, and tier progression in real-time across POS and mobile apps.',
 'Node.js, MongoDB, Redis, Express',
 'active',
 '2024-03-15'),

('Utiliko Compliance & Audit Tracker',
 'Tracks compliance across multiple projects, logs changes, and automates audit report generation with role-based access.',
 'Python, FastAPI, PostgreSQL, Celery, Vue.js',
 'active',
 '2024-01-15');

```

### 6. Configure Environment Variables

**Create a `.env` file in the root directory:**

```env
# Database Configuration
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password_here
MYSQL_DATABASE=ai_assistant

# Ollama Model
OLLAMA_MODEL=qwen3:8b
# Alternative: OLLAMA_MODEL=llama3.1

# Embedding Model
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

> **⚠️ Note:** Special characters in passwords are automatically URL-encoded by the system.

---

## 📁 Project Structure

```
ai-support-assistant/
│
├── config/
│   ├──setup_database.py     # Create the table and dump the data to MySQL
│   └── database.py          # Database configuration and connection
│
├── src/
│   ├── data_loader.py       # Load data from MySQL
│   ├── vector_store.py      # FAISS vector store management
│   ├── retriever.py         # Advanced context retrieval
│   └── chatbot.py           # Main chatbot logic
│
├── vector_db/               # Persisted FAISS vector store (auto-generated)
│
├── main.py                  # Application entry point
├── .env                     # Environment variables (create this)
├── requirements.txt         # Python dependencies
├── test.py                  # Test the ollama models
└── README.md               # This file
```

---

## 🎯 Usage

### Start the Chatbot

```bash
python main.py
```

### Force Rebuild Vector Store

If you've updated the knowledge base or projects:

```bash
python main.py --reload
```

## 🔧 Configuration Options

### Change LLM Model

Edit `.env`:
```env
OLLAMA_MODEL=llama3.1
# or
OLLAMA_MODEL=mistral
# or
OLLAMA_MODEL=qwen3
```

Then pull the model:
```bash
ollama pull llama3.1
```

**Available Models:**
| Model | Size | Speed | Quality | Use Case |
|-------|------|-------|---------|----------|
| tinyllama:latest | ~600MB | Very Fast | Good | Quick responses |
| llama3.1 | ~4.7GB | Fast | Excellent | Best balance |
| mistral | ~4.1GB | Fast | Excellent | Technical queries |
| qwen3 | ~2.3GB | Fast | Very Good | General purpose |

### Adjust Response Temperature

In `src/chatbot.py`, modify:
```python
self.llm = OllamaLLM(
    model=model_name,
    temperature=0.3,  # 0.0 = deterministic, 1.0 = creative
)
```

**Temperature Guide:**
- `0.0-0.3`: Factual, consistent responses (recommended for support)
- `0.4-0.7`: Balanced creativity and accuracy
- `0.8-1.0`: More creative, varied responses

### Change Embedding Model

Edit `.env`:
```env
EMBEDDING_MODEL=sentence-transformers/all-mpnet-base-v2
```

**Popular Alternatives:**
| Model | Dimensions | Performance | Use Case |
|-------|------------|-------------|----------|
| all-MiniLM-L6-v2 | 384 | Fast, efficient | Default, best for speed |
| all-mpnet-base-v2 | 768 | Better quality | More accurate retrieval |
| paraphrase-multilingual-MiniLM-L12-v2 | 384 | Multilingual | Non-English support |

### Adjust Number of Retrieved Documents

In `src/retriever.py`:
```python
def retrieve_context(self, query: str, k: int = 5):
    # Change k to retrieve more/fewer documents
```

---

## 🛠️ Troubleshooting

### Ollama Connection Issues

**Check if Ollama is running:**
```bash
ollama list
```

**Restart Ollama service:**
```bash
# Start Ollama
ollama serve
```

**Test model:**
```bash
ollama run tinyllama "Hello, how are you?"
```

### MySQL Connection Errors

**Verify credentials:**
- Check username and password in `.env`
- Ensure MySQL service is running:
  ```bash  
  # Windows
  net start MySQL80
  ```

**Create database if missing:**
```sql
CREATE DATABASE ai_assistant;
```

**Test connection:**
```bash
mysql -u root -p -h localhost
```

### Vector Store Issues

**Delete and rebuild:**
```bash
# Remove existing vector store
rm -rf vector_db/

# Rebuild from scratch
python main.py --reload
```

### Import Errors

**Upgrade packages:**
```bash
pip install --upgrade langchain langchain-ollama langchain-community
pip install --upgrade faiss-cpu sentence-transformers
```

**Verify installations:**
```bash
pip list | grep langchain
pip list | grep faiss
```

### Performance Issues

**Reduce context window:**
```python
# In src/retriever.py
context = self.retriever.retrieve_context(question, k=3)  # Instead of k=5
```

**Use smaller embedding model:**
```env
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

**Switch to lighter LLM:**
```env
OLLAMA_MODEL=tinyllama:latest
```

---

## 📊 System Architecture

```
┌──────────────────┐
│   User Input     │
│  (Command Line)  │
└────────┬─────────┘
         │
         v
┌─────────────────────────────────┐
│      Main Application           │
│        (main.py)                │
│  ┌──────────────────────────┐   │
│  │  Initialize Components   │   │
│  │  - Database Config       │   │
│  │  - Vector Store          │   │
│  │  - Retriever             │   │
│  │  - Chatbot               │   │
│  └──────────────────────────┘   │
└────────┬────────────────────────┘
         │
         v
┌─────────────────────────────────┐
│    Support Chatbot              │
│     (chatbot.py)                │
│  ┌──────────────────────────┐   │
│  │  Format Context          │   │
│  │  Generate Response       │   │
│  │  Return Suggestions      │   │
│  └──────────────────────────┘   │
└────────┬────────────────────────┘
         │
         v
┌─────────────────────────────────┐
│   Advanced Retriever            │
│    (retriever.py)               │
│  ┌──────────────────────────┐   │
│  │  Query Processing        │   │
│  │  Context Assembly        │   │
│  │  Troubleshooting Logic   │   │
│  └──────────────────────────┘   │
└────────┬────────────────────────┘
         │
         v
┌─────────────────────────────────┐
│    Vector Store Manager         │
│   (vector_store.py)             │
│  ┌──────────────────────────┐   │
│  │  FAISS Vector Database   │   │
│  │  Semantic Search         │   │
│  │  Similarity Matching     │   │
│  └──────────────────────────┘   │
└────────┬────────────────────────┘
         │
         v
┌─────────────────────────────────┐      ┌──────────────────┐
│      Data Loader                │◄─────┤  MySQL Database  │
│    (data_loader.py)             │      │                  │
│  ┌──────────────────────────┐   │      │  - knowledgebase │
│  │  Load Knowledge Base     │   │      │  - projects      │
│  │  Load Projects           │   │      └──────────────────┘
│  │  Format Documents        │   │
│  └──────────────────────────┘   │
└─────────────────────────────────┘
         │
         v
┌─────────────────────────────────┐
│     Ollama LLM                  │
│   (Local Inference)             │
│  ┌──────────────────────────┐   │
│  │  Process Prompts         │   │
│  │  Generate Responses      │   │
│  │  Temperature Control     │   │
│  └──────────────────────────┘   │
└─────────────────────────────────┘
```

---


## 📝 Important Notes

### Ticket System Removed
This version focuses exclusively on knowledge base and project information. All ticket-related functionality has been intentionally removed to streamline the system.

### Privacy & Security
- ✅ **Local Processing**: All AI inference happens locally via Ollama
- ✅ **No External APIs**: No data sent to cloud services
- ✅ **Data Control**: Full control over your data in MySQL
- ⚠️ **Secure Passwords**: Use strong passwords and keep `.env` secure

### Performance Tips
- Use `tinyllama` for fastest responses
- Reduce `k` parameter for quicker retrieval
- Keep knowledge base articles concise (< 500 words)
- Regularly clean up old project entries

### Extensibility
The system is designed to be easily extended:
- Add new data sources in `data_loader.py`
- Customize prompts in `chatbot.py`
- Modify retrieval logic in `retriever.py`
- Add preprocessing in `vector_store.py`

---


## 🔗 Resources

### Official Documentation
- [LangChain Documentation](https://python.langchain.com/)
- [Ollama Official Site](https://ollama.ai/)
- [Ollama Model Library](https://ollama.ai/library)
- [FAISS Documentation](https://faiss.ai/)
- [Sentence Transformers](https://www.sbert.net/)

### Tutorials & Guides
- [LangChain RAG Tutorial](https://python.langchain.com/docs/use_cases/question_answering/)
- [Building with Ollama](https://github.com/ollama/ollama/blob/main/docs/api.md)
- [FAISS for Similarity Search](https://github.com/facebookresearch/faiss/wiki)

### Community
- [LangChain GitHub](https://github.com/langchain-ai/langchain)
- [Ollama Discord](https://discord.com/invite/ollama)
- [FAISS Issues](https://github.com/facebookresearch/faiss/issues)


## 🎉 Acknowledgments

- **LangChain** for the powerful RAG framework
- **Ollama** for local LLM inference
- **Meta** for FAISS vector search
- **Sentence Transformers** for embeddings
- **SQLAlchemy** for database ORM



**Built with ❤️ using LangChain, Ollama, and FAISS**

*Last Updated: December 2024*