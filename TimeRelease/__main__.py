import argparse
import json
from pathlib import Path
from .bench import run_benchmark


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

	# Determine and validate infile and outfile
	if args.encrypt:
		infile, outfile = Path(args.encrypt[0]), Path(args.encrypt[1])
	elif args.decrypt:
		infile, outfile = Path(args.decrypt[0]), Path(args.decrypt[1])
	if not infile.is_file():
		print(f"{infile} does not exist or is not a file")
		return -1
	if outfile.is_file():
		print(f"{outfile} will be overwritten! Proceed anyway? [y/n]")
		if input(">>> ").strip().lower() != "y":
			print("Exiting.")
			return -1
	if outfile.is_dir():
		print(f"{outfile} cannot be overwritten: is a directory")
		return -1

	# Begin encrypting/decrypting
	if args.encrypt:
		print(f"Encrypting {infile} -> {outfile}:")
		main_enc(infile, outfile)
	elif args.decrypt:
		print(f"Decrypting {infile} -> {outfile}:")
		main_dec(infile, outfile)


if __name__ == "__main__":
	main()
