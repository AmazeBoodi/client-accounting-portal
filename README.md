# Client Accounting Portal (MVP)

A simple multi-tenant portal:
- Client login (JWT)
- Expenses + attachments
- Income + attachments
- Invoices + partial payments + overdue indicator
- CSV exports
- Admin panel to create clients + client logins + categories

## 1) Run locally with Docker (recommended)
1. Install Docker Desktop.
2. Copy env files:
   - `backend/.env.example` -> `backend/.env`
   - `frontend/.env.example` -> `frontend/.env` (optional)
3. Start:
   ```bash
   docker compose up --build
   ```

## 2) Create DB tables (migrations)
In a new terminal:
```bash
docker compose exec backend bash -lc "alembic upgrade head"
docker compose exec backend bash -lc "python -m app.seed"
```

Admin login will be printed by the seed script (default: admin@portal.local / admin12345).

Frontend: http://localhost:3000  
Backend: http://localhost:8000/docs

## 3) Deploy (simple)
- Backend: deploy on Render/Railway/Fly as a Docker service.
- Database: use managed Postgres on the same provider.
- Frontend: deploy on Vercel (connect to GitHub), set `NEXT_PUBLIC_API_BASE` to your backend URL.

## Notes
Uploads are stored locally in `backend/app/uploads` for MVP. For production, switch to S3/R2 storage.
