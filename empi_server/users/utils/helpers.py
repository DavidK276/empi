from pathlib import Path


def check_gnupg_homedir(gpghomedir: Path):
    if not gpghomedir.is_dir():
        gpghomedir.mkdir(mode=0o700)
        (gpghomedir / "private-keys-v1.d").mkdir()
