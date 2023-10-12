import os
from pathlib import Path
import tempfile
import time

from api.src.jobs import delete_all_files_older_than


def test_delete_all_files_older_than() -> None:
    """Test if old enough files are deleted properly."""
    with tempfile.TemporaryDirectory() as tempdir:
        file1 = tempfile.NamedTemporaryFile(dir=tempdir)
        file2 = tempfile.NamedTemporaryFile(dir=tempdir)
        dir1 = tempfile.TemporaryDirectory(dir=tempdir)
        tempfile.NamedTemporaryFile(dir=dir1.name)

        now = time.time()
        modified_time = now - 3600

        os.utime(file2.name, (modified_time, modified_time))
        os.utime(dir1.name, (modified_time, modified_time))

        delete_all_files_older_than(tempdir, 3600)

        files = os.listdir(tempdir)
        assert Path(file1.name).name in files
        assert not Path(file2.name).name in files
        assert not Path(dir1.name).name in files
