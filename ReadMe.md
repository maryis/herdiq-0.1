# 🚀 AI Startup - All-in-One Stack (React + Node + FastAPI + Postgres + Chroma + Nginx)

This is a **ready-to-deploy** full-stack AI startup template, designed for a **single Google Cloud VM** using Docker Compose.

---

## 🧩 Components

| Service | Port | Description |
|----------|------|-------------|
| frontend | 80 (via nginx) | React web app |
| backend | 4000 | Node.js API |
| agent | 8000 | Python FastAPI AI service |
| postgres | 5432 | Main database |
| chroma | 8001 | Local vector DB |
| nginx | 80 | Reverse proxy + static hosting |

---

## ⚙️ Setup

### 1️⃣ Install Docker on your VM
```bash
sudo apt update && sudo apt install -y docker.io docker-compose
sudo usermod -aG docker $USER && newgrp docker

Create persistent data directories
sudo mkdir -p /var/lib/postgres-data /var/lib/chroma-data
sudo chmod -R 777 /var/lib/postgres-data /var/lib/chroma-data
```

### 2️⃣ Configure environment

Edit .env with your OpenAI key and DB credentials.

### 3️⃣ Build and start everything
```
sudo docker-compose up -d --build
```

🌐 Access

URL	Description

http://<VM_IP>/	React frontend 

http://<VM_IP>/api/hello	Backend API

http://<VM_IP>/agent/ask?query=Hello	AI agent

http://<VM_IP>/agent/health	Agent health check


🧠 Data Persistence
Service	Path	Persistent
PostgreSQL	/var/lib/postgres-data	✅
Chroma	/var/lib/chroma-data


-----

**Deploying on Google Cloud Run**

1️⃣ Create Cloud SQL (MySQL) and Cloud Storage bucket
```
gcloud sql instances create agent-db --database-version=MYSQL_8_0 --tier=db-f1-micro
gcloud storage buckets create gs://your-bucket-name --location=EU
```

2️⃣ Build & Deploy
```
gcloud builds submit --tag gcr.io/your-project/agentic-ai
gcloud run deploy agentic-ai \
  --image gcr.io/your-project/agentic-ai \
  --platform managed \
  --allow-unauthenticated \
  --add-cloudsql-instances your-project:region:agent-db \
  --set-env-vars \
    GEMINI_API_KEY=your_gemini_key,\
    DB_HOST=/cloudsql/your-project:region:agent-db,\
    DB_USER=root,\
    DB_PASS=yourpassword,\
    DB_NAME=yourdbname,\
    CACHE_BUCKET=your-bucket-name \
  --region=europe-west1
```

💰 Expected Cost (monthly)
 
- Cloud Run	Serverless FastAPI	$1 – $5
- Cloud SQL (MySQL)	f1-micro tier	$7 – $10
- Cloud Storage	Cache text	< $1
- Gemini 1.5 Flash	Pay-per-token	< $5
- Total MVP		≈ $15 / month

🧭 Next Steps

- Add Firestore for chat history / memory.
- Add scheduled Cloud Run Job to refresh cached websites daily.
- Add LangGraph / CrewAI for richer agent orchestration later.
