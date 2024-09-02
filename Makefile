docker-shell:
	docker compose run --rm --user="`id -u`:`id -g`" app bash

shell:
	make docker-shell

run:
	docker compose run --rm --user="`id -u`:`id -g`" app

send-message:
	curl -X PUT -H "Content-Type: application/json" -d "{\"message\": \"hello world sent at $(shell date -u +'%Y-%m-%dT%H:%M:%SZ')\"}" http://127.0.0.1:8080

