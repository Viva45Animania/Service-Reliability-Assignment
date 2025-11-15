# Service-Reliability-Assignment
Take home assignment for a service reliability app to check on the health status of deployed services
---
📡 Service Reliability Monitor

A lightweight service reliability and health monitoring system that periodically checks multiple service endpoints, records their availability and performance, and exposes the results via a REST API and a simple dashboard.

Designed using Domain-Driven Design (DDD) principles, FastAPI, and an asynchronous scheduler to ensure clarity, reliability, and maintainability.
---
⚡ Quickstart
1. Clone the repository
git clone https://github.com/your-username/service-reliability-monitor.git
cd service-reliability-monitor

2. Create a virtual environment
python -m venv venv
source venv/bin/activate      # macOS / Linux
venv\Scripts\activate         # Windows

3. Install dependencies
pip install -r requirements.txt

4. Configure environment variables

Create a .env file in the project root:

cp .env.example .env


Example:

HEALTH_CHECK_INTERVAL_SECONDS=60
ALERT_CONSECUTIVE_FAILURES_THRESHOLD=3
ALERT_WEBHOOK_URL=
DB_URL=sqlite:///./health.db

5. Configure monitored services

Edit config/services.json:

{
  "services": [
    {
      "id": "github",
      "name": "GitHub API",
      "url": "https://api.github.com",
      "expectedVersion": null,
      "environment": "production",
      "enabled": true
    }
  ]
}

6. Run the application
uvicorn app.main:app --reload

Available endpoints
URL	Purpose
/	Dashboard UI
/health	Latest health snapshot (all services)
/health/{serviceId}	Historical health results
/services	Manage monitored services
/docs	Interactive API docs (Swagger)
---
🐳 Running with Docker

Build:

docker build -t service-monitor .


Run:

docker run -p 8000:8000 --env-file .env service-monitor


Optional config mounting:

docker run \
  -p 8000:8000 \
  --env-file .env \
  -v ./config/services.json:/app/config/services.json \
  service-monitor

🏛 Design Overview

The project follows a clean hexagonal / DDD architecture:

1. Domain Layer

Pure business logic:

Service, HealthCheckResult, value objects

Health evaluation logic

No framework dependencies

2. Application Layer

Use cases orchestrate workflows:

Initialize services from config

Run health checks (async)

Return summaries & histories

Create/enable/disable services

Evaluate alert conditions

3. Infrastructure Layer

Concrete implementations:

SQLite repositories (SQLAlchemy)

Async HTTP pinger (httpx)

Scheduler background loop

Alert notifier (log + webhook)

ORM models & DB bootstrap

4. Interface Layer

APIs & dashboard:

REST endpoints (FastAPI)

DTOs for service/health responses

HTML dashboard (Jinja2 templates)

This layered structure ensures testability, clarity, and easy future extension.

---
🚀 Deployment / Infrastructure Notes

The system runs as a single lightweight containerised service.
It is suitable for:

Local development

Docker Desktop

AWS ECS/Fargate

Kubernetes (EKS/GKE/AKS)

Private servers

No external dependencies are required by default (SQLite).
Environment variables control the scheduler interval and alerting settings.

In containerised/cloud environments:

Run as a single replica (to avoid duplicate checks).

Logs can be forwarded to CloudWatch/ELK/OpenTelemetry.

The embedded DB can be swapped with PostgreSQL/MySQL using the repository abstraction.

⚖ Trade-offs & Design Decisions

Monolith vs Microservices:
Chose a single lightweight service instead of splitting scheduler/API/UI to keep deployment simple and predictable.

SQLite:
Selected for ease of setup and portability. Can be swapped with a relational DB without changing the domain model.

Polling:
Time-based polling was chosen for predictability and simplicity over event-driven architecture.

Async single worker:
Horizontal scaling intentionally avoided because duplicated checks are undesirable.

Simple server-rendered UI:
A Jinja2 dashboard keeps dependencies minimal while still making the system easy to observe.

---
🔮 Future Enhancements

Version drift analytics

Environment grouping and filtering in UI

Websocket or Server-Sent Events for live updates

Automatic retry or exponential backoff rules

Metrics export (Prometheus/OpenTelemetry)

Advanced alert routing (Slack/Teams/email)

---
🤖 AI Usage

AI tools (ChatGPT and GitHub Copilot) were used responsibly to support development.
As my primary language is Java, AI was used to:

Verify Python and FastAPI syntax

Debug errors and interpret tracebacks

Suggest idiomatic async patterns

Generate boilerplate (DTOs, routers, examples)

Assist with documentation clarity

All design decisions, domain modelling, logic implementation, and architecture were manually reviewed, adapted, or rewritten. AI served as a productivity enhancer, not a substitute for engineering reasoning.