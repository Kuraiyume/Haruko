# HARUKO - Password Wordlist Generator

HARUKO is a robust tool designed to generate customizable password wordlists for brute-force attacks. It caters to cybersecurity professionals, penetration testers, and security researchers who need to create tailored wordlists to assess password strength and improve system security.

## Features

- **Customizable Wordlists:** Create wordlists with specific character sets, lengths, and patterns.
- **Compression Support:** Optionally compress the output file for efficient storage.
- **Multithreaded Processing:** Utilize multiple CPU threads for faster generation.
- **Configurable Encoding:** Choose the encoding for the output file.
- **Pattern Filtering:** Use regular expressions to filter generated words.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/veilwr4ith/haruko
   ```
   
2. **Install gzip:**
   ```bash
   sudo apt install gzip
   ```

3. **Navigate to the directory:**
   ```bash
   cd Haruko
   ```

4. **Run the script to show up the Main Menu:**
   ```bash
   python3 haruko.py
   ```

## Options
    -c, --characters : Set of characters to include in the wordlist (e.g., abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789).
    -min, --min_length : Minimum length of the words (default: 4).
    -max, --max_length : Maximum length of the words (default: 6).
    -o, --output_file : Output file name (default: custom_wordlist.txt). Includes timestamp by default.
    -p, --prefix : Prefix for each word (default: "").
    -s, --suffix : Suffix for each word (default: "").
    -e, --exclusions : Characters to exclude from the wordlist (e.g., l1o0).
    -inc, --include_lengths : Specific lengths to include in the wordlist (e.g., 6 8 10).
    -exc, --exclude_lengths : Specific lengths to exclude from the wordlist (e.g., 7 9).
    -t, --threads : Number of threads to use (default: number of CPU cores).
    -z, --compress : Compress the output file using gzip.
    -enc, --encoding : Encoding for the output file (default: utf-8).
    -cfg, --config_file : Path to a JSON configuration file for loading options.
    -r, --regex : Regular expression pattern to filter generated words (e.g., ^[a-zA-Z0-9]{8}$).

## Example Usage
```bash
python3 haruko.py -c "abc123" -min 4 -max 6 -o wordlist.txt -p "pre_" -s "_suf" -e "1l" -inc 6 8 -t 8 -z -enc utf-8 -r "^[a-zA-Z0-9]{6,8}$"
```
*This command generates a wordlist with combinations of abc123, with lengths between 6 and 8 characters, including prefixes and suffixes, compresses the output file, uses 8 threads, and filters words with the specified regex pattern.*

## Warning

THIS TOOL IS INTENDED FOR LEGAL AND ETHICAL USE ONLY. ANY ATTEMPT TO USE IT FOR UNAUTHORIZED ACCESS OR ILLEGAL ACTIVITIES IS PROHIBITED AND WILL BE PURSUED LEGALLY. USE RESPONSIBLY.

## License

This project is licensed under the MIT License
