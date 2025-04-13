{
  description = "fuckyoumoto utilities";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
    frostix = {
      url = "github:shomykohai/frostix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

 
  outputs = { self, nixpkgs, ...}@inputs: 
  let
    system = "x86_64-linux";
    pkgs = nixpkgs.legacyPackages.${system};
    frostix = inputs.frostix.packages.${system};
  in
  {
    devShells.${system}.default = pkgs.mkShell {
      packages = [
        pkgs.python3.pkgs.pyserial
        pkgs.python3
        
        # In case mtkclient complains about not being able to get configuration
        # make sure to include `programs.adb.enable = true;` in your configuration.nix
        # and to add your user to `adbusers` group.
        frostix.mtkclient-git
      ];
    };
  };
}
