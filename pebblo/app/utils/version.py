from importlib.metadata import PackageNotFoundError, version


def get_pebblo_version():
    try:
        ver = version("pebblo")
    except PackageNotFoundError:
        ver = "unknown"
    return ver
