import base64


def base64_to_byte_str(base64_string: str) -> bytes:
	"""Converts a base64 string to its byte string representation."""
	return base64.b64decode(base64_string.encode("ASCII"))


def byte_str_to_base64(byte_string: bytes | bytearray | memoryview) -> str:
	"""Converts a byte string to its base64 (non-byte string) representation."""
	return base64.b64encode(byte_string).decode("ASCII")
