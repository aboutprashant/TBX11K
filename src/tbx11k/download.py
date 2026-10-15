"""Download the TBX11K dataset from the official Google Drive file and check that it is complete.

Usage: uv run python -m tbx11k.download [DATA_DIR]
"""

import argparse
import zipfile
from pathlib import Path

import gdown

# Official link from https://github.com/yun-liu/Tuberculosis (TBX11K.zip, CC BY 4.0).
GOOGLE_DRIVE_FILE_ID = "1r-oNYTPiPCOUzSjChjCIYTdkjBTugqxR"
# Image counts from the paper. The test labels are not public, so only train and val are checked.
EXPECTED_LIST_SIZES = {"TBX11K_train.txt": 6600, "TBX11K_val.txt": 1800}


class IncompleteDatasetError(Exception):
    pass


def download(data_dir: Path) -> Path:
    archive = data_dir / "TBX11K.zip"
    if not archive.exists():
        partial = data_dir / "TBX11K.zip.part"
        gdown.download(id=GOOGLE_DRIVE_FILE_ID, output=str(partial), resume=True)
        partial.rename(archive)
    with zipfile.ZipFile(archive) as zip_file:
        zip_file.extractall(data_dir)  # zipfile drops ".." and absolute paths, so files stay in data_dir.
    dataset_dir = data_dir / "TBX11K"
    check(dataset_dir)
    return dataset_dir


def check(dataset_dir: Path) -> None:
    for list_name, expected_size in EXPECTED_LIST_SIZES.items():
        images = (dataset_dir / "lists" / list_name).read_text().split()
        if len(images) != expected_size:
            raise IncompleteDatasetError(f"{list_name} has {len(images)} images, expected {expected_size}")
        missing = [image for image in images if not (dataset_dir / "imgs" / image).is_file()]
        if missing:
            raise IncompleteDatasetError(f"{list_name}: {len(missing)} images are missing, for example {missing[0]}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("data_dir", nargs="?", type=Path, default=Path("data"))
    data_dir = parser.parse_args().data_dir
    data_dir.mkdir(parents=True, exist_ok=True)
    print(f"Dataset is complete: {download(data_dir)}")
