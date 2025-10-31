
.PHONY: up down migrate
up:
	docker-compose up -d

down:
	docker-compose down

migrate:
	psql postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:${POSTGRES_PORT}/${POSTGRES_DB} -f infra/schema.sql
