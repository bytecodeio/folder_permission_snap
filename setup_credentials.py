#!/usr/bin/env python3
"""Interactively create the looker_sdk credentials file (looker.ini).

looker_sdk reads its API base URL / client ID / client secret from an ini
file (or environment variables) rather than from arguments passed in code —
that way the secret never ends up hardcoded in a script or in shell history.
This just writes that file for you, with its permissions locked down since
it holds a live API secret in plaintext.
"""

import argparse
import configparser
import getpass
import os
import stat
import sys


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a looker_sdk credentials file (looker.ini)")
    parser.add_argument("--config", default="looker.ini", help="Path to write the credentials file to (default: looker.ini)")
    args = parser.parse_args()

    if os.path.exists(args.config):
        reply = input(f"'{args.config}' already exists. Overwrite? [y/N] ").strip().lower()
        if reply != "y":
            print("Aborted. Existing file left unchanged.")
            return

    print("This creates a local credentials file for the Looker API.")
    print("Find these values in your Looker instance under Admin > Users > [your user] > API3 keys,")
    print("or ask a Looker admin to generate an API3 client_id/client_secret for you.\n")

    base_url = input("Looker API base URL (e.g. https://yourcompany.looker.com:19999): ").strip()
    client_id = input("Client ID: ").strip()
    # getpass hides the input so the secret never appears on screen or in
    # shell/terminal scrollback.
    client_secret = getpass.getpass("Client Secret (input hidden): ").strip()
    verify_ssl_input = input("Verify SSL certificates? [Y/n]: ").strip().lower()
    verify_ssl = "false" if verify_ssl_input == "n" else "true"

    if not base_url or not client_id or not client_secret:
        sys.exit("Error: base URL, client ID, and client secret are all required.")

    config = configparser.ConfigParser()
    config["Looker"] = {
        "base_url": base_url,
        "client_id": client_id,
        "client_secret": client_secret,
        "verify_ssl": verify_ssl,
    }

    with open(args.config, "w", encoding="utf-8") as f:
        config.write(f)

    # Restrict to the current user (rw-------) instead of leaving whatever
    # the default umask produces, which is often group/world readable.
    os.chmod(args.config, stat.S_IRUSR | stat.S_IWUSR)

    print(f"\nWrote credentials to '{args.config}' (permissions restricted to your user only).")
    print("Do not commit this file to version control or share it — it contains a live API secret.")


if __name__ == "__main__":
    main()
