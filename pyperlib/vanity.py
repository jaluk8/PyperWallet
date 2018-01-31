from multiprocessing import Process, cpu_count
from multiprocessing import Queue
from pyperlib import data, ec
import re
import string
import time


substitutions = {
    "i": ["1"],
    "o": ["0"],
    "l": ["1"],
    "e": ["3"],
    "s": ["5"]
}


class InvalidCharException(Exception):
    """Raise when a non-alphanumeric character is used in a pattern."""


class Generator:
    """Generate vanity addresses."""

    def __init__(self, Coin):
        """Create the generator given a coin type."""
        self.Coin = Coin

    @staticmethod
    def regex(pattern):
        """Turn a pattern into a regular expression."""
        exp = ""
        for char in pattern:
            allowed_chars = []
            if char in string.digits:
                allowed_chars += [char]
            elif char in string.ascii_letters:
                allowed_chars += [char.lower(), char.upper()]
                if char.lower() in substitutions:
                    allowed_chars += substitutions[char.lower()]
            else:
                raise InvalidCharException(pattern + " is not alphanumeric.")

            exp += "("
            for c in allowed_chars:
                exp += c + "|"
            exp = exp[:-1]
            exp += ")"
        exp += ".*"
        return re.compile(exp)

    def run_thread(self, pattern, queue):
        """Run a single thread of vanity generation."""
        regex = self.regex(pattern)
        c = self.Coin()
        match = False
        while not match:
            c = self.Coin()
            addr = c.addr_string()
            match = regex.match(addr)
        queue.put(c.keypair)

    def run(self, pattern):
        """Generate and return a coin that matches the pattern."""
        processes = []
        queue = Queue(1)
        for _ in range(cpu_count()):
            proc = Process(target=self.run_thread, args=(pattern, queue))
            processes += [proc]
            proc.start()
        kp = queue.get()
        for p in processes:
            p.terminate()
        return kp
