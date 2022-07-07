# This file is part of cjdk-pre-commit.
# Copyright 2022 Board of Regents of the University of Wisconsin System
# SPDX-License-Identifier: MIT


import os
import subprocess
from pathlib import Path


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


def test_checkstyle_fail(monkeypatch, tmp_path):
    repodir = os.getcwd()
    monkeypatch.chdir(tmp_path)
    result = run_hook_with_defaults(
        repodir,
        "checkstyle",
        {
            "src/main/java/Hello.java": """
public class Hello {

}
""".lstrip()
        },
    )
    assert result.returncode != 0


def test_checkstyle_pass(monkeypatch, tmp_path):
    repodir = os.getcwd()
    monkeypatch.chdir(tmp_path)
    result = run_hook_with_defaults(
        repodir,
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


def test_google_java_format_fail(monkeypatch, tmp_path):
    repodir = os.getcwd()
    monkeypatch.chdir(tmp_path)
    result = run_hook_with_defaults(
        repodir,
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


def test_google_java_format_pass(monkeypatch, tmp_path):
    repodir = os.getcwd()
    monkeypatch.chdir(tmp_path)
    result = run_hook_with_defaults(
        repodir,
        "google-java-format",
        {"src/main/java/Hello.java": "public class Hello {}\n"},
    )
    assert result.returncode == 0


def test_pmd_fail(monkeypatch, tmp_path):
    repodir = os.getcwd()
    monkeypatch.chdir(tmp_path)
    result = run_hook_with_defaults(
        repodir,
        "pmd",
        {
            "src/main/java/Hello.java": """
public class Hello {

}
""".lstrip(),
        },
    )
    assert result.returncode != 0


def test_pmd_pass(monkeypatch, tmp_path):
    repodir = os.getcwd()
    monkeypatch.chdir(tmp_path)
    result = run_hook_with_defaults(
        repodir,
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


def test_cpd_fail(monkeypatch, tmp_path):
    repodir = os.getcwd()
    monkeypatch.chdir(tmp_path)
    result = run_hook_with_defaults(
        repodir,
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


def test_cpd_pass(monkeypatch, tmp_path):
    repodir = os.getcwd()
    monkeypatch.chdir(tmp_path)
    result = run_hook_with_defaults(
        repodir,
        "cpd",
        {
            "src/main/java/Hello.java": """
public class Hello {

}
""".lstrip()
        },
    )
    assert result.returncode == 0
