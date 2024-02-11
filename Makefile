up:
	docker compose up -d --build
.PHONY: up

down:
	docker compose down
.PHONY: down

sync_benchmark_main:
	cd tests && ./run-main-sync.sh
.PHONY: sync_benchmark_main

sync_benchmark_PR:
	cd tests && ./run-PR-sync.sh
.PHONY: sync_benchmark_PR

async_benchmark_PR:
	cd tests && ./run-PR-async.sh
.PHONY: async_benchmark_PR
