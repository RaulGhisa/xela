import logging
import os
import signal
import psutil


def find_and_kill_process(process_name):
    """
        credits: Claude.ai

        Find a process by name and kill it if found.

        Args:
            process_name (str): Name of the process to find and kill

        Returns:
            bool: True if process was found and killed, False otherwise
    """
    found = False

    # Iterate through all running processes
    for proc in psutil.process_iter(['pid', 'name']):
        if process_name.lower() in proc.info['name'].lower():
            pid = proc.info['pid']
            try:
                os.kill(pid, signal.SIGTERM)
                logging.debug(f"Process '{process_name}' with PID {pid} terminated successfully.")
                found = True
            except (ProcessLookupError, PermissionError) as e:
                logging.debug(f"Failed to terminate process '{process_name}' with PID {pid}: {e}")

    if not found:
        logging.debug(f"No process with name '{process_name}' found.")

    return found
