nix
{
  description = "A basic Python development environment using .idx/dev.nix";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }: {
    devShells.default = nixpkgs.legacyPackages.${nixpkgs.system}.callPackage ./.idx/dev.nix {};
  };
}