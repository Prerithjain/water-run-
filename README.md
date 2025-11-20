# Water Run Counter

A clean, responsive web app to track water runs.

## Features
- Track "Alone" (2 pts) or "Group" (1 pt) runs.
- Suggests the next pair based on lowest score and time since last visit.
- Visual charts and history.
- Export to CSV and PDF.
- Mobile-friendly premium design.

## Setup

1. Install dependencies:
   ```bash
   npm install
   pip install -r requirements.txt
   ```

2. Run locally:
   ```bash
   npm run dev
   ```
   This starts both the Python backend (port 8000) and Next.js frontend (port 3000).
   Open [http://localhost:3000](http://localhost:3000).

## Deployment to Vercel

1. Push to GitHub.
2. Import project in Vercel.
3. Vercel should automatically detect Next.js.
4. The `vercel.json` and `api/index.py` are configured for Python Serverless Functions.
5. **Note on Persistence**: Vercel serverless functions have ephemeral storage. The SQLite database (`data/waterrun.db`) will NOT persist between deployments or cold starts on Vercel.
   - For a persistent demo, use a provider like Render or Railway for the backend, or use Vercel KV / external database (Postgres/Turso).
   - This project uses a local SQLite file as requested, which works perfectly for local development.

3. **(Optional) Enable WhatsApp Alerts - 100% FREE!**:
   - See detailed setup guide: [WHATSAPP_SETUP.md](./WHATSAPP_SETUP.md)
   - Uses **CallMeBot** - completely FREE WhatsApp API (no credit card needed!)
   - Takes 5 minutes per person to setup
   - Quick start: Create a `.env` file (see `env.example`)

## Tech Stack
- **Frontend**: Next.js (App Router), Tailwind CSS, Chart.js, SWR.
- **Backend**: FastAPI (Python), SQLite3.
# water-run-
