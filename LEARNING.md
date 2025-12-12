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

### Project 2 - Day 2 (Friday)
**Goal**: Database integration - models, schemas, CRUD endpoints

**Completed**:
- Created SQLAlchemy models (Sensor and Reading tables)
- Set up database connection with engine and SessionLocal
- Created Pydantic schemas (SensorCreate, SensorResponse)
- Built POST /sensors and GET /sensors endpoints
- Tested CRUD operations via FastAPI docs UI
- Data persisting in PostgreSQL

**What I learned**:
- SQLAlchemy ORM basics (Base, Column types, relationships)
- Foreign keys and relationships (sensor.readings)
- Pydantic schema separation (Create vs Response)
- FastAPI dependency injection (Depends(get_db))
- Database session management (yield pattern)
- server_default=func.now() for database-side timestamps
- How Pydantic, FastAPI, and SQLAlchemy layers interact

**Challenges**:
- created_at field was NULL - needed server_default=func.now()
- Confusing which layer (Pydantic/FastAPI/SQLAlchemy) was causing issues
- Understanding data flow between three frameworks
- Initially returned wrong type from endpoint

**Debugging process**:
- Tried making created_at nullable in schema (didn't like this solution)
- Researched SQLAlchemy default timestamps
- Found server_default solution - database handles it

**Energy**: [1/5] - what a day

**Next**: Day 3 - MQTT integration, sensor data ingestion