#!/usr/bin/env python3
import re
import sys
import argparse
from reposcore.main import main

if __name__ == "__main__":
    urlPattern = r'''https://github\.com/([\w-]+)/([\w-]+)(\.git)?$'''
    parser = argparse.ArgumentParser(description='Provide repo url to scan')
    parser.add_argument('--url', type=str, help='Github repo url')
    urls = parser.parse_args()
    
    main(url=urls.url)
