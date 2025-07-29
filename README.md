# TimeRelease

A simple Python utility to lock (or encrypt) secrets, such that they require a preset amount of compute to unlock (or decrypt) them later.

Since each cryptographic step requires the last, it (by design) cannot be parallelized.

This could potentially be useful if you want to wait, say, an hour, before being able to access a password, as a form of stolen device protection.