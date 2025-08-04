import os
import argparse
import logging
from glob import glob
from PIL import Image

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, help="Path to input data folder (e.g., daisies)")
    parser.add_argument("--output_data", type=str, help="Path to output data folder")
    args = parser.parse_args()

    print(" ".join(f"{k}={v}" for k, v in vars(args).items()))

    print("Input data folder:", args.data)
    print("Output folder:", args.output_data)

    output_dir = args.output_data
    size = (64, 64)

    for file in glob(args.data + "/*.jpg"):
        img = Image.open(file)
        img_resized = img.resize(size)
        output_file = os.path.join(output_dir, os.path.basename(file))
        img_resized.save(output_file)

if __name__ == "__main__":
    main()