import itertools
import os
import sys
import gzip
import json
import re
from multiprocessing import Pool, cpu_count
from typing import List, Tuple
from datetime import datetime

# Banner for tool identification
tool = r"""
  _    _                  _         
 | |  | |                | |        
 | |__| | __ _ _ __ _   _| | _____  
 |  __  |/ _` | '__| | | | |/ / _ \ 
 | |  | | (_| | |  | |_| |   < (_) |
 |_|  |_|\__,_|_|   \__,_|_|\_\___/ v1.0.12
                    Veilwr4ith
"""

class Haruko:
    def __init__(self, characters: str, min_length: int, max_length: int, output_file: str, 
                 prefix: str = '', suffix: str = '', exclusions: str = '', 
                 include_lengths: List[int] = None, exclude_lengths: List[int] = None, 
                 threads: int = cpu_count(), compress: bool = False, encoding: str = 'utf-8', 
                 patterns: str = '', year_range: Tuple[int, int] = None, 
                 year_position: str = 'suffix', year_format: str = 'YYYY', 
                 delimiters: List[str] = None):
        """
        Initialize Haruko with configuration parameters.
        """
        # Filter out exclusions from characters
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
        self.year_range = year_range
        self.year_position = year_position
        self.year_format = year_format
        self.delimiters = delimiters or ['']
        self.compiled_pattern = re.compile(patterns) if patterns else None

    def generate_combinations(self, params):
        """
        Generate combinations of characters for a given length.
        """
        characters, length = params
        return (''.join(combination) for combination in itertools.product(characters, repeat=length))

    def format_year(self, year: int) -> str:
        """
        Format the year based on the specified format.
        """
        if self.year_format == 'YY':
            return str(year)[-2:]
        elif self.year_format == 'MMYY':
            return f'01{str(year)[-2:]}'
        return str(year)

    def add_year(self, word: str, year: str, delimiter: str) -> str:
        """
        Insert the formatted year into the word at the specified position.
        """
        if self.year_position == 'prefix':
            return f"{year}{delimiter}{word}"
        elif self.year_position == 'suffix':
            return f"{word}{delimiter}{year}"
        elif self.year_position.isdigit():
            pos = int(self.year_position)
            return word[:pos] + year + delimiter + word[pos:]
        return word

    def process_length(self, length):
        """
        Generate words of a specific length and apply filters and formatting.
        """
        if length in self.include_lengths and length not in self.exclude_lengths:
            combinations = self.generate_combinations((self.characters, length))
            words = [f"{self.prefix}{word}{self.suffix}" for word in combinations]
            if self.compiled_pattern:
                # Apply regex pattern filter
                words = [word for word in words if self.compiled_pattern.match(word)]
            if self.year_range:
                # Add year information to words
                years = range(self.year_range[0], self.year_range[1] + 1)
                words_with_years = []
                for word in words:
                    for year in years:
                        for delimiter in self.delimiters:
                            words_with_years.append(self.add_year(word, self.format_year(year), delimiter))
                return words_with_years
            return words
        return []

    def write_wordlist(self, wordlist):
        """
        Write the generated wordlist to the specified output file.
        """
        try:
            if self.compress:
                # Write compressed file if specified
                compressed_file = self.output_file + '.gz'
                with gzip.open(compressed_file, 'wt', encoding=self.encoding) as f:
                    f.write('\n'.join(wordlist) + '\n')
                return f"Compressed wordlist generated to {compressed_file}", len(wordlist)
            else:
                # Write regular file
                with open(self.output_file, 'w', encoding=self.encoding) as f:
                    f.write('\n'.join(wordlist) + '\n')
                return f"Generated {len(wordlist)} words to {self.output_file}", len(wordlist)
        except IOError as e:
            print(f"[-] Error writing file: {e}")
            sys.exit(1)

    def generate_wordlist(self):
        """
        Generate the full wordlist using multiprocessing for efficiency.
        """
        all_lengths = self.include_lengths - self.exclude_lengths
        if not all_lengths:
            raise ValueError("[-] No valid lengths to include.")
        print("[*] Generating wordlist....")
        if self.compiled_pattern:
            print(f"[*] Applying pattern: {self.compiled_pattern.pattern}")
        wordlist = []
        try:
            # Use multiprocessing to speed up wordlist generation
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
        """
        Load configuration from a JSON file.
        """
        with open(config_file, 'r') as f:
            return json.load(f)

