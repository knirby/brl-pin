# brl-tools

Tools that smooth over the rough edges of a [Bedrock Linux](https://bedrocklinux.org) desktop. They need Bedrock and Python 3, and work with any desktop environment that follows the freedesktop specifications. Licensed under GPL-3.0-only; see [LICENSE](LICENSE).

| Tool | What it does |
| --- | --- |
| `brl-pin` | makes a command run from the stratum you choose |
| `brl-desktop` | gives apps from every stratum clean, live launchers and icons |
| `brl-brand` | presents a hijacked install as Bedrock Linux, from boot splash to About page |

## Install

```sh
git clone https://github.com/knirby/brl-tools.git
cd brl-tools
sudo ./install
```

`install` copies the tools to `/usr/local/bin` and the logos to `/usr/local/share/brl-tools/assets`. It is safe to rerun and changes no configuration; set each tool up with its own command below.

## brl-pin

```sh
brl-pin --list
sudo brl-pin <command> <stratum>
sudo brl-pin --rm <command>
```

`sudo brl-pin code fedora` makes `code` resolve from `fedora` by default. `brl-pin` asks Bedrock to resolve the command inside the requested stratum, writes that stratum and path to `[cross-bin]` in `/bedrock/etc/bedrock.conf`, and runs `brl apply`. With `brl-desktop` enabled, the pinned stratum's launcher also wins in the app menu.

`sudo brl-pin --desktop <command>` and `--desktop-rm` write or remove a user-local launcher that follows the pin. `brl-desktop` makes them unnecessary, but they still work without it. `sudo brl-pin --update` and `--uninstall` update or remove the installed `brl-pin`.

## brl-desktop

```sh
sudo brl-desktop enable
brl-desktop status
```

Bedrock's crossfs shows other strata's launchers under `/bedrock/cross`, a FUSE mount. FUSE raises no inotify events for changes made beneath it, so desktops never notice an app being installed or removed until the next login, and the merged hicolor directory carries one stratum's icon cache, which hides every other stratum's icons.

`brl-desktop` writes real launchers to `/bedrock/var/brl-desktop/share` instead, placed first in `XDG_DATA_DIRS`:

- each launcher runs its app through `strat`, with absolute `Icon=` and `Path=` references resolved inside the app's stratum, and `TryExec=` checked there;
- icons from every stratum share one hicolor theme with a fresh cache;
- `update-desktop-database` registers every app's MIME types, so links and files open in apps from any stratum;
- when two strata offer the same app, the stratum its command is pinned to wins, then the init stratum, then `[cross] priority`;
- a root service rebuilds all of it within seconds of a package manager touching any stratum.

A per-user service keeps `~/.local` tidy. Once an app is uninstalled, it moves your launcher overrides for it, such as a menu editor's copy, to `~/.local/share/brl-desktop/orphans`. It also rebuilds two caches that menu editors and uninstalls leave stale: your `mimeinfo.cache`, without which an app whose icon you changed stops being registered for its file types, and your user icon theme caches, which otherwise name deleted files and make launchers draw nothing.

`enable` comments out crossfs's `applications` line in `bedrock.conf`, adds the directory to `XDG_DATA_DIRS`, installs and starts both services, and backs `bedrock.conf` up first. Log out and back in once afterwards. `sudo brl-desktop disable` undoes all of it.

## brl-brand

```sh
sudo brl-brand apply
brl-brand status
```

A hijack keeps the original distro's identity. `brl-brand` rebrands the init stratum, which boots the machine and runs the session:

- **os-release** takes Bedrock's name, version, logo and URLs, so About pages and boot messages say Bedrock Linux. `ID` and `VERSION_ID` keep the distro's values, which its package manager, dracut and kernel-install key on.
- **Logos** go into the hicolor theme under `/usr/local` as `bedrock-logo`, `-text` and `-text-dark`, the names freedesktop About pages derive from `LOGO`, with PNG copies in `/usr/local/share/pixmaps`. The wordmark PNGs are 240 px wide, the size of the distro's own greeter logos, because display managers draw a logo at its pixel size; point yours at `bedrock-logo-text-dark.png` for a dark login screen.
- **The boot splash** becomes a Plymouth theme with the logo, built on the distro's spinner theme. Every initramfs is rebuilt through `kernel-install` and kept only if it still holds systemd and the theme; otherwise the previous one is restored.
- **Boot menu entries** are retitled by that rebuild, and the firmware entry for systemd-boot is relabelled "Bedrock Linux".

A path unit reruns `brl-brand refresh` when a package update replaces the distro's os-release or `brl update` changes Bedrock's version. `sudo brl-brand revert` restores the distro's branding.

The logos in `assets/` are drawn by `assets/make-logos.py`. Bedrock's logo is ASCII art and no vector version is published, so the script draws each character as a stroke: the wordmark from the installer banner, the full form from [paradigm's gist](https://gist.github.com/paradigm/3319799), and the square mark from the favicon.

## Fixes worth knowing

Two Bedrock pitfalls found while building these tools, worth applying by hand:

- **dracut bundles every stratum's firmware.** Bedrock sets the kernel's `firmware_class.path` to `/bedrock/cross/firmware`, and dracut adds that path whenever `fw_dir` is unset, growing the initramfs by around 100 MB. Pin it to the init stratum's firmware in `/etc/dracut.conf.d/90-bedrock-firmware.conf`:

  ```sh
  fw_dir="/lib/firmware/updates /lib/firmware"
  ```

- **`/etc/sudoers.d` is per stratum,** so `sudo` rules there apply only to the stratum whose `sudo` runs, which breaks AUR helpers calling Arch's `sudo`. Marking the directory global in `bedrock.conf` does not work: etcfs shares the directory and its listing, but resolves each file inside it against the stratum's local `/etc`. Put shared rules in a real shared directory instead, and include it from the already global `/etc/sudoers` (validate with `visudo -c` first):

  ```sh
  #includedir /bedrock/etc/sudoers.d
  ```
