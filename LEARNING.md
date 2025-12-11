### Project 2 - Day 1 (Thursday)
**Goal**: Foundation setup - FastAPI + PostgreSQL in Docker

**Completed**:
- Created GitHub repo and project structure
- Built FastAPI app with health endpoints
- Created Dockerfile for FastAPI service
- Set up docker-compose with web + db services
- Got both services running and communicating

**What I learned**:
- FastAPI basics (async routes, auto-docs at /docs)
- Dockerfile structure
- docker-compose services, volumes, depends_on
- PostgreSQL 18 changed volume data directory structure
- Docker troubleshooting: when stuck, nuke and rebuild

**Challenges**:
- Postgres volume path changed in v18 (used /var/lib/postgresql instead of /data)
- Had to clean volumes and rebuild

**Energy**: [3/5]

**Next**: Day 2 - Database models, connect FastAPI to PostgreSQL, first CRUD endpoints