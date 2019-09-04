"""Get information about this package."""


def info(system):
    """Get information about this package."""
    import googledevices.utils.const as package

    print("Projectname:  ", package.NAME)
    print("Version:      ", package.VERSION)
    print("GitHub link:  ", package.URLS.get("github"))
    print("PyPi link:    ", package.URLS.get("pypi"))
    print("Maintainers:")
    for maintainer in package.MAINTAINERS:
        print("    ", maintainer.get("name"), "(", maintainer.get("github"), ")")
    print("")
    if system:
        import platform

        print("")
        print("System:          ", platform.system())
        print("Version:         ", platform.version())
        print("Python version:  ", platform.python_version())
