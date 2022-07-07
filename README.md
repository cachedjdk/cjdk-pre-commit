<!--
This file is part of cjdk-pre-commit.
Copyright 2022 Board of Regents of the University of Wisconsin System
SPDX-License-Identifier: MIT
--->

# pre-commit hooks for Java tools

This repository contains [pre-commit](https://pre-commit.com/) hooks for
running tools that require a Java Virtual Machine to run.

(The tools may be applicable to languages other than Java.)

These hooks use [cjdk](https://marktsuchida.github.io/cjdk/latest/) to download
and cache both the JVM and the tool packages, so that there is no need for
`java` to be available on the `PATH` or for `JAVA_HOME` to be configured
correctly for the tools. You can run the hooks using a different JDK from your
`JAVA_HOME`.

Available hooks:

- [`checkstyle`](#checkstyle) - run [Checkstyle](https://checkstyle.org/)
- [`pmd`](#pmd) - run the [PMD](https://pmd.github.io/) static analyzer
- [`cpd`](#cpd) - run PMD's
  [CPD](https://pmd.github.io/latest/pmd_userdocs_cpd.html) (copy-paste
  detector)
- [`google-java-format`](#google-java-format) - run
  [google-java-format](https://github.com/google/google-java-format)

## Requirements

Python >= 3.8; pre-commit >= 2.0.0.

## `checkstyle`

Runs [Checkstyle](https://checkstyle.org/) on Java source files.

Arguments:

- `--jdk=temruin-jre:17`: set the JDK or JRE to use, using **cjdk** syntax
- `--tool-version=10.3.1`: set the Checkstyle version to use
- `--jvm-arg=<arg>`: any argument to pass to `java` (can be given multiple
  times)
- `--`: pass all subsequent arguments to Checkstyle

See also: Checkstyle [command line usage](https://checkstyle.org/cmdline.html).

If you override `args`, you need to include the `-c` option.

By default, the "Sun" style checks (`/sun_checks.xml`) included with Checkstyle
are used.

`.pre-commit-config.yaml` examples:

```yaml
- repo: https://github.com/marktsuchida/cjdk-pre-commit
  rev: v0.1.0
  hooks:
    - id: checkstyle
      args: ["-c", "/google_checks.xml"]
      verbose: true  # /google_checks.xml only issues warnings.
```

```yaml
- repo: https://github.com/marktsuchida/cjdk-pre-commit
  rev: v0.1.0
  hooks:
    - id: checkstyle
      args:
        - --jdk=temurin-jre:17.0.3
        - --tool-version=10.3.1
        - --jvm-arg=-Xmx2048M
        - --
        - -c
        - /sun_checks.xml
```

## `pmd`

Runs the [PMD](https://pmd.github.io/) static code analyzer on source files
(Java source files by default).

Arguments:

- `--jdk=temurin-jre:17`: set the JDK or JRE to use, using **cjdk** syntax
- `--tool-version=6.47.0`: set the PMD version to use
- `--jvm-args="<args>"`: set `PMD_JAVA_OPTS` to `<args>`
- `--`: pass all subsequent arguments to PMD's command-line interface

See also: PMD command line
[usage](https://pmd.github.io/latest/pmd_userdocs_installation.html#running-pmd-via-command-line)
and [reference](https://pmd.github.io/latest/pmd_userdocs_cli_reference.html).

If you override `args`, you need to include the `-R` and `-d` options.

By default, the `rulesets/java/quickstart.xml` ruleset is run on the directory
`src/main/java`.

`.pre-commit-config.yaml` example:

```yaml
- repo: https://github.com/marktsuchida/cjdk-pre-commit
  rev: v0.1.0
  hooks:
    - id: pmd
      args:
        - --
        - -R
        - my_ruleset.xml
        - -d
        - src/main/java
```

## `cpd`

Runs [PMD](https://pmd.github.io/)'s copy-paste detector
[CPD](https://pmd.github.io/latest/pmd_userdocs_cpd.html) on source files (Java
source files by default).

Arguments:

- `--jdk=temurin-jre:17`: set the JDK or JRE to use, using **cjdk** syntax
- `--tool-version=6.47.0`: set the PMD version to use
- `--jvm-args="<args>"`: set `PMD_JAVA_OPTS` to `<args>`
- `--`: pass all subsequent arguments to CPD's command-line interface

See also: CPD command line
[usage](https://pmd.github.io/latest/pmd_userdocs_installation.html#running-cpd-via-command-line)
and [reference](https://pmd.github.io/latest/pmd_userdocs_cpd.html#cli-usage).

If you override `args`, you need to include the `--minimum-tokens` and
`--files` options.

By default, the minimum token count is set to `100` and CPD is run on the files
in `src/main/java`.

`.pre-commit-config.yaml` example:

```yaml
- repo: https://github.com/marktsuchida/cjdk-pre-commit
  rev: v0.1.0
  hooks:
    - id: cpd
```

`.pre-commit-config.yaml` example for running CPD on Python source files:

```yaml
- repo: https://github.com/marktsuchida/cjdk-pre-commit
  rev: v0.1.0
  hooks:
    - id: cpd
      types: [python]
      args:
        - --
        - --language
        - python
        - --minimum-tokens
        - "100"
        - --files
        - src
```

## `google-java-format`

Formats Java source files using
[google-java-format](https://github.com/google/google-java-format).

Arguments:

- `--jdk=temruin:17`: set the JDK to use, using **cjdk** syntax
- `--tool-version=1.15.0`: set the google-java-format version to use
- `--jvm-arg=<arg>`: any argument to pass to `java` (can be given multiple
  times)
- `--`: pass all subsequent arguments to google-java-format

See also: google-java-format command line usage, produced by running
`cjdk_pre_commit google-java-format -- --help`.

Note that google-java-format requires a full JDK and will not run with a JRE.

If you override `args`, you will probably want to include `--replace`.

`.pre-commit-config.yaml` example:

```yaml
- repo: https://github.com/marktsuchida/cjdk-pre-commit
  rev: v0.1.0
  hooks:
    - id: google-java-format
      args:
        - --
        - --replace
        - --skip-reflowing-long-strings
```

## Development

```sh
git clone https://github.com/marktsuchida/cjdk-pre-commit.git
cd cjdk-pre-commit
python -m venv venv
echo '*' >venv/.gitignore
source venv/bin/activate
pip install -e .[dev,testing]
pre-commit install
```

Run unit tests:

```sh
pytest
```

Run system tests:

```sh
pytest systemtests
```

Run tests as done by the CI:

```sh
nox
nox -s systemtest
```
