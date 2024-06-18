help h:
	@echo "Available Commands:"
	@sed -n "/^[a-zA-Z0-9_.]*:/s/:.*//p" < Makefile | GREP_COLOR="01;34" grep --color=always -E "^[a-zA-Z0-9_.]*"

setup:
	@echo "\e[34m=========================== Setup WDFAP ===========================\e[0m"
	@pip install .

start:
	@echo "\e[1;32m=========================== Welcome to WDFAP! ===========================\e[0m"
	@python3 main.py
	@echo "\e[1;32m=========================== Completed Successfully! ===========================\e[0m"

# Development Stage
setup-dev:
	@echo "\e[34m=========================== Setup Development ===========================\e[0m"
	@pip install .
	@pip install -r requirements-dev.txt

lint:
	@echo "\e[34m=========================== Check Linting ===========================\e[0m"
	@pylint "**/*.py"

test:
	@echo "\e[34m=========================== Check Testing ===========================\e[0m"
	@pytest --cache-clear

coverage:
	@echo "\e[34m=========================== Check Coverage ===========================\e[0m"
	@pytest --cache-clear --cov --cov-report=term-missing

# Automation Documentation
docs:
	@echo "\e[34m=========================== Generate Documentation ===========================\e[0m"
	@sphinx-apidoc -o docs .

# Release Information
version:
	@echo "\e[34m=========================== WDFAP Version ===========================\e[0m"
	@semantic-release -vv version --print
