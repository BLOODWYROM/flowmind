# FlowMind MVP

FlowMind is a Developer Unified Intelligence Dashboard that connects to your tools (GitHub, Gmail) and uses AI to summarize and prioritize your notifications.

## Project Structure

This project is divided into two main components:
- `backend/`: FastAPI application with LangGraph for agent orchestration.
- `frontend/`: Next.js frontend with Tailwind CSS and Zustand for state management.

## Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 18+
- Google Gemini API Key

### Backend Setup
1. Navigate to the backend directory: `cd backend`
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt` (or manually run the pip install command if `requirements.txt` was dynamically generated)
5. Copy the `.env.example` file to `.env` and fill in your `GEMINI_API_KEY`.
6. Start the FastAPI server: `uvicorn backend.main:app --reload`
   - Note: Run this from the root directory or adjust your PYTHONPATH. Alternatively, run `cd backend && uvicorn main:app --reload`.

### Frontend Setup
1. Navigate to the frontend directory: `cd frontend`
2. Install dependencies: `npm install`
3. Start the Next.js development server: `npm run dev`
4. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Features Included in MVP
- **Mock OAuth Connection**: Connect GitHub and Gmail (mocked flow for easy local testing).
- **LangGraph Agents**:
  - `Data Fetcher`: Grabs mocked recent notifications from GitHub and Gmail.
  - `Prioritizer`: Uses Gemini to score urgency (1-10) and assign tags (`Action Required`, `FYI`, `Ignore`).
  - `Summarizer`: Uses Gemini to create a morning briefing narrative.
- **Unified Dashboard**: Clean dark-mode UI to view your priority items without context switching.

## Testing
Run the basic tests for the agents:
```bash
cd backend
python -m pytest tests/
```