class FileUtils:
    @staticmethod
    def add_timestamp(filename):
        """
        Append a timestamp to the filename to avoid overwriting existing files.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base, ext = os.path.splitext(filename)
        return f"{base}_{timestamp}{ext}"

def main():
    import argparse
    print(tool)
    parser = argparse.ArgumentParser(description="Haruko: A Password Wordlist Generator for Brute-Force an Dictionary Attacks")
    parser.add_argument("-c", "--characters", type=str, help="Set of characters to include in the wordlist")
    parser.add_argument("-min", "--min-length", type=int, default=4, help="Minimum length of words")
    parser.add_argument("-max", "--max-length", type=int, default=6, help="Maximum length of words")
    parser.add_argument("-o", "--output-file", type=str, default="haruko_wordlist.txt", help="Output file name")
    parser.add_argument("-p", "--prefix", type=str, default="", help="Prefix for each word")
    parser.add_argument("-s", "--suffix", type=str, default="", help="Suffix for each word")
    parser.add_argument("-e", "--exclusions", type=str, default="", help="Characters to exclude from the wordlist")
    parser.add_argument("-inc", "--include-lengths", type=int, nargs="*", default=[], help="Lengths to include in the wordlist")
    parser.add_argument("-exc", "--exclude-lengths", type=int, nargs="*", default=[], help="Lengths to exclude from the wordlist")
    parser.add_argument("-t", "--threads", type=int, default=cpu_count(), help="Number of threads to use")
    parser.add_argument("-z", "--compress", action='store_true', help="Compress the output file")
    parser.add_argument("-enc", "--encoding", type=str, default="utf-8", help="Encoding for the output file")
    parser.add_argument("-cfg", "--config-file", type=str, help="Path to a JSON configuration file")
    parser.add_argument("-r", "--regex", type=str, default="", help="Regex pattern to filter generated words")
    parser.add_argument("-y", "--year-range", type=str, help="Year range to include, formatted as 'start_year-end_year'")
    parser.add_argument("-yp", "--year-position", type=str, default="suffix", help="Position to place the year: 'prefix', 'suffix', or specific position index (e.g., '2')")
    parser.add_argument("-yf", "--year-format", type=str, default="YYYY", help="Year format: 'YY', 'YYYY', 'MMYY'")
    parser.add_argument("-yd", "--year-delimiters", type=str, nargs="*", default=[''], help="Delimiters to use between words and years, separated by spaces (e.g., '-', '_', '')")
    parser.add_argument("--no-timestamp", action='store_true', help="Exclude timestamp from the output file name")
    args = parser.parse_args()
    # Display help if no arguments are provided
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    """
    Error messages
    """
    if args.min_length < 1:
        print("[-] Invalid minimum length. It must be at least 1")
        sys.exit(1)
    if args.max_length < args.min_length:
        print("[-] Invalid maximum length. It must be greater than or equal to the minimum length")
        sys.exit(1)
    if not args.characters and not args.config_file:
        print("[-] Characters parameter is required")
        sys.exit(1)
    if args.year_position and args.year_format and not args.year_range:
        print("[-] The 'year_range' must be specified")
        sys.exit(1)
    if args.year_range:
        try:
            start_year, end_year = map(int, args.year_range.split('-'))
            if start_year > end_year:
                print("[-] Invalid year range. The 'end_year' must be greater than 'start_year'")
                sys.exit(1)
            year_range = (start_year, end_year)
        except ValueError:
            print("[-] Invalid year range format. Use 'start_year-end_year'.")
            sys.exit(1)
    else:
        year_range = None
    if args.year_position not in ['prefix', 'suffix'] and not args.year_position.isdigit():
        print("[-] Invalid year position. Use 'prefix', 'suffix', or a digit.")
        sys.exit(1)
    if args.year_format not in ["YY", "YYYY", "MMYY"]:
        print("[-] Invalid year format. Use 'YY', 'YYYY', or 'MMYY'.")
        sys.exit(1)
    # Load the config file if specified
    if args.config_file:
        config = ConfigLoader.load_config(args.config_file)
        args.__dict__.update(config)
    # Add timestamp if needed
    if not args.no_timestamp:
        args.output_file = FileUtils.add_timestamp(args.output_file)
    haruko = Haruko(
        characters=args.characters,
        min_length=args.min_length,
        max_length=args.max_length,
        output_file=args.output_file,
        prefix=args.prefix,
        suffix=args.suffix,
        exclusions=args.exclusions,
        include_lengths=args.include_lengths,
        exclude_lengths=args.exclude_lengths,
        threads=args.threads,
        compress=args.compress,
        encoding=args.encoding,
        patterns=args.regex,
        year_range=tuple(map(int, args.year_range.split('-'))) if args.year_range else None,
        year_position=args.year_position,
        year_format=args.year_format,
        delimiters=args.year_delimiters
    )
    result_message, word_count = haruko.generate_wordlist()
    print(f"[+] {result_message}")
    
if __name__ == "__main__":
    main()
