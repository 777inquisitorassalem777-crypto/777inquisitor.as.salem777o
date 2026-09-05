# Деплой

## VPS
1. Установить Docker + Compose.
2. Клонировать репозиторий.
3. Создать `.env`.
4. `docker compose up -d --build`
5. Проверить `/health`.

## CI/CD
GitHub Actions запускает тесты на push/PR. Production deploy можно добавить отдельным
job с SSH secrets после настройки VPS.

## Production hardening
- reverse proxy + TLS
- OAuth/OIDC
- secret manager
- firewall
- rate limiting
- audit logs
- отдельная сеть для AI backends
- запрет публикации Ollama без reverse proxy/auth
