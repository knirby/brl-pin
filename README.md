# brl-pin

`brl-pin` makes a command run from the stratum you choose when you call it normally in your shell.

Requires Bedrock Linux and Python 3. Listing pins does not need root. Adding or removing a pin updates `/bedrock/etc/bedrock.conf` and runs `brl apply`, so those commands must be run as root. Desktop entry synchronization also requires root.

```sh
brl-pin --list
sudo brl-pin <command> <stratum>
sudo brl-pin --rm <command>
sudo brl-pin --desktop <command>
```

For example, `sudo brl-pin code fedora` makes `code` resolve from `fedora` by default. `brl-pin` asks Bedrock to resolve the command inside the requested stratum, then writes that stratum and path to `cross-bin`. Licensed under GPL-3.0-only; see [LICENSE](LICENSE).

`sudo brl-pin --desktop code` updates desktop launchers whose `Exec` command is `code` to run the executable from its current pin. If no matching launcher exists, it creates one in the invoking user's `~/.local/share/applications` directory. The command does not create or change the pin itself.

## Install

Run this block to clone the repository if needed and install or overwrite `brl-pin` in `/usr/local/bin`:

```sh
cd /tmp
if [ -d brl-pin/.git ]; then
	git -C brl-pin pull --ff-only
else
	git clone https://github.com/knirby/brl-pin.git
fi
cd /tmp/brl-pin
sudo install -D -m 755 brl-pin /usr/local/bin/brl-pin
```

This is safe to rerun: it updates an existing clone and overwrites the installed executable. It only copies `brl-pin` and does not edit shell configuration.

## Update or remove

```sh
sudo brl-pin --update
sudo brl-pin --uninstall
```

Update fetches the latest version from GitHub and replaces the installed executable. Uninstall removes only that executable.
