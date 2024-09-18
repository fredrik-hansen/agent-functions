# filename: ssh_executor.py
"""This script takes the host, username and command as arguments from the command line. You can run it like this:
```bash
python ssh_executor.py <host> <username> "<command>"
```
Replace `<host>` with your hostname or IP address, `<username>` with your SSH username and `<command>` with the actual command you want to execute.#

I used `sys.argv` to get the arguments from the command line. This is a simple way to pass arguments to a Python script.

pip install paramiko socket

"""


import paramiko
import sys
import os
import socket


def validate_input(host, username):
    """
    Validate user input for host and username.
    
    Args:
        host (str): Hostname or IP address of the remote server.
        username (str): Username to use for SSH connection.

    Returns:
        bool: True if all inputs are valid, False otherwise.
    """
    if not isinstance(host, str) or len(host.strip()) == 0:
        print("Error: Hostname/IP address is required.")
        return False
    if not isinstance(username, str) or len(username.strip()) == 0:
        print("Error: Username is required.")
        return False

    try:
        socket.gethostbyname(host)
    except socket.gaierror:
        print(f"Error: Unable to resolve hostname/IP address '{host}'.")
        return False

    # Check if SSH key exists in ~/.ssh folder
    ssh_key_path = os.path.expanduser('~/.ssh/id_rsa')
    if not os.path.exists(ssh_key_path):
        print("Error: No SSH key found in ~/.ssh folder.")
        return False

    return True


def execute_ssh_command(host, username, command):
    """
    Execute a remote SSH command on the specified host using an SSH key.

    Args:
        host (str): Hostname or IP address of the remote server.
        username (str): Username to use for SSH connection.
        command (str): Command to execute on the remote host.

    Returns:
        str: Output from the executed command, or an error message if execution failed.
    """
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Connect to remote host using SSH key
        ssh.connect(host, username=username, key_filename=os.path.expanduser('~/.ssh/id_rsa'))
        
        # Execute command and capture output
        stdin, stdout, stderr = ssh.exec_command(command)
            
        # Get output from executed command
        output = stdout.read().decode('utf-8')
                    
        return output
    
    except paramiko.SSHException as e:
        return f"Error: SSH connection to host '{host}' failed - {e}"
    
    finally:
        ssh.close()


def main():
    """
    Main program entry point.
    
    Prompts user for input, validates it and executes the remote SSH command if valid.
    """
    
    print("SSH Remote Command Executor")
     
    # Get arguments from command line
    if len(sys.argv) != 4:
       print("Usage: python ssh_executor.py <host> <username> <command>")
       sys.exit(1)
            
    host = sys.argv[1]
    username = sys.argv[2]
    command = ' '.join(sys.argv[3:])
                       
    # Validate input
    if validate_input(host, username):
       output = execute_ssh_command(host, username, command)

       print(output)


if __name__ == "__main__":
    main()

