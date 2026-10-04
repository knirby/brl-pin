# brl-pin

`brl-pin` pins a direct shell command to be ran from a specific Bedrock Linux Strata by default.

Requires Bedrock Linux and Python 3. Listing pins does not need root. Adding or removing a pin updates `/bedrock/etc/bedrock.conf` and runs `brl apply`, so those commands must be run as root.

```sh
brl-pin --list
sudo brl-pin <command>
sudo brl-pin --rm <command>
```

Pinning asks `brl which` for the provider, resolves the executable with Bedrock, and writes that provider and path to `cross-bin`. Licensed under GPL-3.0-only; see [LICENSE](LICENSE).

## Install

Run this block of commands to:

Clone the repository in `/tmp`, then install the command in `~/.local/bin`:

```sh
cd /tmp
git clone https://github.com/knirby/brl-pin.git
cd brl-pin
python3 brl-pin --install
```

Install copies only `brl-pin` into a writable `~/.local/bin` or `~/bin` directory that is already on `PATH`. If neither directory is on `PATH`, add one yourself and rerun the install command.

## Update or remove

```sh
brl-pin --update
brl-pin --uninstall
```

Update fetches the latest version from GitHub and replaces the installed command. Uninstall removes only the installed command.
