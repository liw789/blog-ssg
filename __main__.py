import sys
from . import ssg
import argparse

def main():
    parser = argparse.ArgumentParser(description='Static Site Generator for a photo blog')
    parser.add_argument("-t", "--theme", help="Web site theme")
    parser.add_argument("-s", "--source", help="source location")
    parser.add_argument("output_path", help="output location")
    args = parser.parse_args()

    theme = args.theme
    output_path = args.output_path
    source = args.source
    sys.exit(ssg.generate(theme, source, output_path))

if __name__ == "__main__":
    main()