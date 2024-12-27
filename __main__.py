import sys
import ssg
import argparse

# Instantiate the parser
parser = argparse.ArgumentParser(description='Static Site Generator for a photo blog')
parser.add_argument("-t", "--theme", help="Web site theme")
parser.add_argument("-p", "--photos", help="photos location")
parser.add_argument("config_file", help="config file")
parser.add_argument("output_path", help="output location")
args = parser.parse_args()

theme = args.theme
photos = args.photos
config_file = args.config_file
output_path = args.output_path
sys.exit(ssg.main(theme, photos, config_file, output_path))