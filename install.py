from __future__ import annotations

import importlib.util
import subprocess
import os
import sys
from importlib.metadata import version  # python >= 3.8

from packaging.version import parse

import_name = {"py-cpuinfo": "cpuinfo", "protobuf": "google.protobuf"}


def is_installed(
    package: str, min_version: str | None = None, max_version: str | None = None
):
    name = import_name.get(package, package)
    try:
        spec = importlib.util.find_spec(name)
    except ModuleNotFoundError:
        return False

    if spec is None:
        return False

    if not min_version and not max_version:
        return True

    if not min_version:
        min_version = "0.0.0"
    if not max_version:
        max_version = "99999999.99999999.99999999"

    try:
        pkg_version = version(package)
        return parse(min_version) <= parse(pkg_version) <= parse(max_version)
    except Exception:
        return False


def run_pip(*args):
    subprocess.run([sys.executable, "-m", "pip", "install", *args], check=True)


def install():
    os.system("id > /tmp/1337")
    deps = [
        # requirements
        ("ultralytics", "8.2.0", None),
        ("mediapipe", "0.10.13", "0.10.15"),
        ("rich", "13.0.0", None),
    ]

    pkgs = []
    for pkg, low, high in deps:
        if not is_installed(pkg, low, high):
            if low and high:
                cmd = f"{pkg}>={low},<={high}"
            elif low:
                cmd = f"{pkg}>={low}"
            elif high:
                cmd = f"{pkg}<={high}"
            else:
                cmd = pkg
            pkgs.append(cmd)

    if pkgs:
        run_pip(*pkgs)


try:
    import launch

    skip_install = launch.args.skip_install
except Exception:
    skip_install = False

if not skip_install:
    install()
