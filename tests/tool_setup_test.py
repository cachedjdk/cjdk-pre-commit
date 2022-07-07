# This file is part of cjdk-pre-commit.
# Copyright 2022 Board of Regents of the University of Wisconsin System
# SPDX-License-Identifier: MIT

import sys
from pathlib import Path
from urllib.parse import urlparse

import cjdk
import pytest

from cjdk_pre_commit.__main__ import tool_setup as f


def mock_cjdk_cache_file(name, url, filename):
    parts = urlparse(url)
    assert parts.scheme == "https"
    return Path("CACHED_FILE", filename)


def mock_cjdk_cache_package(name, url):
    parts = urlparse(url)
    assert parts.scheme in ("tgz+https", "zip+https")
    archive_name = parts.path.split("/")[-1]
    return Path(f"CACHED_DIR-{archive_name}")


def test_checkstyle(monkeypatch):
    monkeypatch.setattr(cjdk, "cache_file", mock_cjdk_cache_file)

    with pytest.raises(ValueError):
        f("checkstyle", "VERSION", [], "blah", [])

    assert f("checkstyle", "VERSION", [], None, []) == (
        [
            "java",
            "-jar",
            str(Path("CACHED_FILE", "checkstyle-VERSION-all.jar")),
        ],
        {},
    )

    assert f("checkstyle", "VERSION", ["x", "y"], None, ["z", "w"]) == (
        [
            "java",
            "x",
            "y",
            "-jar",
            str(Path("CACHED_FILE", "checkstyle-VERSION-all.jar")),
            "z",
            "w",
        ],
        {},
    )


def test_google_java_format(monkeypatch):
    monkeypatch.setattr(cjdk, "cache_file", mock_cjdk_cache_file)

    with pytest.raises(ValueError):
        f("google-java-format", "VERSION", [], "blah", [])

    assert f("google-java-format", "VERSION", [], None, []) == (
        [
            "java",
            "-jar",
            str(
                Path("CACHED_FILE", "google-java-format-VERSION-all-deps.jar")
            ),
        ],
        {},
    )

    assert f(
        "google-java-format", "VERSION", ["x", "y"], None, ["z", "w"]
    ) == (
        [
            "java",
            "x",
            "y",
            "-jar",
            str(
                Path("CACHED_FILE", "google-java-format-VERSION-all-deps.jar")
            ),
            "z",
            "w",
        ],
        {},
    )


def test_pmd(monkeypatch):
    monkeypatch.setattr(cjdk, "cache_package", mock_cjdk_cache_package)

    with pytest.raises(ValueError):
        f("pmd", "VERSION", ["blah"], None, [])

    bin_path = Path("CACHED_DIR-pmd-bin-VERSION.zip", "pmd-bin-VERSION", "bin")
    script = (
        [str(bin_path / "pmd.bat")]
        if sys.platform == "win32"
        else [str(bin_path / "run.sh"), "pmd"]
    )

    assert f("pmd", "VERSION", [], None, []) == (
        script,
        {},
    )

    assert f("pmd", "VERSION", [], "x y", ["z", "w"]) == (
        script + ["z", "w"],
        {"PMD_JAVA_OPTS": "x y"},
    )


def test_cpd(monkeypatch):
    monkeypatch.setattr(cjdk, "cache_package", mock_cjdk_cache_package)

    with pytest.raises(ValueError):
        f("cpd", "VERSION", ["blah"], None, [])

    bin_path = Path("CACHED_DIR-pmd-bin-VERSION.zip", "pmd-bin-VERSION", "bin")
    script = (
        [str(bin_path / "cpd.bat")]
        if sys.platform == "win32"
        else [str(bin_path / "run.sh"), "cpd"]
    )

    assert f("cpd", "VERSION", [], None, []) == (
        script,
        {},
    )

    assert f("cpd", "VERSION", [], "x y", ["z", "w"]) == (
        script + ["z", "w"],
        {"PMD_JAVA_OPTS": "x y"},
    )
