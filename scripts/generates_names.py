"""Generate first and last name lists and write them to scripts/data/."""

import pathlib

from faker import Faker

COUNT = 10_000
DATA_DIR = pathlib.Path(__file__).parent / "data"


def generate_names(count: int = COUNT) -> None:
    """Write first_names.txt and last_names.txt to scripts/data/."""
    fake = Faker()
    DATA_DIR.mkdir(exist_ok=True)

    first_names = [fake.first_name() for _ in range(count)]
    last_names = [fake.last_name() for _ in range(count)]

    (DATA_DIR / "first_names.txt").write_text("\n".join(first_names))
    (DATA_DIR / "last_names.txt").write_text("\n".join(last_names))

    print(f"Wrote {count:,} names to {DATA_DIR}/")


if __name__ == "__main__":
    generate_names()
