# A dummy vulnerable app for Strix to scan
import os
import sys

def process_data(user_input):
    print("Processing:", user_input)
    # WARNING: Intentional Remote Code Execution vulnerability
    # Do not use in production!
    eval(user_input)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        process_data(sys.argv[1])
    else:
        print("Provide input to process.")
