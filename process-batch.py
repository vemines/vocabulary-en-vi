import os
import re
import subprocess
import time

# Function to get the list of part numbers from files starting with part_ and ending with .txt
def get_part_numbers(directory):
    part_numbers = []

    # Iterate over all files in the directory
    for filename in os.listdir(directory):
        match = re.match(r'part_(\d+)\.txt', filename)
        if match:
            part_numbers.append(int(match.group(1)))

    return sorted(part_numbers)

def execute_batch(part_numbers, directory):
    """
    Executes a batch of commands based on part numbers. Each command runs `process.py`.
    """
    for part_number in part_numbers:
        part_file = f"part_{part_number}.txt"
        output_file = f"_part_{part_number}.txt"
        command = f'python process.py {part_file} {output_file}'

        # Execute the command in a new command prompt window
        subprocess.Popen(['cmd', '/K', command])
        print(f"Started process for {part_file}...")

def monitor_and_process(directory, check_interval=300):
    """
    Monitors the directory for changes in part_* files, processes them in batches, 
    and stops after no progress is detected within the interval.
    """
    last_len = 0  # Store the previous length of part files

    while True:
        # Get the current list of part numbers
        part_numbers = get_part_numbers(directory)

        # If the length hasn't changed, break the loop
        if len(part_numbers) == last_len or len(part_numbers) == 0:
            print(f"Part files length not change. Breaking the loop.")
            break  # Exit the loop if no new part files

        # If the length has changed, process the batch
        last_len = len(part_numbers)  # Update the last known length

        # Execute a batch of part files, process the first 10 files in each iteration
        batch_size = 10
        execute_batch(part_numbers[:batch_size], directory)

        # After processing the batch, wait for the specified interval before checking again
        print(f"Waiting for {check_interval // 60} minutes before excute again...")
        time.sleep(check_interval)

directory = '.'  # Directory target
monitor_and_process(directory, 300)
