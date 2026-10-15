import zipfile

import pytest

from tbx11k import download


@pytest.fixture
def small_list_sizes(monkeypatch):
    monkeypatch.setattr(download, "EXPECTED_LIST_SIZES", {"TBX11K_train.txt": 2, "TBX11K_val.txt": 1})


def make_dataset(root, train_images=("health/h1.png", "tb/tb1.png"), val_images=("sick/s1.png",)):
    dataset_dir = root / "TBX11K"
    (dataset_dir / "lists").mkdir(parents=True)
    for list_name, images in [("TBX11K_train.txt", train_images), ("TBX11K_val.txt", val_images)]:
        (dataset_dir / "lists" / list_name).write_text("\n".join(images) + "\n")
        for image in images:
            (dataset_dir / "imgs" / image).parent.mkdir(parents=True, exist_ok=True)
            (dataset_dir / "imgs" / image).touch()
    return dataset_dir


def test_check_accepts_complete_dataset(tmp_path, small_list_sizes):
    download.check(make_dataset(tmp_path))


def test_check_rejects_missing_image(tmp_path, small_list_sizes):
    dataset_dir = make_dataset(tmp_path)
    (dataset_dir / "imgs" / "tb" / "tb1.png").unlink()
    with pytest.raises(download.IncompleteDatasetError, match="tb1.png"):
        download.check(dataset_dir)


def test_check_rejects_wrong_image_count(tmp_path, small_list_sizes):
    dataset_dir = make_dataset(tmp_path, train_images=("health/h1.png",))
    with pytest.raises(download.IncompleteDatasetError, match="TBX11K_train.txt"):
        download.check(dataset_dir)


def test_download_extracts_existing_archive_without_new_download(tmp_path, small_list_sizes, monkeypatch):
    source_dir = make_dataset(tmp_path / "source")
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    with zipfile.ZipFile(data_dir / "TBX11K.zip", "w") as archive:
        for path in source_dir.rglob("*"):
            archive.write(path, path.relative_to(source_dir.parent))
    monkeypatch.setattr(download.gdown, "download", lambda **kwargs: pytest.fail("must not download again"))

    download.download(data_dir)

    assert (data_dir / "TBX11K" / "imgs" / "tb" / "tb1.png").exists()
