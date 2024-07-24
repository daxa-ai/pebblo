from importlib.metadata import version, PackageNotFoundError

def get_pebblo_version():
    try:
        ver =  version("pebblo")
    except PackageNotFoundError:
        ver = "unknown"
    return ver