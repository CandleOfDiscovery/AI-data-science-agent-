# AI Data Science Agent Platform

A production-style microservice platform for automated data science workflows. The LLM plans and explains; deterministic Python services perform profiling, cleaning, visualization, ML recommendations, and report generation.

## Stack

- Next.js 15, TypeScript, TailwindCSS, React Query-ready UI patterns, Zustand-ready state architecture
- FastAPI microservices
- pandas, numpy, scipy, scikit-learn, matplotlib, seaborn, reportlab
- OpenRouter planner integration with JSON-only structured plans

## Services

- `apps/web` - premium SaaS dashboard at `http://localhost:3000`
- `apps/api-gateway` - upload, orchestration, status, report, download endpoints
- `services/planner-service` - OpenRouter/fallback plan generation
- `services/profiling-service` - deterministic dataset profiling
- `services/cleaning-service` - deterministic safe cleaning actions
- `services/visualization-service` - chart generation
- `services/ml-advisor-service` - task detection and model advice
- `services/report-service` - HTML/PDF report generation

## Quick start

```bash
cp .env.example .env
docker compose up
```

Open `http://localhost:3000` and upload a CSV or XLSX file.

## API

- `POST /upload` multipart file upload (`.csv`, `.xlsx`)
- `POST /analyze` with `{ "analysis_id": "..." }`
- `GET /analysis/{id}` returns analysis JSON
- `GET /report/{id}` returns HTML report
- `GET /download/{id}` downloads cleaned CSV

## Security model

- API keys remain server-side in `.env`
- LLM returns structured JSON only and never manipulates data
- Cleaning service supports only allow-listed deterministic actions
- File extensions are validated at upload
- CORS is configurable via `CORS_ORIGINS`

## Example data

See `examples/sample_customers.csv`.
