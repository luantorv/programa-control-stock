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
        python = pkgs.python312;

        # Copia el código fuente al store de Nix (sin archivos .git ni .nix)
        archivos_instalados = pkgs.stdenv.mkDerivation {
          pname = "control-stock";
          version = "0.1.0";
          src = pkgs.lib.cleanSource ./.;
          dontBuild = true;
          installPhase = ''
            mkdir -p $out/lib/control-stock
            cp -r . $out/lib/control-stock/
          '';
        };

        # Wrapper que configura XDG e inicializa los datos en el primer uso
        paquete = pkgs.writeShellScriptBin "control-stock" ''
          export CONTROL_STOCK_DATOS_DIR="''${XDG_DATA_HOME:-$HOME/.local/share}/control-stock"

          if [ ! -f "$CONTROL_STOCK_DATOS_DIR/users.csv" ]; then
            mkdir -p "$CONTROL_STOCK_DATOS_DIR"
            cp ${archivos_instalados}/lib/control-stock/datos/users.csv "$CONTROL_STOCK_DATOS_DIR/users.csv"
            cp ${archivos_instalados}/lib/control-stock/datos/productos.csv "$CONTROL_STOCK_DATOS_DIR/productos.csv"
            cp ${archivos_instalados}/lib/control-stock/datos/cierre_diario.csv "$CONTROL_STOCK_DATOS_DIR/cierre_diario.csv"
          fi

          exec ${python}/bin/python3 ${archivos_instalados}/lib/control-stock/main.py "$@"
        '';
      in
      {
        packages.default = paquete;

        apps.default = {
          type = "app";
          program = "${paquete}/bin/control-stock";
        };

        devShells.default = pkgs.mkShell {
          packages = [ python ];
        };
      }
    );
}
