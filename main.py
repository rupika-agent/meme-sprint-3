"""Copy entry.png to the output directory and verify it byte for byte."""

import hashlib
import shutil
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "entry.png"
OUTPUT_DIR = Path("/output")
DESTINATION = OUTPUT_DIR / "entry.png"


def sha256_of(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    if not SOURCE.exists():
        raise SystemExit("entry.png not found next to main.py")
    if SOURCE.stat().st_size > 1_048_576:
        raise SystemExit("entry.png exceeds the 1 MiB gate")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, DESTINATION)
    source_hash = sha256_of(SOURCE)
    dest_hash = sha256_of(DESTINATION)
    assert source_hash == dest_hash, "copy does not match source"
    print(source_hash)


if __name__ == "__main__":
    main()
