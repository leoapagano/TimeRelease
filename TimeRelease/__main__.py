import argparse
import json
from pathlib import Path
from .bench import run_benchmark
from .decrypt import decrypt_secret
from .encrypt import encrypt_secret


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
	iters_group = parser.add_mutually_exclusive_group()
	iters_group.add_argument(
		"--iters",
		type=int,
		metavar="N",
		help="Number of iterations for encryption (required with --encrypt)",
	)
	iters_group.add_argument(
		"--time",
		type=float,
		metavar="SECONDS",
		help="Target decryption time in seconds; benchmarks your CPU to compute iterations (required with --encrypt)",
	)
	args = parser.parse_args(argv)

	# Validate --iters/--time usage
	if args.encrypt and args.iters is None and args.time is None:
		parser.error("--encrypt requires either --iters or --time")
	if (args.iters is not None or args.time is not None) and not args.encrypt:
		parser.error("--iters and --time can only be used with --encrypt")

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

	# ENCRYPTION
	if args.encrypt:
		# Determine # of iterations
		if args.iters is not None:
			iters = args.iters
		else:
			print("TimeRelease is benchmarking your CPU. This may take up to a minute.")
			ips = run_benchmark(logging=False)
			iters = int(args.time * ips)
		
		print(f"Encrypting {infile} -> {outfile}:")

		# Read infile
		with open(infile, 'rb') as f:
			secret = f.read()

		# Encrypt secret & get JSON package
		enc_package = encrypt_secret(secret, iters)

		# Write outfile
		with open(outfile, 'w') as f:
			json.dump(enc_package, f, indent=4)
	
	# DECRYPTION
	elif args.decrypt:
		print(f"Decrypting {infile} -> {outfile}:")
		
		# Read infile
		with open(infile, 'r') as f:
			enc_package = json.load(f)

		# Decrypt
		decrypted = decrypt_secret(enc_package)
		
		# Write outfile
		with open(outfile, 'wb') as f:
			f.write(decrypted)


if __name__ == "__main__":
	main()
