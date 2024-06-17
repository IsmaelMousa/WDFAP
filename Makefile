help h:
	@echo "Available Commands:"
	@sed -n "/^[a-zA-Z0-9_.]*:/s/:.*//p" < Makefile | GREP_COLOR="01;34" grep --color=always -E "^[a-zA-Z0-9_.]*"

setup:
	@echo "\e[34m----------------------------Setup In Progress----------------------------\e[0m"
	@pip install .

start:
	@echo "\e[34m----------------------------Welcome to WDFAP!----------------------------\e[0m"
	@python3 main.py

# Development
setup-dev:
	@echo "\e[34m----------------------------Setup Development----------------------------\e[0m"
	@pip install .
	@pip install -r requirements-dev.txt

lint:
	@echo "\e[34m----------------------------Check Linting----------------------------\e[0m"
	@pylint "**/*.py"

test:
	@echo "\e[34m----------------------------Check Testing----------------------------\e[0m"
	@pytest --cache-clear

coverage:
	@echo "\e[34m----------------------------Check Coverage----------------------------\e[0m"
	@pytest --cache-clear --cov --cov-report=term-missing

docs:
	@echo "\e[34m----------------------------Generate Documentation----------------------------\e[0m"
	@sphinx-apidoc -o docs ..

version:
	@echo "\e[34m----------------------------WDFAP Version----------------------------\e[0m"
	@semantic-release -vv version --print
