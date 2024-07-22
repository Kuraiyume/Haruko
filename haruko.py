import itertools
import os
import sys
import gzip
import json
import re
from multiprocessing import Pool, cpu_count
from typing import List
from datetime import datetime

tool = """HARUKO: THIS TOOL IS INTENDED FOR LEGAL AND ETHICAL USE ONLY. ANY ATTEMPT TO USE IT FOR UNAUTHORIZED ACCESS OR ILLEGAL ACTIVITIES IS PROHIBITED AND WILL BE PURSUED LEGALLY. USE RESPONSIBLY.
Veilwr4ith 2024
"""

class Haruko:
    def __init__(self, characters: str, min_length: int, max_length: int, output_file: str, prefix: str = '', suffix: str = '', exclusions: str = '', include_lengths: List[int] = None, exclude_lengths: List[int] = None, threads: int = cpu_count(), compress: bool = False, encoding: str = 'utf-8', patterns: str = ''):
        self.characters = ''.join([ch for ch in characters if ch not in exclusions])
        self.min_length = min_length
        self.max_length = max_length
        self.output_file = output_file
        self.prefix = prefix
        self.suffix = suffix
        self.exclusions = exclusions
        self.include_lengths = set(include_lengths) if include_lengths else set(range(min_length, max_length + 1))
        self.exclude_lengths = set(exclude_lengths) if exclude_lengths else set()
        self.threads = threads
        self.compress = compress
        self.encoding = encoding
        try:
            self.compiled_pattern = re.compile(patterns) if patterns else None
        except re.error:
            raise ValueError(f"Invalid regex pattern: {patterns}")

    def generate_combinations(self, params):
        characters, length = params
        return (''.join(combination) for combination in itertools.product(characters, repeat=length))

    def process_length(self, length):
        if length in self.include_lengths and length not in self.exclude_lengths:
            combinations = self.generate_combinations((self.characters, length))
            words = [f"{self.prefix}{word}{self.suffix}" for word in combinations]
            if self.compiled_pattern:
                words = [word for word in words if self.compiled_pattern.match(word)]
            return words
        return []

    def write_wordlist(self, wordlist):
        try:
            if self.compress:
                compressed_file = self.output_file + '.gz'
                with gzip.open(compressed_file, 'wt', encoding=self.encoding) as f:
                    f.write('\n'.join(wordlist))
                return f"Compressed wordlist generated to {compressed_file}", len(wordlist) - 1
            else:
                with open(self.output_file, 'w', encoding=self.encoding) as f:
                    f.write('\n'.join(wordlist))
                return f"Generated {len(wordlist) - 1} words to {self.output_file}", len(wordlist) - 1
        except IOError as e:
            print(f"[!] Error writing file: {e}")
            sys.exit(1)

    def generate_wordlist(self):
        all_lengths = self.include_lengths - self.exclude_lengths
        if not all_lengths:
            raise ValueError("No valid lengths to include.")
        print(tool)
        print("[*] Generating wordlist....")
        if self.compiled_pattern:
            print(f"Applying pattern: {self.compiled_pattern.pattern}")
        wordlist = []
        try:
            with Pool(self.threads) as pool:
                results = [pool.apply_async(self.process_length, (length,)) for length in all_lengths]
                for result in results:
                    wordlist.extend(result.get())
        except KeyboardInterrupt:
            print("[*] Generation interrupted. Exiting...")
            sys.exit(0)
        result_message, word_count = self.write_wordlist(wordlist)
        return result_message, word_count

class ConfigLoader:
    @staticmethod
    def load_config(config_file):
        with open(config_file, 'r') as f:
            return json.load(f)

class FileUtils:
    @staticmethod
    def add_timestamp(filename):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base, ext = os.path.splitext(filename)
        return f"{base}_{timestamp}{ext}"

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Haruko: A Password Wordlist Generator for Brute-Force Attacks.")
    parser.add_argument("-c", "--characters", type=str, help="Set of characters to include in the wordlist.")
    parser.add_argument("-min", "--min_length", type=int, default=4, help="Minimum length of words.")
    parser.add_argument("-max", "--max_length", type=int, default=6, help="Maximum length of words.")
    parser.add_argument("-o", "--output-file", type=str, default="haruko_wordlist.txt", help="Output file name.")
    parser.add_argument("-p", "--prefix", type=str, default="", help="Prefix for each word.")
    parser.add_argument("-s", "--suffix", type=str, default="", help="Suffix for each word.")
    parser.add_argument("-e", "--exclusions", type=str, default="", help="Characters to exclude from the wordlist.")
    parser.add_argument("-inc", "--include_lengths", type=int, nargs="*", default=[], help="Lengths to include in the wordlist.")
    parser.add_argument("-exc", "--exclude_lengths", type=int, nargs="*", default=[], help="Lengths to exclude from the wordlist.")
    parser.add_argument("-t", "--threads", type=int, default=cpu_count(), help="Number of threads to use.")
    parser.add_argument("-z", "--compress", action='store_true', help="Compress the output file.")
    parser.add_argument("-enc", "--encoding", type=str, default="utf-8", help="Encoding for the output file.")
    parser.add_argument("-cfg", "--config_file", type=str, help="Path to a JSON configuration file.")
    parser.add_argument("-r", "--regex", type=str, default="", help="Regex pattern to filter generated words.")
    args = parser.parse_args()

    if args.config_file:
        config = ConfigLoader.load_config(args.config_file)
        for key, value in config.items():
            if getattr(args, key, None) is None:
                setattr(args, key, value)

    if os.path.exists(args.output_file):
        overwrite = input(f"[*] File {args.output_file} already exists. Overwrite? (y/n): ").strip().lower()
        if overwrite != 'y':
            print("Operation cancelled.")
            sys.exit(1)

    args.output_file = FileUtils.add_timestamp(args.output_file)
    wordlist_generator = Haruko(args.characters, args.min_length, args.max_length, args.output_file, args.prefix, args.suffix, args.exclusions, args.include_lengths, args.exclude_lengths, args.threads, args.compress, args.encoding, args.regex)
    result_message, word_count = wordlist_generator.generate_wordlist()
    print(f"[+] {result_message}")

if __name__ == "__main__":
    main()
