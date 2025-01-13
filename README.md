# SPEEDSOLVER


- https://speedsolver.ru/ - основной сайт.
- https://api.speedsolver.ru/docs - документация к API

## Описание

***SPEEDSOLVER*** — это система управления проектами, предназначенная для эффективного управления командами, проектами, задачами, подзадачами и дедлайнами. Проект помогает командам организовать свою работу, отслеживать прогресс и достигать поставленных целей в срок.

## Содержание

- [Описание](#описание)
- [Функции](#функции)
- [Стек технологий](#стек-технологий)
- [Установка и запуск](#установка)
- [Лицензия](#лицензия)

## Функции

- **Управление командами**: Создание и управление командами, добавление и удаление участников.
- **Управление проектами**: Создание и управление проектами, назначение задач и подзадач. Общение в реальном времени внутри проекта с сохранением истории чата.
- **Управление задачами**: Создание, редактирование и удаление задач, назначение ответственных лиц.
- **Управление подзадачами**: Создание, редактирование и удаление подзадач, отслеживание прогресса.
- **Дедлайны**: Установка и отслеживание дедлайнов для задач и подзадач.
- **Уведомления**: Автоматические уведомления о приближающихся дедлайнах и изменениях в задачах.

## Стек технологий

- **Frontend**: React + TypeScript
- **Backend**: Python - FastAPI, Pydantic, Uvicorn (проксирующийся через nginx)
- **Object Relational Mapping**: Python SQLAlchemy, Alembic, asyncpg driver
- **База данных**: PostgreSQL
- **Аутентификация & Авторизация**: JWT (JSON Web Tokens) - pyjwt
- **Тестирование Backend**: Python - pytest
- **Мониторинг**: Grafana, Prometheus, Node Exporter, AlertManager
- **Логирование**: Собственная библиотека [teleglog](https://github.com/w1tnessbtwwwww/teleglog)
- **Дополнительно**:
   - Docker – контейнеризация приложения.
   - Nginx - Веб-сервер для проксирования внешних подключений путем **reverse proxy**, реализация защищенного соединения с **SSL/TLS**, проксирование поддоменов.
   - Github Actions (CI/CD) – непрерывная интеграция и непрерывная доставка.

## Установка и запуск

1. Клонируйте репозиторий:
   ```shell
   git clone https://github.com/w1tnessbtwwwww/SpeedSolver.git
2. Необходимо создать файл **.env** и заполнить его из **.env.example**.
3. Необходимо переназначить порты в файле **.env** в случае, если у вас заняты одни из назначенных вами.
4. Запустите Docker Engine на вашем компьютере или виртуальной машине.
5. Запустите контейнеры Docker с **Backend** и **Frontend** частью:
- macOS/Linux:
   ```shell
   make build-backend
   make build-frontend
   ```
   
- Windows:
  - При наличии утилиты **make** от **chocolatey**:
   ```shell
   make build-backend
   make build-frontend
   ```
   - В ином случае:
   ```shell
   docker-compose --env-file SpeedSolverBackend/SpeedSolverAPI/.env -f SpeedSolverBackend/SpeedSolverAPI/docker/docker-compose.backend.yml --project-directory SpeedSolverBackend/SpeedSolverAPI up --build -d

   docker-compose -f docker/docker-compose.frontend.yml --project-directory . up --build
   ```
После выполнения всех вышеперечисленных шагов вы сможете получить доступ к:
   - Backend - http://localhost:port/docs, запросы - https://localhost:port/v1/...
   - Frontend - http://localhost:port/

## Лицензия
Этот проект лицензирован по лицензии Apache License 2.0. Подробности см. в файле [LICENSE](https://github.com/w1tnessbtwwwww/SpeedSolver/blob/master/LICENSE).