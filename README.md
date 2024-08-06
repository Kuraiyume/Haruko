# HARUKO - An Advanced Password Wordlist Generator for Brute-Force an Dictionary Attacks

HARUKO is a robust tool designed to generate customizable password wordlists for brute-force attacks.

## [+] Features

- **Customizable Wordlists:** Create wordlists with specific character sets, lengths, and patterns.
- **Year Formatting:** Add formatted year information to your wordlists with customizable positions and formats.
- **Delimiter Support:** Use custom delimiters between characters and years.
- **Compression Support:** Optionally compress the output file for efficient storage.
- **Multithreaded Processing:** Utilize multiple CPU threads for faster generation.
- **Configurable Encoding:** Choose the encoding for the output file.
- **Pattern Filtering:** Use regular expressions to filter generated words.

## [+] Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/veilwr4ith/haruko
   ```

2. **Install gzip:**
   ```bash
   apt install gzip
   ```

3. **Navigate to the directory:**
   ```bash
   cd Haruko
   ```

4. **Run the script to show up the Main Menu:**
   ```bash
   python3 haruko.py
   ```

## [+] Available Parameters

| Parameters        | Description                                                                                       | Example                                     |
|---------------|---------------------------------------------------------------------------------------------------|---------------------------------------------|
| `-c, --characters`   | Set of characters to include in the wordlist.                                                   | `abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789` |
| `-min, --min_length` | Minimum length of the words (default: 4).                                                        | `4`                                         |
| `-max, --max_length` | Maximum length of the words (default: 6).                                                        | `6`                                         |
| `-o, --output_file`  | Output file name (default: `custom_wordlist.txt`). Includes timestamp by default.                | `custom_wordlist.txt`                      |
| `-p, --prefix`       | Prefix for each word (default: "").                                                                | `"pre_"`                                    |
| `-s, --suffix`       | Suffix for each word (default: "").                                                                | `"_suf"`                                    |
| `-e, --exclusions`   | Characters to exclude from the wordlist.                                                           | `l1o0`                                      |
| `-inc, --include_lengths` | Specific lengths to include in the wordlist.                                                   | `6 8 10`                                    |
| `-exc, --exclude_lengths` | Specific lengths to exclude from the wordlist.                                                   | `7 9`                                       |
| `-t, --threads`      | Number of threads to use (default: number of CPU cores).                                           | `8`                                         |
| `-z, --compress`     | Compress the output file using gzip.                                                               | (no argument, but file will be compressed) |
| `-enc, --encoding`   | Encoding for the output file (default: utf-8).                                                     | `utf-8`                                     |
| `-cfg, --config_file`| Path to a JSON configuration file for loading options.                                             | `config.json`                               |
| `-r, --regex`        | Regular expression pattern to filter generated words.                                             | `^[a-zA-Z0-9]{8}$`                          |
| `-y, --year_range`   | Year range to include, formatted as `start_year-end_year`.                                         | `2020-2023`                                 |
| `-yp, --year_position`| Position to place the year: 'prefix', 'suffix', or specific position index (e.g., '2').             | `suffix`                                    |
| `-yf, --year_format` | Year format: 'YY', 'YYYY', 'MMYY'.                                                                 | `YYYY`                                      |
| `-yd, --year_delimiters`| Delimiters to use between words and years, separated by spaces (e.g., '-', '_', '').               | `- _`                                       |
| `--no-timestamp`     | Exclude timestamp from the output file name.                                                       | (no timestamp in file name)                |

## [+] Basic Usage

   ```bash
   python3 haruko.py -c abc123 -min 1 -max 6 -o wordlist.txt
   ```
*This command generates a wordlist with combinations of abc123, with lengths between 1 and 6 characters, with an output file name of wordlist.txt*

## [+] License

- This project is licensed under MIT License




