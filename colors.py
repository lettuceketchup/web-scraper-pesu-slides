from colorama import Fore, Style

# Define colorama functions
def task(str, end = '\n'):
    print(f'{Fore.LIGHTYELLOW_EX}{str}{Style.RESET_ALL}', end = end)
    return str

def success(str, end = '\n'):
    print(f'{Fore.GREEN}{str}{Style.RESET_ALL}', end = end)
    return str

def error(str, end = '\n'):
    print(f'{Fore.RED}{str}{Style.RESET_ALL}', end = end)
    return str

def info_cont(str, end = ''):
    print(f'{Fore.BLUE}{str}{Style.RESET_ALL}', end=end)

def info(str, end = '\n'):
    print(f'{Fore.LIGHTBLUE_EX}{str}{Style.RESET_ALL}', end = end)

def enter(str, end = ''):
    inp = input(f'{Fore.LIGHTYELLOW_EX}{str}{Fore.LIGHTGREEN_EX}')
    print(f'{Style.RESET_ALL}', end=end)
    return inp