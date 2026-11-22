# Setup & First Run Guide

Your API keys have already been populated in `backend/.env` from your provided credentials:
- **NewsData.io:** Configured
- **Currents API:** Configured
- **GNews:** Configured
- **Google Gemini:** Configured
- **Groq Cloud:** Configured

## Running the Application Locally

### Step 1: Start Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --port 8000 --reload
```

### Step 2: Trigger Your First Newspaper Generation
Once the backend is running, you can immediately generate today's newspaper edition by running:
```bash
curl -X POST http://localhost:8000/api/editions/generate
```
or by clicking the **"Trigger Manual Generation"** button in the Swagger UI at [http://localhost:8000/docs#/editions/trigger_manual_generation_api_editions_generate_post](http://localhost:8000/docs).

### Step 3: Start Frontend
```bash
cd frontend
npm install
npm run dev
```
Visit [http://localhost:3000](http://localhost:3000) to view your morning digital newspaper!
