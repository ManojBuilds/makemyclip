# Production Deployment Guide (Free Tier Strategy)

This guide outlines a cost-free strategy to deploy the **MakeMyClip** stack. Given the high CPU/RAM requirements for video processing (FFmpeg), we use a hybrid approach across specialized free-tier providers.

## 🏗 Architecture Overview

| Component | Provider | Free Tier Benefits |
| :--- | :--- | :--- |
| **Frontend / Waitlist** | [Vercel](https://vercel.com) | Best Next.js support, edge functions. |
| **Database (Postgres)** | [Neon](https://neon.tech) | Serverless, autoscaling, 500MB storage. |
| **Redis (Queue/Cache)** | [Upstash](https://upstash.com) | Serverless Redis, perfect for ARQ workers. |
| **Backend & Worker** | [Hugging Face Spaces](https://huggingface.co/spaces) | **2 vCPU, 16GB RAM** (Docker), free persistent-ish. |
| **Media Storage** | [Cloudflare R2](https://cloudflare.com) | 10GB storage, $0 egress (optional but recommended). |

---

## 1. Database Setup (Neon)

1.  **Create Account**: Sign up at [Neon.tech](https://neon.tech/).
2.  **Create Project**: Name it `makemyclip-prod`.
3.  **Connection String**: Copy the "Pooled" connection string. It looks like:
    `postgresql://user:password@host.neon.tech/neondb?sslmode=require`
    *   **Backend Note**: Since the backend uses `sqlalchemy` with `asyncpg`, your `DATABASE_URL` for the **Hugging Face Space** must start with `postgresql+asyncpg://`.
    *   **Frontend Note**: The Next.js app (Prisma) uses the standard `postgresql://` prefix.
    From your local machine, run:
    ```bash
    cd frontend
    DATABASE_URL="your_neon_url" npx prisma migrate deploy
    ```

## 2. Redis Setup (Upstash)

1.  **Create Account**: Sign up at [Upstash](https://upstash.com/).
2.  **Create Redis**: Select a region close to your Hugging Face Space (usually `us-east-1`).
3.  **Credentials**: Copy the `UPSTASH_REDIS_REST_URL` and `Password`.
    *   For the Backend, you will need the `Endpoint` (host) and `Password`.

---

## 3. Backend & Worker Setup (Hugging Face)

Hugging Face Spaces offer the best free hardware for FFmpeg. Since we need to run both the FastAPI API and the ARQ Worker, we will use a process manager.

### Step A: Create `backend/start_prod.sh`
Create this file to launch both processes in one container:

```bash
#!/bin/bash
# Start ARQ worker in the background
.venv/bin/arq src.workers.tasks.WorkerSettings &

# Start FastAPI on port 7860 (Hugging Face default)
.venv/bin/uvicorn src.main_refactored:app --host 0.0.0.0 --port 7860
```

### Step B: Create a Hugging Face Space
1.  Go to [huggingface.co/new-space](https://huggingface.co/new-space).
2.  **SDK**: Select **Docker**.
3.  **Public/Private**: Public is free; Private may require a subscription for high-resource hardware, but the "Basic" 16GB RAM tier is free for public spaces.
4.  **Upload**: Push your `backend/` directory or connect your GitHub.

### Step C: Environment Variables
In the HF Space **Settings > Variables and secrets**, add:
*   `DATABASE_URL`: (Neon URL)
*   `REDIS_HOST`: (Upstash Endpoint)
*   `REDIS_PORT`: `6379`
*   `REDIS_PASSWORD`: (Upstash Password)
*   `ASSEMBLY_AI_API_KEY`: (Your Key)
*   `GOOGLE_API_KEY`: (For Gemini/LLM)
*   `SELF_HOST`: `true`

---

## 4. Frontend & Waitlist Setup (Vercel)

1.  **Import Repo**: Connect GitHub to Vercel.
2.  **Configure**:
    *   **Root Directory**: `frontend` (Repeat for `waitlist`).
    *   **Framework Preset**: Next.js.
3.  **Environment Variables**:
    *   `DATABASE_URL`: (Neon URL)
    *   `NEXT_PUBLIC_API_URL`: `https://your-space-name.hf.space` (Found in HF Space "Embed this Space")
    *   `BETTER_AUTH_SECRET`: (Run `openssl rand -base64 32`)
    *   `BETTER_AUTH_URL`: `https://your-app.vercel.app`

---

## 🛠 Critical Adjustments for Video Storage

The app currently saves clips to `/app/clips`. On Hugging Face (and most free tiers), this storage is **ephemeral**. If the container restarts, files are deleted.

### Recommended Fix: Cloudflare R2
1.  Sign up for **Cloudflare R2** (10GB free).
2.  In `backend/src/services/storage.py` (if it exists), add logic to upload to S3/R2 instead of local disk.
3.  Alternatively, ensure users download their clips immediately.

---

## ✅ Deployment Checklist
- [ ] Prisma migrations applied to Neon.
- [ ] Upstash Redis pingable.
- [ ] Hugging Face Space status is "Running".
- [ ] Vercel build successful.
- [ ] `NEXT_PUBLIC_API_URL` updated to the HF Space URL.

> [!IMPORTANT]
> **Performance Tip**: Both Neon and Hugging Face Spaces "sleep" after inactivity on the free tier. Your first request after a break will experience a "Cold Start" delay of 10-20 seconds.
