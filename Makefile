all:

run :
	@chmod +x automation.sh
	@bash automation.sh

git :
	@python3 git.py
