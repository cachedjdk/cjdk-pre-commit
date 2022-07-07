# This file is part of cjdk-pre-commit.
# Copyright 2022 Board of Regents of the University of Wisconsin System
# SPDX-License-Identifier: MIT

import os
import subprocess

import cjdk
from click.testing import CliRunner

from cjdk_pre_commit.__main__ import main


def test_main():
    result = CliRunner().invoke(main, [])
    assert result.exit_code != 0


def test_main_jar(mocker):
    mocker.patch(
        "cjdk_pre_commit.__main__.tool_setup",
        mocker.Mock(return_value=(["a", "b"], {"C": "d"})),
    )
    java_env_ctx_mgr = mocker.MagicMock()
    java_env_ctx_mgr.__enter__ = mocker.Mock(
        side_effect=lambda: mocker.patch.dict("os.environ", {"E": "f"})
    )
    mocker.patch("cjdk.java_env", mocker.Mock(return_value=java_env_ctx_mgr))
    completed_proc = mocker.Mock()
    completed_proc.returncode = 42
    mocker.patch("subprocess.run", mocker.Mock(return_value=completed_proc))
    expected_env = dict(os.environ)
    expected_env.update({"C": "d", "E": "f"})
    result = CliRunner().invoke(
        main,
        [
            "--verbose",
            "checkstyle",
            "--jdk",
            "JDK",
            "--tool-version",
            "VERSION",
            "--jvm-arg",
            "x",
            "--",
            "y",
            "z",
        ],
    )
    assert result.exit_code == 42
    cjdk.java_env.assert_called_once_with(jdk="JDK")
    java_env_ctx_mgr.__enter__.assert_called_once()
    subprocess.run.assert_called_once_with(["a", "b"], env=expected_env)


def test_main_script(mocker):
    mocker.patch(
        "cjdk_pre_commit.__main__.tool_setup",
        mocker.Mock(return_value=(["a", "b"], {"C": "d"})),
    )
    java_env_ctx_mgr = mocker.MagicMock()
    java_env_ctx_mgr.__enter__ = mocker.Mock(
        side_effect=lambda: mocker.patch.dict("os.environ", {"E": "f"})
    )
    mocker.patch("cjdk.java_env", mocker.Mock(return_value=java_env_ctx_mgr))
    completed_proc = mocker.Mock()
    completed_proc.returncode = 42
    mocker.patch("subprocess.run", mocker.Mock(return_value=completed_proc))
    expected_env = dict(os.environ)
    expected_env.update({"C": "d", "E": "f"})
    result = CliRunner().invoke(
        main,
        [
            "--verbose",
            "pdm",
            "--jdk",
            "JDK",
            "--tool-version",
            "VERSION",
            "--jvm-args",
            "x w",
            "--",
            "y",
            "z",
        ],
    )
    assert result.exit_code == 42
    cjdk.java_env.assert_called_once_with(jdk="JDK")
    java_env_ctx_mgr.__enter__.assert_called_once()
    subprocess.run.assert_called_once_with(["a", "b"], env=expected_env)
