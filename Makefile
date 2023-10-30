ROOT_URL ?= "https://classificados.inf.ufsc.br/latestads.php"
SINCE ?= $(shell date +"%Y-%m-%d")
UNTIL ?= $(shell date +"%Y-%m-%d")

run:
	poetry run python main.py $(ROOT_URL) $(SINCE) $(UNTIL)
