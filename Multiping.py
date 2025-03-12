import os
import time
import threading
from collections import defaultdict
import colorama
from colorama import Fore, Style
import subprocess

# Initialize colorama
colorama.init()

# Store ping results
ping_results = defaultdict(list)

# Global flag for emergency break
emergency_stop = False

# Global flag for RGB credits thread
rgb_running = False

# ASCII Logo
ASCII_LOGO = r"""
  ____  _       _  _____ __  __    _    ____ _____ ____  
 |  _ \| |     | |/ /_ _|  \/  |  / \  / ___|_   _/ ___| 
 | |_) | |     | ' / | || |\/| | / _ \ \___ \ | | \___ \ 
 |  __/| |___  | . \ | || |  | |/ ___ \ ___) || |  ___) |
 |_|   |_____| |_|\_\___|_|  |_/_/   \_\____/ |_| |____/ 
"""

# RGB Switching Colors for Credits
def rgb_credits():
    global rgb_running
    colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]
    while rgb_running:
        for color in colors:
            if not rgb_running:
                break
            print(f"{color}Made by joseitoxx2{Style.RESET_ALL}", end="\r")
            time.sleep(0.5)

# Start Menu
def start_menu():
    print(f"{Fore.CYAN}{ASCII_LOGO}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}=== PingMaster - Network Testing Tool ==={Style.RESET_ALL}")
    print(f"{Fore.GREEN}1. Start Pinging{Style.RESET_ALL}")
    print(f"{Fore.GREEN}2. Help{Style.RESET_ALL}")
    print(f"{Fore.GREEN}3. Credits{Style.RESET_ALL}")
    print(f"{Fore.RED}0. Exit{Style.RESET_ALL}")

    choice = input(f"{Fore.CYAN}Enter your choice: {Style.RESET_ALL}")
    return choice

# Help Menu
def help_menu():
    while True:
        print(f"{Fore.YELLOW}=== Help Menu ==={Style.RESET_ALL}")
        print(f"{Fore.GREEN}1. What is DNS?{Style.RESET_ALL}")
        print(f"{Fore.GREEN}2. Why was this program made?{Style.RESET_ALL}")
        print(f"{Fore.GREEN}3. Packet Sizes{Style.RESET_ALL}")
        print(f"{Fore.GREEN}4. Multithreading{Style.RESET_ALL}")
        print(f"{Fore.GREEN}5. General Help{Style.RESET_ALL}")
        print(f"{Fore.GREEN}6. Common Issues{Style.RESET_ALL}")
        print(f"{Fore.GREEN}7. Other Issues{Style.RESET_ALL}")
        print(f"{Fore.RED}0. Back to Main Menu{Style.RESET_ALL}")

        choice = input(f"{Fore.CYAN}Enter your choice: {Style.RESET_ALL}")
        if choice == "1":
            print(f"{Fore.CYAN}DNS (Domain Name System) is a system that translates human-readable domain names into IP addresses.{Style.RESET_ALL}")
        elif choice == "2":
            print(f"{Fore.CYAN}This program was made for testing network connectivity and performance.{Style.RESET_ALL}")
        elif choice == "3":
            print(f"{Fore.CYAN}Packet size refers to the size of the data packet sent during a ping. Larger packets can test network capacity.{Style.RESET_ALL}")
        elif choice == "4":
            print(f"{Fore.CYAN}Multithreading allows the program to perform multiple pings simultaneously, improving efficiency.{Style.RESET_ALL}")
        elif choice == "5":
            print(f"{Fore.CYAN}For general help, refer to the program's documentation or contact support.{Style.RESET_ALL}")
        elif choice == "6":
            print(f"{Fore.CYAN}Common issues include unreachable domains, network restrictions, or incorrect settings.{Style.RESET_ALL}")
        elif choice == "7":
            print(f"{Fore.CYAN}For other issues, please provide detailed information to the developer.{Style.RESET_ALL}")
        elif choice == "0":
            break
        else:
            print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")

# Credits
def show_credits():
    global rgb_running
    rgb_running = True
    print(f"{Fore.YELLOW}=== Credits ==={Style.RESET_ALL}")
    rgb_thread = threading.Thread(target=rgb_credits, daemon=True)
    rgb_thread.start()
    input(f"{Fore.CYAN}Press Enter to return to the main menu...{Style.RESET_ALL}")
    rgb_running = False  # Stop the RGB thread
    time.sleep(0.5)  # Allow the thread to exit gracefully
    print("\033[K", end="")  # Clear the line

