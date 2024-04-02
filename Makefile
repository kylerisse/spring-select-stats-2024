lint:
	nix-shell --command 'pylint *.py'

test:
	nix-shell --command 'pytest *.py'

build: clean
	nix-shell --command 'python3 generate.py'

clean:
	rm -v output_* || exit 0
