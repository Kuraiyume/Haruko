import argparse
import random
import string
import json
import sys
import secrets

def validate_positive_int(value):
    """Ensure that a value is a positive integer."""
    ivalue = int(value)
    if ivalue < 0:
        raise argparse.ArgumentTypeError(f"{value} is not a positive integer.")
    return ivalue

def leet_speak_conversion(custom_string):
    """Convert a string to leet speak."""
    leet_mapping = {
        'a': '4', 'b': '8', 'e': '3', 'g': '6', 'i': '!',
        'l': '1', 'o': '0', 's': '$', 't': '7', 'z': '2',
        'A': '4', 'B': '8', 'E': '3', 'G': '6', 'I': '!',
        'L': '1', 'O': '0', 'S': '$', 'T': '7', 'Z': '2'
    }
    return ''.join(leet_mapping.get(c, c) for c in custom_string)

def generate_password(counts, pools, exclude_chars, prefix, suffix, total_length, secrets_generator, custom):
    """
    Generate a password based on specified counts, total length, or custom string.
    
    :param counts: Dictionary containing the count of each character type
    :param pools: Dictionary of character pools
    :param exclude_chars: Characters to exclude from the password
    :param prefix: Prefix to add to the password
    :param suffix: Suffix to add to the password
    :param total_length: Desired total length of the password
    :param secrets_generator: Random generator instance
    :param custom: Custom string for leet speak conversion
    :return: Generated password
    """
    if custom:
        return leet_speak_conversion(custom)
    
    available_chars = ''.join(pools.values())
    if exclude_chars:
        available_chars = ''.join(c for c in available_chars if c not in exclude_chars)
    
    # Ensure at least one character from each selected pool is present
    password_chars = []
    if total_length > 0:
        for pool in pools.values():
            if pool:
                password_chars.append(secrets_generator.choice(pool))
        
        # Fill the rest of the password with random characters from the combined pool
        remaining_length = total_length - len(password_chars) - len(prefix) - len(suffix)
        if remaining_length > 0:
            password_chars.extend(secrets_generator.choice(available_chars) for _ in range(remaining_length))
    else:
        # Use counts to determine the exact number of each character type
        for char_type, count in counts.items():
            if count > 0:
                password_chars.extend(secrets_generator.choice(pools[char_type]) for _ in range(count))
    
    # Shuffle and ensure total length
    random.shuffle(password_chars)
    
    # Add prefix and suffix
    password = f"{prefix}{''.join(password_chars)}{suffix}"
    
    # Ensure the password meets the total length requirement
    if total_length > 0 and len(password) < total_length:
        additional_chars = [secrets_generator.choice(available_chars) for _ in range(total_length - len(password))]
        password += ''.join(additional_chars)

    return password

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        prog='Password Generator',
        description='Generate customizable passwords with various options.'
    )
    
    parser.add_argument("-n", "--numbers", default=0, type=validate_positive_int, 
                        help="Number of digits in the password")
    parser.add_argument("-l", "--lowercase", default=0, type=validate_positive_int, 
                        help="Number of lowercase characters in the password")
    parser.add_argument("-u", "--uppercase", default=0, type=validate_positive_int, 
                        help="Number of uppercase characters in the password")
    parser.add_argument("-s", "--special-chars", default=0, type=validate_positive_int, 
                        help="Number of special characters in the password")
    
    parser.add_argument("-a", "--amount", default=1, type=validate_positive_int, 
                        help="Number of passwords to generate")
    parser.add_argument("-o", "--output-file", help="File to write the generated passwords to")
    parser.add_argument("--output-format", choices=['txt', 'json'], default='txt',
                        help="Format of the output file (txt or json)")
    parser.add_argument("--exclude-chars", default='', type=str,
                        help="Characters to exclude from the password")
    parser.add_argument("--prefix", default='', type=str,
                        help="Prefix to add to each password")
    parser.add_argument("--suffix", default='', type=str,
                        help="Suffix to add to each password")
    parser.add_argument("--total-length", default=0, type=validate_positive_int,
                        help="Total length of the password (including prefix and suffix). If 0, use specified counts.")
    parser.add_argument("--seed", type=int,
                        help="Seed for randomization to allow reproducible results")
    parser.add_argument("--custom", default='', type=str,
                        help="Custom name for the password with leet speak conversion")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    return args

def main():
    args = parse_arguments()

    if args.seed is not None:
        random.seed(args.seed)
        secrets_generator = random.Random(args.seed)
    else:
        secrets_generator = secrets.SystemRandom()

    pools = {
        'digits': string.digits if args.numbers > 0 else '',
        'lowercase': string.ascii_lowercase if args.lowercase > 0 else '',
        'uppercase': string.ascii_uppercase if args.uppercase > 0 else '',
        'special': string.punctuation if args.special_chars > 0 else ''
    }

    # Ensure at least one pool is included
    if not any(pools.values()) and not args.custom:
        pools = {
            'digits': string.digits,
            'lowercase': string.ascii_lowercase,
            'uppercase': string.ascii_uppercase,
            'special': string.punctuation
        }

    passwords = []
    for _ in range(args.amount):
        try:
            counts = {
                'digits': args.numbers,
                'lowercase': args.lowercase,
                'uppercase': args.uppercase,
                'special': args.special_chars
            }
            
            password = generate_password(
                counts,
                pools,
                args.exclude_chars,
                args.prefix,
                args.suffix,
                args.total_length,
                secrets_generator,
                args.custom
            )

            passwords.append(password)
        except ValueError as e:
            print(f"Error generating password: {e}", file=sys.stderr)
            sys.exit(1)

    output = '\n'.join(passwords)

    if args.output_file:
        if args.output_format == 'json':
            output_data = {"passwords": passwords}
            with open(args.output_file, 'w') as f:
                json.dump(output_data, f, indent=4)
        else:
            with open(args.output_file, 'w') as f:
                f.write(output)

    print(output)

if __name__ == "__main__":
    main()
