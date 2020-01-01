##
# Data Engineering Nanodegree
#
# @file
# @version 0.1

all: install_deps run_containers

run_containers:
	docker-compose up -d

install_deps:
	poetry install

# end
