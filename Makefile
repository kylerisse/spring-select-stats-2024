lint:
	nix-shell --command 'pylint *.py'

test:
	nix-shell --command 'pytest *.py'

build: clean
	nix-shell --command 'python3 generate.py'

clean:
	rm -rf __pycache__ || exit 0
	rm -rf .pytest_cache || exit 0
	rm -v output_* || exit 0
