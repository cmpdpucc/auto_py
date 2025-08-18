nix
{
  description = "A simple Python development environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable"; # Or the channel you prefer
  };

  outputs = { self, nixpkgs }:
    let
      pkgs = nixpkgs.legacyPackages.${nixpkgs.system};
      devNix = import ./.idx/dev.nix { inherit pkgs; };
    in
    {
      devShells.${nixpkgs.system}.default = pkgs.mkShell {
        packages = devNix.packages;
        shellHook = ''
          # Add any shell-specific configurations here
        '';
        # You can also include env variables from devNix.env here if needed
        # e.g., nativeBuildInputs = [ pkgs.makeWrapper ];
        #         postShellHook = ''
        #           wrapProgram $EDITOR --set someVar someValue
        #         '';
      };
    };
}
