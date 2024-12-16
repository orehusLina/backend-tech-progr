# fastapi_docker_postgres_example
FastApi app with Docker + PostgreSQL study example

Порядок запуска приложения:
- создать poetry окружение на основе Python ^3.11
- в терминале прописать poetry install
- дождаться установки всех библиотек и сборки проекта (`Installing the current project: project (0.1.0)`)
- в терминале прописать docker compose up
- При успешном запуске будет написано:
  - `INFO:     Application startup complete.`
  - `INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)`


Swagger:
- после успешного запуска приложения, по адресу http://localhost:8020/docs будет доступен swagger