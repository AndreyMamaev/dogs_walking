docker-compose exec backend alembic revision --autogenerate -m "create_table"
docker-compose exec backend alembic upgrade head
docker-compose exec postgres psql -h 127.0.0.1 -U postgres -d postgres -c \
"INSERT INTO executor (id, name) VALUES (1, 'Петр');
INSERT INTO executor (id, name) VALUES (2, 'Антон');"
