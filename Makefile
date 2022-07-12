.DEFAULT_GOAL := help
DOCKER_PROD = docker-compose.yml
STACK_NAME = "Billing"
#####---PROD---#####
help:
	$(info ------------------------------------------------------------------------------------------------------------------------------)
	$(info "#####---PROD---#####" (build, up, build_up, start, down, destroy, stop, restart))
	$(info ------------------------------------------------------------------------------------------------------------------------------)
build:
	docker-compose -p ${STACK_NAME} -f ${DOCKER_PROD} build
up:
	docker-compose -p ${STACK_NAME} -f ${DOCKER_PROD} up -d
build_up: build up
start:
	docker-compose -p ${STACK_NAME} -f ${DOCKER_PROD} start
down:
	docker-compose -p ${STACK_NAME} -f ${DOCKER_PROD} down
destroy:
	docker-compose -p ${STACK_NAME} -f ${DOCKER_PROD} down -v
	docker volume ls -f dangling=true
	docker volume prune --force
	docker image prune --force --filter="dangling=true"
stop:
	docker-compose -p ${STACK_NAME} -f ${DOCKER_PROD} stop
restart:
	docker-compose -p ${STACK_NAME} -f ${DOCKER_PROD} stop
	docker-compose -p ${STACK_NAME} -f ${DOCKER_PROD} up -d
