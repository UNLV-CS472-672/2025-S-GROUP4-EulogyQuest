#!/usr/bin/env python3
#
# ai-gen start (ChatGPT-4o-mini-high, 0)
##!/usr/bin/env python3
import argparse
import subprocess
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(
        description="Upload an EverQuest quest trigger via FTP to your AWS game server."
    )
    
    parser.add_argument(
        "name",
        help="Target name (e.g. \"Robin Williams\"). Use quotes if your shell needs them."
    )
    args = parser.parse_args()

    # Convert "First Last" → "First_Last"
    underscored = "_".join(args.name.split())
    filename = f"Eulogyquest_{underscored}.trigger"
    local_file = Path(filename)

    # Create the trigger file if it doesn't exist
    if not local_file.exists():
        print(f"Creating trigger file: {filename}")
        try:
            local_file.touch()
        except Exception as e:
            print(f"Error creating file '{filename}': {e}", file=sys.stderr)
            sys.exit(1)

    # FTP credentials & destination
    ftp_user     = "quests"
    ftp_password = "BU5H9LaaGXe8cUj6SIZI0eXpGeDmVJW"
    ftp_host     = "184.169.160.73"
    remote_dir   = "tutorialb"
    remote_path  = f"{remote_dir}/{filename}"
    url          = f"ftp://{ftp_user}:{ftp_password}@{ftp_host}/{remote_path}"

    cmd = [
        "curl",
        "--ftp-pasv",
        "-T", filename,
        url
    ]

    print(f"Uploading '{filename}' to '{ftp_host}/{remote_path}'...")
    try:
        subprocess.run(cmd, check=True)
        print("Upload successful.")
    except subprocess.CalledProcessError as e:
        print(f"Upload failed (exit {e.returncode}).", file=sys.stderr)
        sys.exit(e.returncode)

if __name__ == "__main__":
    main()


# ai-gen end