{ pkgs ? import <nixpkgs> { } }:

with pkgs;

let
  python = python312.withPackages
    (pythonPackages: with pythonPackages; [ jinja2 pylint pytest ]);
  utils = [ gnumake ];

in
mkShell {
  buildInputs = [ python utils ];
}
