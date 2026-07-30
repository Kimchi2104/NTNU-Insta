# ==============================================================================
# This script is used to generate JKC synthetic photometry from a given Gaia XP continuous spectrum file
# ==============================================================================

import os
import sys
from gaiaxpy import generate, PhotometricSystem


def main(in_file, out_dir):
    # Get the base name without the extension
    base_name = os.path.basename(in_file)
    generate(in_file, PhotometricSystem.JKC, save_file=True, output_file=base_name, output_path=out_dir)


if __name__ == '__main__':
    # Get the path from command line arguments
    if len(sys.argv) != 3:
        print("Usage: python gaiaxpy_phot.py <input_file> <output_directory>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_directory = sys.argv[2]

    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Process the files
    main(input_file, output_directory)
