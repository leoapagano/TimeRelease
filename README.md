# TimeRelease

## Introduction

A simple Python utility to lock (or encrypt) secrets, such that they require a preset amount of compute to unlock (or decrypt) them later.

Since each cryptographic step requires the last, it (by design) cannot be parallelized.

This could potentially be useful if you want to wait, say, an hour, before being able to access a password, as a form of stolen device protection.

## WARNING!

Always keep your output `timerelease.json` file secret, treating it as if it were a password. It is effectively unencrypted as it can be used to decrypt the secret (if such an attacker has sufficient time to complete the puzzle).

## Setup

To get it up and running, first, install dependencies:

```
python3 -m venv ./venv
source ./venv/bin/activate
pip install -r requirements.txt
```

Then, run `encrypt_secret.py` interactively:

```
python3 encrypt_secret.py
```

And follow the instructions provided.