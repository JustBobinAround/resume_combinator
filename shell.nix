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
  ];
  LD_LIBRARY_PATH = lib.makeLibraryPath buildInputs;
}

