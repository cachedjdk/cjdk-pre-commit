# This file is part of cjdk-pre-commit.
# Copyright 2022 Board of Regents of the University of Wisconsin System
# SPDX-License-Identifier: MIT


import os
import subprocess
import tempfile
from pathlib import Path

import pytest


# Normally we would use pytest's tmp_path fixture, but we get problems on the
# GitHub Actions Windows runner if we do that (something to do with referring
# to a local repo with absolute path, or referring to a local repo on a
# different drive). So create the temporary directory locally, so that we can
# refer to the cjdk-pre-commit repo as '..'.  We probably don't need pytest's
# nice naming and management of used temporary directories for these simple
# tests.
@pytest.fixture(scope="function")
def path_to_repo_from_tempdir(monkeypatch):
    orig = os.getcwd()
    with tempfile.TemporaryDirectory(prefix="hook-test-repo-", dir=".") as d:
        monkeypatch.chdir(d)
        try:
            yield ".."
        finally:
            monkeypatch.chdir(orig)  # So that removal of the tempdir works.


def write_files(files):
    for path, content in files.items():
        Path(path).parent.mkdir(exist_ok=True, parents=True)
        with open(path, "w") as fp:
            fp.write(content)


def run_hook_with_defaults(repodir, hook, files):
    repodir = Path(repodir)
    write_files(files)
    subprocess.run(["git", "init"], check=True)
    subprocess.run(["git", "add", "."], check=True)
    return subprocess.run(
        ["pre-commit", "try-repo", repodir, hook, "--verbose"]
    )


def test_checkstyle_fail(path_to_repo_from_tempdir):
    result = run_hook_with_defaults(
        path_to_repo_from_tempdir,
        "checkstyle",
        {
            "src/main/java/Hello.java": """
public class Hello {

}
""".lstrip()
        },
    )
    assert result.returncode != 0


def test_checkstyle_pass(path_to_repo_from_tempdir):
    result = run_hook_with_defaults(
        path_to_repo_from_tempdir,
        "checkstyle",
        {
            "src/main/java/mypackage/Hello.java": """
package mypackage;

/**
 * A greeting.
 */
public class Hello {

}
""".lstrip(),
            "src/main/java/mypackage/package-info.java": "\n",
        },
    )
    assert result.returncode == 0


def test_google_java_format_fail(path_to_repo_from_tempdir):
    result = run_hook_with_defaults(
        path_to_repo_from_tempdir,
        "google-java-format",
        {
            "src/main/java/Hello.java": """
public class Hello {

}
""".lstrip()
        },
    )
    assert result.returncode != 0
    with open("src/main/java/Hello.java") as fp:
        assert fp.read() == "public class Hello {}\n"


def test_google_java_format_pass(path_to_repo_from_tempdir):
    result = run_hook_with_defaults(
        path_to_repo_from_tempdir,
        "google-java-format",
        {"src/main/java/Hello.java": "public class Hello {}\n"},
    )
    assert result.returncode == 0


def test_pmd_fail(path_to_repo_from_tempdir):
    result = run_hook_with_defaults(
        path_to_repo_from_tempdir,
        "pmd",
        {
            "src/main/java/Hello.java": """
public class Hello {

}
""".lstrip(),
        },
    )
    assert result.returncode != 0


def test_pmd_pass(path_to_repo_from_tempdir):
    result = run_hook_with_defaults(
        path_to_repo_from_tempdir,
        "pmd",
        {
            "src/main/java/mypackage/Hello.java": """
package mypackage;

/**
 * A greeting.
 */
public class Hello {

}
""".lstrip(),
            "src/main/java/mypackage/package-info.java": "\n",
        },
    )
    assert result.returncode == 0


def test_cpd_fail(path_to_repo_from_tempdir):
    result = run_hook_with_defaults(
        path_to_repo_from_tempdir,
        "cpd",
        {
            "src/main/java/Hello.java": """
public class Hello {
    public static void hello() {
        for (int i = 0; i < 10; ++i) {
            System.out.println("Hello, World!");
        }
        for (int i = 0; i < 20; ++i) {
            System.out.println("Hello, World!");
        }
        for (int i = 0; i < 30; ++i) {
            System.out.println("Hello, World!");
        }
        for (int i = 0; i < 40; ++i) {
            System.out.println("Hello, World!");
        }
        for (int i = 0; i < 50; ++i) {
            System.out.println("Hello, World!");
        }
    }
}
""".lstrip(),
            "src/main/java/World.java": """
public class World {
    public static void world() {
        for (int i = 0; i < 10; ++i) {
            System.out.println("Hello, World!");
        }
        for (int i = 0; i < 20; ++i) {
            System.out.println("Hello, World!");
        }
        for (int i = 0; i < 30; ++i) {
            System.out.println("Hello, World!");
        }
        for (int i = 0; i < 40; ++i) {
            System.out.println("Hello, World!");
        }
        for (int i = 0; i < 50; ++i) {
            System.out.println("Hello, World!");
        }
    }
}
""".lstrip(),
        },
    )
    assert result.returncode != 0


def test_cpd_pass(path_to_repo_from_tempdir):
    result = run_hook_with_defaults(
        path_to_repo_from_tempdir,
        "cpd",
        {
            "src/main/java/Hello.java": """
public class Hello {

}
""".lstrip()
        },
    )
    assert result.returncode == 0
