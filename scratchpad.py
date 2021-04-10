# only for python code snippets
# do not run this script

import sys

if sys.platform.startswith("linux"):
    print("Linux OS detected")
    # executable_path = "./binaries/chromedriver"
    # chrome_options.BinaryLocation = "/usr/bin/chromium-browser"
elif sys.platform.startswith("win"):
    print("Windows OS detected")
    # executable_path = "./binaries/chromedriver.exe"
else:
    raise ValueError("Unknown OS")
