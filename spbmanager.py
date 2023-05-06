import argparse, os, sys
import subprocess

from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

from time import sleep

import re

def fatal_error(error_text):
    print(f"{Fore.RED}{error_text}{Style.RESET_ALL}")
    exit()

def dir_path(string):
    if os.path.isfile(string):
        return string
    else:
        fatal_error(f"{string} is not a valid file!")

def extract_yaml_header(text):
    s, header = text.split("\n", 1)
    
    if s.rstrip() == "---":
        i = header.find("\n...")
        if header[i+1:].split('\n', 1)[0].rstrip() == "...":
            return header[:i]
        else:
            fatal_error("Didn't find end of YAML")
    else:
        fatal_error("No YAML-header at start")

def parse_yaml_header(file):
    try:
        import yaml
    except ModuleNotFoundError:
        fatal_error("No python YAML-parsing module found; try installing it with 'pip install yaml'")
    
    header = extract_yaml_header(open(args.input_file, encoding="utf-8").read())
    return yaml.safe_load(header)


def generate_united_yaml(file, settings):
    main = yaml.safe_load(settings)
    inner = parse_yaml_header(file)
    inner_sett = inner.pop("general_options")
    main = main.update(inner_sett)
    if 'metadata' not in main:
        main['metadata'] = {}
    main['metadata'].update(inner)
    yaml.dump(main, open(os.path.join(CUR_PATH, "current_settings.yaml"), 'w', encoding="utf-8"))
    return main

def change_extension(filename, ext):
    ind = filename.rfind('.')
    if ind!=-1:
        filename = filename[:ind]
    return filename+(('.'+ext) if ext else "")

SPB_PATH = os.path.dirname(os.path.realpath(__file__))
CUR_PATH = os.getcwd()

parser = argparse.ArgumentParser(description=f'Pandoc manager tool from {Fore.RED}@sitandr{Style.RESET_ALL}')
subparsers = parser.add_subparsers(dest='command', required=True)

run_parser = subparsers.add_parser('run', help='Runs pandoc and converts file with given yaml')
run_parser.add_argument('input_file', type=dir_path)
run_parser.add_argument('settings')
run_parser.add_argument('-w', '--wait', action="store_true",
                        help="Wait for key press after the end of build if any warnings/errors are present")
run_parser.add_argument('-t', '--tex', action="store_true",
                        help="Compiles output .tex file with tex (engine can be set up with --engine option)")
run_parser.add_argument('--engine', default="pdflatex",
                        help="What engine to use to compile output .tex")

init_parser = subparsers.add_parser('init', help='Creates registry files (dev in progress)')
install_parser = subparsers.add_parser('install', help='Downloads and places filters (coming in far future)')
extract_parser = subparsers.add_parser('extract', help='Extracts yaml (test)')
extract_parser.add_argument('input_file', type=dir_path)

colorama_init()

#print(f"Hello from {Fore.GREEN}sitandr{Style.RESET_ALL}!")

args = parser.parse_args()

if args.command == "extract":
    header = open(args.input_file, encoding="utf-8").read()
    print(extract_yaml_reader(header))
    

# print(args.__dict__)
path_regexp = re.compile(r'((/[a-zA-Z0-9_\.\-]+)+|(?:\\\\[^\\/]+|[a-zA-Z]:[\\/](?:[\w\.\-]+[\\/]?)*))')

def get_settings(settings_name):
    for path in (CUR_PATH, os.path.join(SPB_PATH, 'settings')):
        string = os.path.join(path, args.settings + '.yaml')
        # print(f"Checking {Fore.YELLOW + string + Style.RESET_ALL}")
        if os.path.isfile(string):
            return string
    print(f"{Fore.YELLOW+settings_name+Fore.RED} was not found neither in {Fore.CYAN+CUR_PATH+Fore.RED} nor {Fore.CYAN+SPB_PATH}")
    exit()


def highlight_paths(text, main_color=Style.RESET_ALL):
    text = filter(lambda t: t != None, path_regexp.split(text))
    text = [((Style.RESET_ALL+Fore.CYAN) if i%2 else (Style.RESET_ALL+main_color)) + l
                              for (i, l) in enumerate(text)]

    text = ''.join(text)
    return text


error_hints = {'allowed only in math mode':
              f"Probably, you are using math commands or symbols {Fore.MAGENTA}outside of math env{Fore.YELLOW}; see above for more info"}
def hinter(error):
    for error_msg in error_hints:
        if error_msg in error:
            print(Fore.YELLOW+error_hints[error_msg]+Style.RESET_ALL)
            return

output_file = change_extension(args.input_file, "tex" if args.tex else "")

os.environ["PYTHONUNBUFFERED"] = "1"

total_log = ""
were_any_warnings = False
with subprocess.Popen(["pandoc", args.input_file, "--defaults",
                       get_settings(args.settings),
                      "-o", output_file],
                      close_fds=True,
                      stdout=subprocess.PIPE,
                      stderr=subprocess.PIPE) as process:

    running = True
    while running:
        # pandoc usually puts all logs into stderr
        log = process.stderr.read().decode('utf-8', errors='ignore')
        total_log += log
        running = process.poll()

        for line in log.split("\n"):
            if not line:
                continue
            if line.startswith("[INFO]"):
                line = line[len('[INFO]'):]
                action, line = line.split(maxsplit=1)

                print(f"{Fore.GREEN}{action}{Style.RESET_ALL} {highlight_paths(line)}")
            elif line.startswith("[WARNING]"):
                were_any_warnings = True
                line = line[len('[WARNING]'):]

                print(f"{Fore.YELLOW}{highlight_paths(line, Fore.YELLOW)}{Style.RESET_ALL}")
            else:
                were_any_warnings = True
                print(f"{Fore.RED}{highlight_paths(line, Fore.RED)}{Style.RESET_ALL}")
        sleep(0.2)

if args.tex:
    with subprocess.Popen(args.engine+ ' "' + output_file + '" '
                           + " --interaction=nonstopmode"+ " --halt-on-error"
                           + " 1>&2", # redirect everything to stderr to avoid buffering
                      stdout=subprocess.PIPE,
                      stderr=subprocess.PIPE,
                          shell=True) as process:
        running = True
        last_err = 0
        while running:
            # pdf engines usually put all logs into stderr too

            #process.stdin.write("aa\n")
            log = process.stderr.read().decode('utf-8')
            log += process.stdout.read().decode('utf-8')
            total_log += log
            
            running = process.poll()

            for line in log.split("\n"):
                if not line:
                    continue

                if line.startswith("!"):
                    were_any_warnings = True
                    line = line[1:]

                    last_err = 10
                    print(f"{Fore.RED}{highlight_paths(line, Fore.RED)}{Style.RESET_ALL}")
                elif last_err:
                    print(line)
                    last_err -= 1
            sleep(0.2)

if were_any_warnings:
    hinter(total_log)
    if args.wait:
        input("Press any key…")
else:
    print(f"{Fore.GREEN}All completed{Style.RESET_ALL} succesfuly")
