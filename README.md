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

Run this block to clone the repository if needed and install or overwrite `brl-pin` in `/usr/local/bin`:

```sh
cd /tmp
if [ ! -d brl-pin/.git ]; then
	git clone https://github.com/knirby/brl-pin.git
fi
cd /tmp/brl-pin
sudo python3 brl-pin --install
```

Install replaces an existing executable and copies only `brl-pin`; it does not edit shell configuration. Without `sudo`, install works only when `~/bin` or `~/.local/bin` already exists on `PATH` and is writable.

## Update or remove

```sh
sudo brl-pin --update
sudo brl-pin --uninstall
```

Update fetches the latest version from GitHub and replaces the installed executable. Uninstall removes only that executable.
