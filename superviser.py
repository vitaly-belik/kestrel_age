# the file supervises another script (e.g. stream recording script and restarts it if necessery)

import subprocess
import sys
import time


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 restart_script.py <script_to_run.py> [args...]")
        sys.exit(1)

    target = sys.argv[1]
    args = sys.argv[2:]

    while True:
        print(f"Starting {target} {' '.join(args)}")
        try:
            completed = subprocess.run([sys.executable, target, *args])
        except KeyboardInterrupt:
            print("Interrupted. Exiting.")
            break
        except Exception as exc:
            print(f"Error running {target}: {exc}")
            print("Restarting in 1 second...")
            time.sleep(1)
            continue

        if completed.returncode == 0:
            print(f"{target} exited cleanly with code 0. No restart.")
            break

        print(f"{target} failed with exit code {completed.returncode}. Restarting in 1 second...")
        time.sleep(1)


if __name__ == "__main__":
    main()
