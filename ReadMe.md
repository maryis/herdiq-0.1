Deploying on Google Cloud Run
1️⃣ Create Cloud SQL (MySQL) and Cloud Storage bucket
gcloud sql instances create agent-db --database-version=MYSQL_8_0 --tier=db-f1-micro
gcloud storage buckets create gs://your-bucket-name --location=EU

2️⃣ Build & Deploy
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

💰 Expected Cost (monthly)
Component	Description	Approx Cost
Cloud Run	Serverless FastAPI	$1 – $5
Cloud SQL (MySQL)	f1-micro tier	$7 – $10
Cloud Storage	Cache text	< $1
Gemini 1.5 Flash	Pay-per-token	< $5
Total MVP		≈ $15 / month
🧭 Next Steps

Add Firestore for chat history / memory.

Add scheduled Cloud Run Job to refresh cached websites daily.

Add LangGraph / CrewAI for richer agent orchestration later.
