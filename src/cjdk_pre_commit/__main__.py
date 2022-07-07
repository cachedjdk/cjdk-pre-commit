# This file is part of cjdk-pre-commit.
# Copyright 2022 Board of Regents of the University of Wisconsin System
# SPDX-License-Identifier: MIT

import os
import subprocess
import sys

import cjdk
import click

from . import _version

__all__ = [
    "main",
]

default_jdk = "temurin:17.0.3"

default_tool_version = {
    "checkstyle": "10.3.1",
    "pmd": "6.47.0",
    "cpd": "6.47.0",
    "google-java-format": "1.15.0",
}


def checkstyle_jar(v):
    return cjdk.cache_file(
        "Checkstyle",
        f"https://github.com/checkstyle/checkstyle/releases/download/checkstyle-{v}/checkstyle-{v}-all.jar",
        f"checkstyle-{v}-all.jar",
    )


def pmd_bindir(v):
    parent = cjdk.cache_package(
        "PMD",
        f"zip+https://github.com/pmd/pmd/releases/download/pmd_releases%2F{v}/pmd-bin-{v}.zip",
    )
    return parent / f"pmd-bin-{v}" / "bin"


def pmd_script(v):
    if sys.platform == "win32":
        return [str(pmd_bindir(v) / "pmd.bat")]
    return [str(pmd_bindir(v) / "run.sh"), "pmd"]


def cpd_script(v):
    if sys.platform == "win32":
        return [str(pmd_bindir(v) / "cpd.bat")]
    return [str(pmd_bindir(v) / "run.sh"), "cpd"]


def google_java_format_jar(v):
    return cjdk.cache_file(
        "google-java-format",
        f"https://github.com/google/google-java-format/releases/download/v{v}/google-java-format-{v}-all-deps.jar",
        f"google-java-format-{v}-all-deps.jar",
    )


tool_type = {
    "checkstyle": "jar",
    "pmd": "script",
    "cpd": "script",
    "google-java-format": "jar",
}


jar_func = {
    "checkstyle": checkstyle_jar,
    "pmd": pmd_script,
    "cpd": cpd_script,
    "google-java-format": google_java_format_jar,
}


script_func = {
    "pmd": pmd_script,
    "cpd": cpd_script,
}


env_func = {
    "pmd": lambda jvm_args: {"PMD_JAVA_OPTS": jvm_args},
    "cpd": lambda jvm_args: {"PMD_JAVA_OPTS": jvm_args},
}


def jar_tool_args(jar, jvm_args, args):
    ret = ["java"]
    ret.extend(jvm_args)
    ret.extend(("-jar", str(jar)))
    ret.extend(args)
    return ret


def script_tool_args(script, args):
    ret = script
    ret.extend(args)
    return ret


def tool_setup(tool, version, jvm_arg_list, jvm_arg_str, tool_args):
    ttype = tool_type[tool]
    if ttype == "jar":
        jar = jar_func[tool](version)
        jvm_arg_list = jvm_arg_list if jvm_arg_list else []
        args = jar_tool_args(jar, jvm_arg_list, tool_args)
    elif ttype == "script":
        script = script_func[tool](version)
        args = script_tool_args(script, tool_args)
    env = env_func.get(tool, lambda jvm_args: {})(jvm_arg_str)
    env = {k: v for k, v in env.items() if v}
    return args, env


@click.command()
@click.option("--jdk", metavar="VENDOR:VERSION", default=default_jdk)
@click.option("--tool-version", metavar="VERSION")
@click.option("--jvm-arg", metavar="ARG", multiple=True)
@click.option("--jvm-args", metavar="ARGS")
@click.argument("tool", nargs=1)
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
@click.option("--verbose", is_flag=True)
@click.version_option(version=_version.__version__)
def main(jdk, tool_version, jvm_arg, jvm_args, tool, args, verbose):
    tool_version = tool_version if tool_version else default_tool_version[tool]
    if verbose:
        print(f"Running {tool} {tool_version} with {jdk}", file=sys.stderr)
    args, env = tool_setup(tool, tool_version, jvm_arg, jvm_args, args)
    if verbose:
        print(f"Args: {args}", file=sys.stderr)
        print(f"Env: {env}", file=sys.stderr)

    with cjdk.java_env(jdk=jdk):
        whole_env = dict(os.environ)
        whole_env.update(env)
        result = subprocess.run(args, env=whole_env)
        sys.exit(result.returncode)


if __name__ == "__main__":
    main()
