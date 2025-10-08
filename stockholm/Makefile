IMAGE_NAME = stockholm
CONTAINER_NAME = stockholm_container

.PHONY: all build run exec down clean fclean re status logs

all: build run

build:
	@printf "Building...\n"
	@docker build -t $(IMAGE_NAME) .

run:
	@docker run -d --name $(CONTAINER_NAME) $(IMAGE_NAME)

exec:
	@docker exec -it $(CONTAINER_NAME) bash

down:
	@printf "Stopping \n"
	@if [ ! -z "$$(docker ps -aq -f name=$(CONTAINER_NAME))" ]; then \
		docker stop $(CONTAINER_NAME); \
	else \
		printf "Container $(CONTAINER_NAME) does not exist, skipping stop.\n"; \
	fi

re: down all

clean: down
	@printf "Cleaning \n"
	@if [ ! -z "$$(docker ps -aq -f name=$(CONTAINER_NAME))" ]; then \
		docker rm -f $(CONTAINER_NAME); \
	else \
		printf "Container $(CONTAINER_NAME) does not exist, skipping removal.\n"; \
	fi

	@if [ ! -z "$$(docker images -q $(IMAGE_NAME))" ]; then \
		docker rmi -f $(IMAGE_NAME); \
	else \
		printf "Image $(IMAGE_NAME) does not exist, skipping removal.\n"; \
	fi
	@docker system prune -f
	@printf "Cleaning \n"

status:
	@docker ps -a
	@docker images -a
	@docker volume ls

logs:
	@docker logs $(CONTAINER_NAME)
