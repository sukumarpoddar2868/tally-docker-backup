import os
import shutil
import sys
from datetime import datetime, timedelta
from pathlib import Path


# ============================================================
# Configuration
# ============================================================

SOURCE_DIR = Path(
    os.getenv("SOURCE_DIR", "/data/source")
)

BACKUP_ROOT = Path(
    os.getenv("BACKUP_ROOT", "/data/backups/tally")
)

FIFTEEN_MIN_DIR = BACKUP_ROOT / "15min"
DAILY_DIR = BACKUP_ROOT / "daily"

# Retention policy
FIFTEEN_MIN_RETENTION_DAYS = int(
    os.getenv("FIFTEEN_MIN_RETENTION_DAYS", "7")
)

DAILY_RETENTION_DAYS = int(
    os.getenv("DAILY_RETENTION_DAYS", "30")
)


# ============================================================
# Directory setup
# ============================================================

def ensure_directories():
    """Create backup directories if they don't exist."""

    FIFTEEN_MIN_DIR.mkdir(parents=True, exist_ok=True)
    DAILY_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# Source validation
# ============================================================

def check_source():
    """Check whether Tally backup data exists."""

    if not SOURCE_DIR.exists():
        print(f"[ERROR] Source directory does not exist: {SOURCE_DIR}")
        return False

    if not any(SOURCE_DIR.iterdir()):
        print(f"[WARNING] Source directory is empty: {SOURCE_DIR}")
        return False

    return True


# ============================================================
# Copy backup data
# ============================================================

def copy_backup(destination):
    """
    Copy everything from the Tally backup directory
    into the specified destination.
    """

    destination.mkdir(parents=True, exist_ok=True)

    for item in SOURCE_DIR.iterdir():

        target = destination / item.name

        if item.is_dir():

            shutil.copytree(
                item,
                target,
                dirs_exist_ok=True
            )

        else:

            shutil.copy2(
                item,
                target
            )


# ============================================================
# 15-minute snapshot
# ============================================================

def create_snapshot():

    print("[INFO] Creating 15-minute snapshot...")

    if not check_source():
        return

    timestamp = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    destination = FIFTEEN_MIN_DIR / timestamp

    try:

        copy_backup(destination)

        print(
            f"[SUCCESS] 15-minute snapshot created: "
            f"{destination}"
        )

    except Exception as error:

        print(
            f"[ERROR] Snapshot failed: {error}"
        )

        if destination.exists():
            shutil.rmtree(
                destination,
                ignore_errors=True
            )

        raise


# ============================================================
# Daily snapshot
# ============================================================

def create_daily_backup():

    print("[INFO] Creating daily snapshot...")

    if not check_source():
        return

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )

    destination = DAILY_DIR / today

    # Don't create the same daily backup twice
    if destination.exists():

        print(
            f"[INFO] Daily snapshot already exists: "
            f"{destination}"
        )

        return

    try:

        copy_backup(destination)

        print(
            f"[SUCCESS] Daily snapshot created: "
            f"{destination}"
        )

    except Exception as error:

        print(
            f"[ERROR] Daily backup failed: {error}"
        )

        if destination.exists():
            shutil.rmtree(
                destination,
                ignore_errors=True
            )

        raise


# ============================================================
# Cleanup old backups
# ============================================================

def remove_old_backups(directory, retention_days):

    if not directory.exists():
        return

    cutoff = datetime.now() - timedelta(
        days=retention_days
    )

    for item in directory.iterdir():

        if not item.is_dir():
            continue

        modified_time = datetime.fromtimestamp(
            item.stat().st_mtime
        )

        if modified_time < cutoff:

            print(
                f"[INFO] Removing old backup: {item}"
            )

            shutil.rmtree(
                item,
                ignore_errors=True
            )


def cleanup():

    print("[INFO] Starting cleanup...")

    remove_old_backups(
        FIFTEEN_MIN_DIR,
        FIFTEEN_MIN_RETENTION_DAYS
    )

    remove_old_backups(
        DAILY_DIR,
        DAILY_RETENTION_DAYS
    )

    print("[SUCCESS] Cleanup completed.")


# ============================================================
# Main
# ============================================================

def main():

    ensure_directories()

    if len(sys.argv) < 2:

        print(
            "Usage:\n"
            "  python backup.py snapshot\n"
            "  python backup.py daily\n"
            "  python backup.py cleanup"
        )

        sys.exit(1)

    command = sys.argv[1]

    if command == "snapshot":

        create_snapshot()

    elif command == "daily":

        create_daily_backup()

    elif command == "cleanup":

        cleanup()

    else:

        print(
            f"[ERROR] Unknown command: {command}"
        )

        sys.exit(1)


if __name__ == "__main__":
    main()
