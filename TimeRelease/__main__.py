import argparse
import hashlib
import json
from pathlib import Path
import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from sympy import nextprime
from .b64utils import byte_str_to_base64
from .bench import run_benchmark


def encrypt_secret(secret, iterations, logging=True):
	# Create new (symmetric) AES key and encrypt secret with it
	if logging: print("Generating encryption key...")
	aes_key = get_random_bytes(16)
	cipher = AES.new(aes_key, AES.MODE_CBC)
	secret_iv = cipher.iv
	encrypted_secret = cipher.encrypt(pad(secret, AES.block_size))

	# Time-lock puzzle setup
	# Generate N = p * q
	if logging: print("Preparing time lock...")
	p = nextprime(random.getrandbits(512))
	q = nextprime(random.getrandbits(512))
	modulus = p * q

	# Puzzle: compute r = base^(2^iterations) mod modulus
	base = random.randint(2, modulus - 1)
	r = pow(base, pow(2, iterations, (p - 1)*(q - 1)), modulus)

	# Derive AES key from r (e.g. using SHA256)
	if logging: print("Deriving AES key from time lock...")
	derived_key = hashlib.sha256(str(r).encode()).digest()[:16]

	# Encrypt AES key with derived key
	if logging: print("Encrypting derived key...")
	cipher2 = AES.new(derived_key, AES.MODE_CBC)
	key_iv = cipher2.iv
	encrypted_key = cipher2.encrypt(pad(aes_key, AES.block_size))

	# Stash stuff needed to decrypt later
	return {
		"base": base,
		"modulus": modulus,
		"iterations": iterations,
		"secret_iv": byte_str_to_base64(secret_iv),
		"encrypted_secret": byte_str_to_base64(encrypted_secret),
		"key_iv": byte_str_to_base64(key_iv),
		"encrypted_key": byte_str_to_base64(encrypted_key)
	}


def main_enc(infile, outfile):
	# Benchmark
	print("Would you like to benchmark your CPU to provide more accurate unlock times? (Note that this may be thwarted by using a CPU with better single-core performance)")
	while True:
		response = input("[y/n] ").strip().lower()
		if response in ("y", "yes"):
			bench = True
			break
		elif response in ("n", "no"):
			bench = False
			break
		else:
			print("Please enter 'y' or 'n'.")

	if bench:
		# Run benchmark
		print("TimeRelease is benchmarking your CPU. This may take up to a minute.")
		ips = run_benchmark(logging=False)
		print("Approximately how long would you like the unlock process to take on your CPU (in seconds)?")
		iters = int(float(input("[float] ")) * ips)
	else:
		# Ask for raw iterations
		print("How many iterations? Note that modern CPUs can handle upwards of 100,000 iterations per second.")
		iters = int(input("[int] "))

	# Read infile
	with open(infile, 'rb') as f:
		secret = f.read()

	# Encrypt secret & get JSON package
	enc_package = encrypt_secret(secret, iters)

	# Write outfile
	with open(outfile, 'w') as f:
		json.dump(enc_package, f, indent=4)


def main_dec(infile, outfile):
	# Read infile
	with open(infile, 'r') as f:
		enc_package = json.load(f)

	# Decrypt
	decrypted = decrypt_secret(enc_package)
	
	# Write outfile
	with open(outfile, 'wb') as f:
		f.write(decrypted)


def main(argv=None):
	# Read arguments
	parser = argparse.ArgumentParser(prog="TimeRelease")
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument(
		"--encrypt",
		nargs=2,
		metavar=("INFILE", "OUTFILE"),
		help="Encrypt input file to output file path",
	)
	group.add_argument(
		"--decrypt",
		nargs=2,
		metavar=("INFILE", "OUTFILE"),
		help="Decrypt input file to output file path",
	)
	args = parser.parse_args(argv)

	if args.encrypt:
		infile, outfile = Path(args.encrypt[0]), Path(args.encrypt[1])
		if not infile.is_file():
			print(f"{infile} does not exist or is not a file")
			return -1
		print(f"Encrypting {infile} -> {outfile}:")
		main_enc(infile, outfile)

	elif args.decrypt:
		infile, outfile = Path(args.decrypt[0]), Path(args.decrypt[1])
		if not infile.is_file():
			print(f"{infile} does not exist or is not a file")
			return -1
		print(f"Decrypting {infile} -> {outfile}:")
		main_dec(infile, outfile)


if __name__ == "__main__":
	main()
