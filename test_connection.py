#!/usr/bin/env python3
"""Smoke test: confirms looker.ini credentials can actually authenticate.

Runs a single read-only API call (GET /user, i.e. "who am I") and prints the
logged-in user. Doesn't touch any dashboards, looks, or folders — safe to
run against prod. Use this to confirm the base_url/client_id/client_secret
in looker.ini are correct before running lock_folder.py for real.
"""

import argparse
import os
import sys

import looker_sdk


def main() -> None:
    parser = argparse.ArgumentParser(description="Test that looker.ini credentials can authenticate")
    parser.add_argument("--config", default="looker.ini", help="Path to looker_sdk credentials file (default: looker.ini)")
    args = parser.parse_args()

    if not os.path.exists(args.config):
        sys.exit(f"Error: credentials file '{args.config}' not found. Run setup_credentials.py first.")

    sdk = looker_sdk.init40(config_file=args.config)

    try:
        me = sdk.me(fields="id,display_name,email")
    except Exception as e:
        sys.exit(f"Login failed: {e}")

    print("Login succeeded.")
    print(f"  User ID:  {me.id}")
    print(f"  Name:     {me.display_name}")
    print(f"  Email:    {me.email}")


if __name__ == "__main__":
    main()
