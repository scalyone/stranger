import sys
import subprocess
import socket
import time
import random
import argparse

class color:
    red = "\033[31m"
    green = "\033[32m"
    yellow = "\033[33m"
    reset = "\033[0m"

def get_mx_records(domain):
    try:
        result = subprocess.run(["dig", "+short", "MX", domain], capture_output=True, text=True, check=True)
        mx_records = result.stdout.strip().split('\n')
        return mx_records
    except subprocess.CalledProcessError as e:
        print(color.red + "Error: " + color.yellow + e + color.reset)
        return []


def send_smtp_commands(**kwargs):

    min_delay = kwargs.get('min_delay', 240)
    max_delay = kwargs.get('max_delay', 360)
    emails = kwargs.get('file')
    if not emails:
        print(color.red + "usage: main.py [-h|--help]\nProvide a file or path to file that contains the list of emails." + color.reset)
        sys.exit(1)
    if min_delay > max_delay:
        print(color.red + "usage: main.py [-h|--help]\nMinimum delay can't be greater than maximum delay." + color.reset)
        sys.exit(1)

    valid_emails = []
    invalid_emails = []

    try:
        with open(emails, 'r') as file:
            for email in file:
                email = email.strip()
                strip_domain = email.split("@")
                domain = strip_domain[1]
                mx_records = get_mx_records(domain)
                if not mx_records:
                    print(color.red + f"No MX records found for: " + color.yellow + f"{domain}" + color.reset)
                    sys.exit(1)
                mx_record = mx_records[0]
                server = mx_record.split()[1][:-1]
                helo = f'HELO {domain}'
                mail_from = "MAIL FROM:<guy@gmail.com>"
                rcpt_to = f'RCPT TO:<{email}>'
                commands = [helo, mail_from, rcpt_to]

                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.connect((server, 25))
                        response = s.recv(1024).decode()

                        for command in commands:
                            s.sendall((command + "\r\n").encode())
                            time.sleep(1)
                            response = s.recv(1024).decode()
                            if command == commands[2]:
                                if response.startswith("550"):
                                     print(color.red + "Invalid: " + color.yellow + email + color.reset)
                                     print(response)
                                     invalid_emails.append(email)
                                     with open("invalid_emails.txt", "w") as invalid_email:
                                         invalid_email.write("\n".join(invalid_emails))
                                elif response.startswith("250"):
                                    print(color.green + "Valid: " + color.yellow + email + color.reset)
                                    valid_emails.append(email)
                                    with open("valid_emails.txt", "w") as valid_email:
                                        valid_email.write("\n".join(valid_emails))
                                else:
                                    print(color.red + "Error: " + color.yellow + response + color.reset)

                    delay = random.uniform(min_delay,max_delay)
                    time.sleep(delay)


                except (socket.timeout, ConnectionRefusedError, ConnectionResetError) as e:
                    print(color.red + "Error: " + color.yellow + e + color.reset)

    except FileNotFoundError:
        print(color.red + f"File '{emails}' not found." + color.reset)
    except Exception as e:
        print(color.red + "An error occurred:" + color.reset, str(e))




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Perform email validation.\n I recommend using the default delay times so your IP is not added to a spam/block list.")
    parser.add_argument("--min", type=int, default=240, help="Minimum delay time (in seconds) before sending requests. DEFAULT: 240 (4 minutes)")
    parser.add_argument("--max", type=int, default=360, help="Maximum delay time (in seconds) before sending requests. DEFAULT 360 (6 minutes)")
    parser.add_argument("--file", type=str, help="File containing a list of just emails to validate. [required]")

    args = parser.parse_args()

    send_smtp_commands(file=args.file, min_delay=args.min, max_delay=args.max)