# Check Domain
def check_domain(domain):
    """Check if the domain exists or is reachable."""
    try:
        if os.name == "posix":  # Unix-based systems (Linux, macOS)
            response = subprocess.run(
                ["ping", "-c", "1", domain],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
        elif os.name == "nt":  # Windows
            response = subprocess.run(
                ["ping", "-n", "1", domain],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
        else:
            print(f"{Fore.RED}Unsupported operating system.{Style.RESET_ALL}")
            return False

        return response.returncode == 0
    except Exception as e:
        print(f"{Fore.RED}Error checking domain: {e}{Style.RESET_ALL}")
        return False

# Ping Domain
def ping_domain(domain, count, interval, packet_size, thread_id):
    global emergency_stop
    for i in range(count):
        if emergency_stop:
            print(f"{Fore.YELLOW}Thread {thread_id}: Emergency stop triggered.{Style.RESET_ALL}")
            break

        try:
            if os.name == "posix":  # Unix-based systems (Linux, macOS)
                command = ["ping", "-c", "1", "-s", str(packet_size), domain]
            elif os.name == "nt":  # Windows
                command = ["ping", "-n", "1", "-l", str(packet_size), domain]
            else:
                print(f"{Fore.RED}Unsupported operating system.{Style.RESET_ALL}")
                return

            response = subprocess.run(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )

            if response.returncode == 0:
                result = f"{Fore.GREEN}Thread {thread_id}: Ping {i+1} to {domain} with {packet_size} bytes was successful!{Style.RESET_ALL}"
            else:
                result = f"{Fore.RED}Thread {thread_id}: Ping {i+1} to {domain} with {packet_size} bytes failed.{Style.RESET_ALL}"

            ping_results[thread_id].append(result)
            print(result)
            time.sleep(interval)
        except Exception as e:
            print(f"{Fore.RED}Error in thread {thread_id}: {e}{Style.RESET_ALL}")

# Emergency Break Listener
def emergency_break_listener():
    global emergency_stop
    e_count = 0
    while True:
        if input() == "e":
            e_count += 1
            if e_count == 3:
                emergency_stop = True
                print(f"{Fore.RED}Emergency stop activated!{Style.RESET_ALL}")
                break
        else:
            e_count = 0

# Main Pinging Function
def start_pinging():
    global emergency_stop
    emergency_stop = False

    print(f"{Fore.YELLOW}=== Multi-Threaded Ping Utility ==={Style.RESET_ALL}")

    domain = input(f"{Fore.CYAN}Enter the domain to ping (e.g., google.com): {Style.RESET_ALL}")
    if not check_domain(domain):
        print(f"{Fore.RED}Error: Domain '{domain}' is not reachable.{Style.RESET_ALL}")
        return

    count = input(f"{Fore.CYAN}Enter the number of times to ping (default: 4): {Style.RESET_ALL}")
    count = int(count) if count.isdigit() else 4

    interval = input(f"{Fore.CYAN}Enter the interval between pings in seconds (default: 1): {Style.RESET_ALL}")
    interval = int(interval) if interval.isdigit() else 1

    packet_size = input(f"{Fore.CYAN}Enter the packet size in bytes (default: 64): {Style.RESET_ALL}")
    packet_size = int(packet_size) if packet_size.isdigit() else 64

    threads = input(f"{Fore.CYAN}Enter the number of threads to use (default: 2): {Style.RESET_ALL}")
    threads = int(threads) if threads.isdigit() else 2

    # Start emergency break listener
    break_thread = threading.Thread(target=emergency_break_listener, daemon=True)
    break_thread.start()

    # Create and start threads
    thread_list = []
    for i in range(threads):
        thread = threading.Thread(target=ping_domain, args=(domain, count, interval, packet_size, i+1))
        thread_list.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in thread_list:
        thread.join()

    # Display statistics
    display_statistics()

    # Save results to file
    save_option = input(f"{Fore.CYAN}Do you want to save the results to a file? (y/n): {Style.RESET_ALL}").strip().lower()
    if save_option == "y":
        save_results_to_file()

    # Keep the program running until the user decides to exit
    while True:
        user_input = input(f"{Fore.CYAN}\nType 'exit' to quit, 'restart' to run again, or 'stats' to view statistics: {Style.RESET_ALL}").strip().lower()
        if user_input == "exit":
            print(f"{Fore.YELLOW}Exiting the program. Goodbye!{Style.RESET_ALL}")
            break
        elif user_input == "restart":
            start_pinging()  # Restart the program
            break
        elif user_input == "stats":
            display_statistics()
        else:
            print(f"{Fore.RED}Invalid input. Please type 'exit', 'restart', or 'stats'.{Style.RESET_ALL}")

# Main Program
def main():
    while True:
        choice = start_menu()
        if choice == "1":
            start_pinging()
        elif choice == "2":
            help_menu()
        elif choice == "3":
            show_credits()
        elif choice == "0":
            print(f"{Fore.RED}Exiting the program. Goodbye!{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
