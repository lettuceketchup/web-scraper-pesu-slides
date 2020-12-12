from colorama import Fore, Style

# Define colorama functions
def task(str):
    print(f'{Fore.LIGHTYELLOW_EX}{str}{Style.RESET_ALL}')
    return str

def success(str):
    print(f'{Fore.GREEN}{str}{Style.RESET_ALL}')
    return str

def error(str):
    print(f'{Fore.RED}{str}{Style.RESET_ALL}')
    return str

def info_cont(str):
    print(f'{Fore.BLUE}{str}{Style.RESET_ALL}', end='')

def info(str):
    print(f'{Fore.LIGHTBLUE_EX}{str}{Style.RESET_ALL}')
