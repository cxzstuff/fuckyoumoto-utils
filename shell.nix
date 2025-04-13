# It is suggested to use flake.nix, as it will also provide mtkclient
with import <nixpkgs> { };
mkShell {

  name = "mtkclient";

  buildInputs = with python3Packages; [
    pyserial
  ];

}
