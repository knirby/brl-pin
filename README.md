# brl-pin

`brl-pin` manages command pins in Bedrock Linux's `cross-bin` configuration.

Requires Bedrock Linux and Python 3. Listing pins does not need root. Adding or removing a pin updates `/bedrock/etc/bedrock.conf` and runs `brl apply`, so those commands must be run as root.

```sh
brl-pin --list
sudo brl-pin <command> <stratum>
sudo brl-pin <command> <stratum> /path/to/command
sudo brl-pin --rm <command>
```

When no path is given, `brl-pin` uses `/usr/bin/<command>`. Licensed under GPL-3.0-only; see [LICENSE](LICENSE).
