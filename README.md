# brl-pin

`brl-pin` pins a command to the provider Bedrock currently selects for it.

Requires Bedrock Linux and Python 3. Listing pins does not need root. Adding or removing a pin updates `/bedrock/etc/bedrock.conf` and runs `brl apply`, so those commands must be run as root.

```sh
brl-pin --list
sudo brl-pin <command>
sudo brl-pin --rm <command>
```

Pinning asks `brl which` for the provider, resolves the executable with Bedrock, and writes that provider and path to `cross-bin`. Licensed under GPL-3.0-only; see [LICENSE](LICENSE).

## Install

Clone the repository once, then install it in `/usr/local/bin`:

```sh
cd /tmp
git clone https://github.com/knirby/brl-pin.git
cd brl-pin
sudo python3 brl-pin --install
```

If you already cloned the repository, just run `sudo python3 brl-pin --install` from that directory. Install copies only the executable to `/usr/local/bin`; it does not edit shell configuration. Without `sudo`, install works only when `~/bin` or `~/.local/bin` already exists on `PATH` and is writable.

## Update or remove

```sh
sudo brl-pin --update
sudo brl-pin --uninstall
```

Update fetches the latest version from GitHub and replaces the installed executable. Uninstall removes only that executable.
