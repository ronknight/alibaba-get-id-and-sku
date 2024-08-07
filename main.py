import subprocess
import sys

def run_program(program_name):
    try:
        result = subprocess.run(['python', program_name], capture_output=True, text=True, check=True)
        print(f"Output of {program_name}:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error running {program_name}:\n{e.stderr}")

if __name__ == "__main__":
    # Run productlist.py with the required arguments
    run_program('productlist.py')

    # Run parse_id_sku.py
    run_program('parse_id_sku.py')
