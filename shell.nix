{ pkgs ? import <nixpkgs> { } }:

with pkgs;

mkShell rec {
  nativeBuildInputs = [
    pkg-config
  ];
  buildInputs = [
    glib
    glibc
    python311Packages.numpy
    python311Packages.beautifulsoup4
  ];
  LD_LIBRARY_PATH = lib.makeLibraryPath buildInputs;
}

