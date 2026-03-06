# TimeRelease

## Introduction

A simple Python utility to lock (or encrypt) secrets, such that they require a preset amount of compute to unlock (or decrypt) them later.

Since each cryptographic step requires the last, it (by design) cannot be parallelized.

This could potentially be useful if you want to wait, for example, an hour, before being able to access a password; as a form of stolen device protection.

## WARNING!

Always keep your output `timerelease.json` file secret, treating it as if it were a password. It is effectively unencrypted as it can be used to decrypt the secret (if such an attacker has sufficient time to complete the puzzle).

## Interactive Usage

### Setup

Install the package and its dependencies in a venv:

```bash
python3 -m venv ./venv
source ./venv/bin/activate
pip install TimeRelease
```

### Encryption

To encrypt a file `somefile.txt` -> `somefile.txt.timerelease`:

```bash
# Specify # of seconds it should take to unlock on your machine
timerelease --encrypt somefile.txt somefile.txt.timerelease --time 3600
# Or, specify raw # of iterations needed to unlock the file
timerelease --encrypt somefile.txt somefile.txt.timerelease --iters 1073741824
```

You can use this to determine how long (on your hardware) the decryption process will take. Encryption should be nearly instant for most settings, even for comically large numbers of iterations.

### Decryption

To decrypt a file `somefile.txt.timerelease` -> `somefile.txt`:

```bash
timerelease --decrypt somefile.txt.timerelease somefile.txt
```

It will take however long the person who encrypted the file dictates. The only way to speed it up is to find a CPU with really, really fast single-core performance.

## Use in Other Codebases

Like any module, TimeRelease can be installed via pip (`pip install TimeRelease`) and imported. 

TODO: describe package API, what each function does

## Development Usage

To install development versions of this package, clone this repo and `cd` into it, then run:

```bash
python3 -m venv ./venv
source ./venv/bin/activate
pip install -e .
```
