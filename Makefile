build-backend:
	docker-compose --env-file SpeedSolverBackend/SpeedSolverAPI/.env -f SpeedSolverBackend/SpeedSolverAPI/docker/docker-compose.backend.yml --project-directory SpeedSolverBackend/SpeedSolverAPI up --build -d

build-frontend:
	docker-compose -f SpeedSolverFrontend/docker/docker-compose.frontend.yml --project-directory SpeedSolverFrontend up --build -d