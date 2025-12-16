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

### Project 2 - Day 3 (Monday)
**Goal**: MQTT integration - real-time sensor data ingestion

**Completed**:
- Added Mosquitto MQTT broker to docker-compose
- Created MQTT listener service (subscribed to sensor topics)
- Built sensor simulator (publishes random data every 5 seconds)
- Integrated listener with FastAPI lifespan
- Added readings CRUD endpoints (GET with filters, POST)
- Full pipeline working: Simulator → MQTT → Listener → Database → API

**What I learned**:
- MQTT pub/sub architecture (topics, wildcards)
- Paho MQTT client (on_connect, on_message callbacks)
- Callback-based programming patterns
- Background service integration with FastAPI
- Multi-service Docker orchestration
- Time-series data ingestion patterns
- Query parameter filtering in FastAPI

**Challenges**:
- Understanding on_message callback implementation
- Couldn't test mqtt_listener.py in isolation
- Debugging through Docker logs instead of direct execution
- Complexity overwhelming

**Design flaws**:
- Sensor type validation: currently sensor.sensor_type isn't enforced
- Temperature sensor can receive pH readings (shouldn't be possible)
- Would need validation logic or database constraints in production

**Energy**: 1/5 by end - mentally exhausting day

**Next**: Day 4 (Tuesday) - Authentication & API Enhancement

### Project 2 - Day 4 (Tuesday)
**Goal**: Authentication and API enhancement

**Completed**:
- JWT authentication with python-jose and passlib
- User model and registration endpoint
- Login endpoint (OAuth2 password flow)
- Protected endpoints (require Bearer token)
- Sensor statistics endpoint (avg, min, max, count)
- Hourly aggregation endpoint (time-series grouping)

**What I learned**:
- JWT token creation and validation
- Password hashing with bcrypt
- FastAPI security dependencies (HTTPBearer)
- OAuth2PasswordRequestForm for login
- SQLAlchemy aggregation functions (func.avg, func.min, func.max)
- Date/time filtering and grouping (date_trunc)
- Bearer token authentication flow

**Challenges**:
- Password verification using wrong variable (User vs user)
- Understanding when current_user dependency validates (before function runs)
- Complex SQLAlchemy queries for aggregations

**Energy**: Started 3/5, ended 1/5

**Next**: Day 5 (Wednesday) - Testing & Documentation