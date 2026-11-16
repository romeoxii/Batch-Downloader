# Fetchflow

A batch file & folder downloader with a FastAPI backend and React frontend — built as a learning project while studying Python, HTTP requests, file handling, and full-stack development.

## Current Features

- **Direct file downloads** — paste any HTTP/HTTPS file URL
- **Folder batch downloads** — paste an Alist-compatible folder URL and every file inside is queued automatically
- **Streaming downloads** — files are written chunk-by-chunk, so large files stay light on memory
- **Live progress** — speed, percentage, and time remaining update in real time for every active download
- **Resume support** — interrupted downloads continue via `Range` requests when the server allows it
- **Cancel & retry** — stop a running download or retry a failed one without re-adding it
- **Duplicate detection** — skips files that already exist locally
- **Queue view** — active downloads show as full cards, pending files stack in a scrollable queue, finished ones collapse into a history section

## Tech Stack

- **Backend**: Python, FastAPI, Uvicorn, Requests
- **Frontend**: React 19, TypeScript, Vite, Tailwind CSS v4, Hugeicons, React Router
- **Dev tools**: Bun, ESLint, Git

## Project Status

**Work in Progress** — this repository represents my progress while learning Python and full-stack development through a practical project. The code and architecture will evolve as I learn more.

### Known Limitations

- Folder listing currently expects an **Alist-style API** (a POST request with a specific JSON payload). Generic directory indexes and other folder sources are not supported yet.
- Jobs are stored **in memory** — restarting the backend clears the queue and history (persistence is planned).
- No authentication or rate limiting — intended for personal/local use.

## Running Locally

```bash
# Backend (from the repo root)
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend (separate terminal)
cd frontend
bun install
bun run dev
```

Open http://localhost:5173 — the homepage links to the downloader at `/downloader`.

## Author

**romeoxii**

Built as part of my Python learning journey.
