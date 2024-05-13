help h:
	@echo "Available Commands:"
	@sed -n "/^[a-zA-Z0-9_.]*:/s/:.*//p" < Makefile | GREP_COLOR="01;34" grep --color=always -E "^[a-zA-Z0-9_.]*"

setup:
	@echo "\e[1;34mSetup In Progress...\e[0m"
	@pip install .

start:
	@echo "\e[1;34mWelcome to WDFAP!\e[0m"
	@python3 main.py
