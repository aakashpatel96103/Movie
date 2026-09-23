# Movie Theater Booking Microservices

A simple FastAPI microservices project with two independent services.

## Microservices

- Movie Service - Port 8001
- Booking Service - Port 8002

## Communication

Booking Service communicates synchronously with Movie Service using HTTPX when booking or cancelling a ticket.

## Run with Docker Compose

```bash
docker-compose build
docker-compose up -d
docker-compose ps
```

## Swagger

- http://localhost:8001/docs
- http://localhost:8002/docs

## Jenkins

GitHub -> Jenkins -> Environment -> Install Dependencies -> Docker Build -> Deploy -> Final Status
