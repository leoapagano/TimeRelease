import random
from sympy import nextprime
import time


def run_single_benchmark(iterations, logging=True):
	"""
	Determines how long it takes for the CPU to run a fixed number of `iterations`.
	Amount of time elapsed is returned in seconds as a float.
	If `logging` (defaults to True) is set to True, extra debug information is printed.
	"""
	# Setup dummy puzzle parameters
	if logging: print("Preparing time lock...")
	p = nextprime(random.getrandbits(512))
	q = nextprime(random.getrandbits(512))
	modulus = p * q

	# Execute & time it
	if logging: print("Running benchmark...")
	start_time = time.time()
	r = random.randint(2, modulus - 1)
	for _ in range(iterations):
		r = pow(r, 2, modulus)
	end_time = time.time()

	return end_time - start_time


def run_benchmark(benches=10, logging=True):
	"""
	Determines how many iterations a single core of the user's CPU is capable of processing, on average, per second (as an integer).
	`benches` (defaults to 10) describes the number of times the benchmark will be run.
	Higher values of `benches` = greater certainty in running time, but more time is spent benchmarking.
	If `logging` (defaults to True) is set to True, extra debug information is printed.
	"""
	# Repeat single benchmarks, doubling iterations until the time per benchmark is less than 1 second
	iterations = 1
	execution_time = 0
	while execution_time < 1:
		iterations *= 2
		if logging: print(f"Running benchmark @ iterations={iterations}")
		execution_time = run_single_benchmark(iterations, logging=logging)
	
	# Run benches (default: 10) benchmarks with this number of iterations
	results = []
	for i in range(benches):
		if logging: print(f"Running standard benchmark {i+1} / {benches}")
		results.append(run_single_benchmark(iterations, logging=logging))

	# Determine average iterations/sec and return
	avg = sum(results) / benches
	return int(iterations // avg)