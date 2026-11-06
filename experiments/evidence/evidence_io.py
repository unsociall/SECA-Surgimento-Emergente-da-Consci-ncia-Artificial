"""Publication of verified laboratory artifacts without in-place fallback."""
import hashlib
import os
from pathlib import Path
from uuid import uuid4


def _sync_directory(directory):
    try:
        fd = os.open(directory, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    except OSError:
        return False
    try:
        os.fsync(fd)
        return True
    except OSError:
        return False
    finally:
        os.close(fd)


def publish_artifact(destination, producer, *, protected_paths=()):
    """Stage, fsync, hash and replace one file; return publication metadata.

    A producer writes to the supplied binary handle or SQLite staging path.
    Existing output bytes are preserved on failures before os.replace.
    The directory fsync result is reported separately from file publication.
    """
    destination = Path(destination).expanduser().absolute()
    if destination.is_symlink():
        raise ValueError("artifact destination must not be a symlink")
    if destination.exists() and not destination.is_file():
        raise ValueError("artifact destination must be a regular file")
    resolved = os.path.normcase(str(destination.resolve()))
    for source in protected_paths:
        source = Path(source)
        same_name = resolved == os.path.normcase(str(source.resolve()))
        same_file = destination.exists() and source.exists() and os.path.samefile(destination, source)
        if same_name or same_file:
            raise ValueError("artifact destination overlaps a live database or journal")

    staging = destination.with_name(f".{destination.name}.{uuid4().hex}.partial")
    # A collision is an error, never a reason to reuse a pre-existing file.
    fd = os.open(staging, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0), 0o600)
    try:
        handle = os.fdopen(fd, "wb")
        fd = None  # the file object owns the descriptor from here
        with handle:
            stats = producer(handle, staging)
            handle.flush()
            os.fsync(handle.fileno())
        digest = hashlib.sha256()
        size = 0
        with staging.open("rb") as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(block)
                size += len(block)
        os.replace(staging, destination)
        directory_fsynced = _sync_directory(destination.parent)
        return {**stats, "path": str(destination), "sha256": digest.hexdigest(),
                "size_bytes": size, "file_fsynced": True,
                "directory_fsynced": directory_fsynced}
    finally:
        if fd is not None:
            os.close(fd)
        staging.unlink(missing_ok=True)
