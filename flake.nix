# SPDX-FileCopyrightText: 2026 Luis Reis Viera
# SPDX-License-Identifier: Apache-2.0

{
  description = "Programa de Control de Stock para un Supermercado";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-26.05";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        python = pkgs.python312.withPackages (ps: with ps; [
          # Aquí irían las librerías, en este caso no aplica
        ]);
      in
      {
        devShells.default = pkgs.mkShell {
          packages = [
            python
          ];

          #shellHook = ''
          #  '';
        };
      }
    );
}
