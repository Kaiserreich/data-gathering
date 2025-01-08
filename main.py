# By Pelmen#2920, made for Kaiserreich
# The script needs .json config and false positives .txt to work
import json
import logging
import os
import shutil
import subprocess
import sys
import time
import glob
import re
from pathlib import Path

import psutil
import webdriver_form_filler as wdff
import pygetwindow as gw
import win32process

# Configuration and reading files
logging.basicConfig(filename='loop_script.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', filemode='w')
APPLICATION_PATH = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(__file__)


def read_input_file(filename: str) -> dict:
    try:
        if ".json" in filename:
            with open(Path(APPLICATION_PATH) / filename, 'r') as file:
                return json.loads(file.read())
        elif ".txt" in filename:
            with open(Path(APPLICATION_PATH) / filename, 'r') as file:
                return file.read().split('\n')
    except Exception as ex:
        print(ex)
        input(f"Error occurred, can't read input file {filename}")


# -------------------------------- CONFIG ------------------------------

config = read_input_file(filename="config.json")                        # Read config file and return a dict with config parameters

# 1 - Generate logs or not
generate_logs = config["generate_logs"]

# 1.1 - Logs generation settings
NUM_OF_INSTANCES = config["num_of_instances"]                                                                # Number of .exe instances
CPU_AFFINITIES_MODE = config["num_of_threads_per_exe"] if config["num_of_threads_per_exe"] in [2, 4] else 2  # Number of threads per exe. Defaults to 2
TIMES_TO_LAUNCH = config["times_to_launch"]                             # How many times to launch the game in a row
GAME_DURATION = config["game_duration_minutes"] * 60                    # How long each game will last before killed
FALSE_POSITIVE_LINES = read_input_file(filename="false_positives.txt")  # list with false positives from external file

# 1.2 Paths
HOI_PATH = config["hoi4_exe_fullpath"]                                 # Path to hoi4 exe
LOGS_PATH = Path(os.environ.get('USERPROFILE')) / "Documents" / "Paradox Interactive" / "Hearts of Iron IV" / "logs" if "custom_logs_path" not in config.keys() else config["custom_logs_path"]
PATH_TO_SETTINGS = Path(os.environ.get('USERPROFILE')) / "Documents" / "Paradox Interactive" / "Hearts of Iron IV" / "settings.txt" if "custom_settings_path" not in config.keys() else config["custom_settings_path"]
PATH_TO_PDX_SETTINGS = Path(os.environ.get('USERPROFILE')) / "Documents" / "Paradox Interactive" / "Hearts of Iron IV" / "pdx_settings.txt" if "custom_pdx_settings_path" not in config.keys() else config["custom_pdx_settings_path"]

# 1.3 Hoi4 args
ENABLE_CRASH_LOGGING = config["crash_logging"]                         # hoi4 arg
ENABLE_DEBUG_MODE = config["debug_mode"]                               # hoi4 arg
ENABLE_HANDS_OFF = True if "hands_off" not in config.keys() else config["hands_off"]                                 # hoi4 arg

affinities_list_for_2_threads_per_exe = [[i, i + 1] for i in [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22]]
affinities_list_for_4_threads_per_exe = [[i, i + 1, i + 2, i + 3] for i in [0, 4, 8, 12, 16, 18, 20]]
if "cpu_affinities_override" in config.keys():
    CPU_AFFINITIES_LIST = json.loads(config["cpu_affinities_override"])
else:
    CPU_AFFINITIES_LIST = affinities_list_for_4_threads_per_exe if CPU_AFFINITIES_MODE == 4 else affinities_list_for_2_threads_per_exe

# 2 - Process logs and send data to google forms
publish_to_google_form = config["publish_to_google_form"]
raw_backup_files_path = Path(APPLICATION_PATH) / "game_log_files" / "backup"
exception_path = Path(APPLICATION_PATH) / "game_log_files" / "exception"

# 3 - Additionally clean generated error.log files if needed
if "clean_error_log_files" in config.keys():
    clean_error_log_files = config["clean_error_log_files"]
else:
    clean_error_log_files = False

# -------------------------------- Functions code ------------------------------


def launch_the_game(run: int, instance: int, cpu_affinity: list):
    """Function that governs game running

    Args:
        run (int): Number of iteration. Used for logging and files naming
        instance (int): Instance number.
        cpu_affinity (list): What CPU affinity to assign to the particular instance.
    Returns:
        game (obj): Game process object. Used to kill it later
    """
    game_setup = f'{HOI_PATH} -nolauncher -debug_smooth=no -start_minimized {"-hands_off" if ENABLE_HANDS_OFF else "-start_tag=BHU -start_speed=4"} {"-crash_data_log" if ENABLE_CRASH_LOGGING else ""} {"-debug" if ENABLE_DEBUG_MODE else ""} -historical=no -logpostfix=_{instance}'
    game = subprocess.Popen(game_setup)
    process_id = game.pid
    game_process = psutil.Process(pid=process_id)
    game_process.cpu_affinity(cpu_affinity)
    print(f"{time.strftime('%H:%M', time.localtime())} - Started the run #{run}/{TIMES_TO_LAUNCH}, run duration - {GAME_DURATION} seconds, logpostfix - _{instance}")
    logging.info(f"Started the run #{run}/{TIMES_TO_LAUNCH}, run duration - {GAME_DURATION} seconds, args - {game_setup}")
    return game


def process_error_log(filepath):
    print(f'Processing error.log {os.path.basename(filepath)}')
    logging.info(f'Processing error.log {os.path.basename(filepath)}')

    with open(filepath, 'r', encoding='utf-8-sig') as initial_error_log:                            # Open log file
        initial_error_log = initial_error_log.read()

    initial_error_log = initial_error_log.split("\n")
    cleared_error_log = initial_error_log.copy()

    for line in initial_error_log:                                                                  # Remove lines that contain text from false positives
        for check in FALSE_POSITIVE_LINES:
            if check in line:
                try:
                    cleared_error_log.remove(line)
                except Exception:
                    continue

    os.remove(filepath)

    with open(filepath, 'w', encoding='utf-8-sig') as new_file:                                     # Create cleaned log file
        new_file.write("\n".join(cleared_error_log))


def copy_log_file(run: int, instance: int, log_type: str):
    if log_type == "game_log":
        shutil.copyfile(Path(LOGS_PATH) / f'game_{instance}.log', Path(APPLICATION_PATH) / 'game_log_files' / f'game_log_instance_{instance}_run#{run}_{time.strftime('%Y%m%d_%H%M', time.localtime())}.log')
        shutil.copyfile(Path(LOGS_PATH) / f'game_{instance}.log', Path(APPLICATION_PATH) / 'error_log_files' / f'game_log_instance_{instance}_run#{run}_{time.strftime('%Y%m%d_%H%M', time.localtime())}.log')
    elif log_type == "error_log":
        error_log_name = f"error_log_instance_{instance}_run#{run}_{time.strftime('%Y%m%d_%H%M', time.localtime())}.log"
        error_log_path = Path(APPLICATION_PATH) / 'error_log_files' / error_log_name
        shutil.copyfile(Path(LOGS_PATH) / f'error_{instance}.log', error_log_path)
        return error_log_path


def change_game_settings():
    MIN_SETTINGS = {
        'size': '{ x=320 y=240 }',
        'max_refresh_rate': '30',
        'fullScreen': 'no',
        'borderless': 'no',
        'shadows': 'no',
        'multi_sampling': '0',
        'maxanisotropy': '0',
        'vsync': 'no',
        'master_volume': '0',
        'draw_trees': 'no',
        'draw_rivers': 'no',
        'draw_postfx': 'no',
        'draw_hires_terrain': 'no',
        'draw_citysprawl': 'no',
        'draw_shadows': 'no',
        'draw_weather_effects': 'no',
        'draw_water_reflections': 'no',
        'draw_units': 'no',
        'draw_buildings': 'no',
        'high_gfx_shaders': 'no',
        'draw_map_full_res': 'no',
        'texture_quality': '2',
        'hide_daynight_cycle': 'yes',
        'autosave': '"NEVER"',
        'pause_on_popups': 'no',
    }

    with open(PATH_TO_SETTINGS, 'r', encoding='utf-8') as text_file:
        settings_file = text_file.read()
        changed_settings_file = settings_file
        backup_file = settings_file
        for key in MIN_SETTINGS.keys():
            try:
                pattern = key + r'=(.*)'
                value = re.findall(pattern, settings_file)[0]
                changed_settings_file = changed_settings_file.replace(key + '=' + value, key + '=' + MIN_SETTINGS[key])
            except Exception:
                print(f"Setting {key} is missing")
                logging.info(f"Setting {key} is missing")
                continue

    with open(PATH_TO_SETTINGS, 'w', encoding='utf-8') as text_file_write:
        text_file_write.write(changed_settings_file)

    print('Game settings changed')
    logging.info('Game settings changed')
    return backup_file


def change_pdx_game_settings():
    MIN_SETTINGS = {
        '"windowed_resolution"': 'value="320x240"',
    }

    with open(PATH_TO_PDX_SETTINGS, 'r', encoding='utf-8') as text_file:
        settings_file = text_file.read()
        changed_settings_file = settings_file
        backup_file = settings_file
        for key in MIN_SETTINGS:
            try:
                pattern = re.findall(key + r'=\{.*?\}', settings_file, flags=re.MULTILINE | re.DOTALL)[0]
                value = re.findall(r'value.*', pattern)[0]
                changed_settings_file = changed_settings_file.replace(pattern, pattern.replace(value, MIN_SETTINGS[key]))
            except Exception:
                print(f"Setting {key} is missing")
                logging.info(f"Setting {key} is missing")
                continue

    with open(PATH_TO_PDX_SETTINGS, 'w', encoding='utf-8') as text_file_write:
        text_file_write.write(changed_settings_file)

    print('Screen resolution changed')
    logging.info('Screen resolution changed')
    return backup_file


def revert_game_settings(backup_file: str, path: str):
    with open(path, 'w', encoding='utf-8') as text_file_write:
        text_file_write.write(backup_file)

    print('Game settings reverted')
    logging.info('Game settings reverted')


def minimize_window(game_processes: list[subprocess.Popen]):
    # Check if the platform is Windows
    if os.name == 'nt':  # Windows

        # Get process IDs
        pids = [i.pid for i in game_processes]

        # Find windows corresponding to each PID
        windows = gw.getAllWindows()    # Get all open windows (no title filter)
        for window in windows:
            try:
                hwnd = window._hWnd  # Get the window handle (HWND)
                # Get the PID associated with the window handle (HWND)
                _, pid = win32process.GetWindowThreadProcessId(hwnd)

                if pid in pids:
                    window.minimize()
            except psutil.NoSuchProcess:
                # Handle any potential error where the process doesn't exist
                print("Window minimize failed")
                continue


def main():
    print("Hoi4 launch script/form filler by Pelmen#2920. Make sure you set correct paths in config file. Starting the script...\n\n")
    if generate_logs:
        backup_settings = change_game_settings()
        backup_pdx_settings = change_pdx_game_settings()
        for run in range(1, TIMES_TO_LAUNCH + 1):
            try:
                game_processes_list = []

                for instance in range(NUM_OF_INSTANCES):                                                        # 1. Launch all games
                    game_processes_list.append(launch_the_game(run, instance, CPU_AFFINITIES_LIST[instance]))

                time.sleep(10)
                minimize_window(game_processes_list)                                                            # 1.01 Minimize opened windows
                time.sleep(GAME_DURATION)

                for game in game_processes_list:                                                                # 1.1. Kill all games
                    game.kill()
            except Exception as ex:
                logging.error(ex)
                print(ex)
                continue

            for instance in range(NUM_OF_INSTANCES):                                                            # 1.2. Process logs for all instances
                try:
                    copy_log_file(run, instance, log_type="game_log")                                           # Copy game.log file to storage
                    error_log_path = copy_log_file(run, instance, log_type="error_log")                         # Copy error.log file to storage
                    process_error_log(error_log_path)                                                           # Process error.log
                    print(f"{time.strftime('%H:%M', time.localtime())} - The run #{run}/{TIMES_TO_LAUNCH} is over!")
                    logging.info(f"The run #{run}/{TIMES_TO_LAUNCH} is over!")
                except Exception as ex:
                    logging.error(ex)
                    print(ex)
                    continue

        revert_game_settings(backup_file=backup_settings, path=PATH_TO_SETTINGS)
        revert_game_settings(backup_file=backup_pdx_settings, path=PATH_TO_PDX_SETTINGS)

    if publish_to_google_form:
        try:
            path = Path(APPLICATION_PATH) / 'game_log_files'
            path = str(path / 'game**.log')
            for filename in glob.iglob(path):
                print(f"{time.strftime('%H:%M', time.localtime())} - Processing {os.path.basename(filename)}")
                with open(filename, 'r', encoding='utf-8-sig') as file:
                    log_file = file.read().split('\n')                                                           # Extract lines from game.log
                    x = {line.split(";")[1]: line.split(";")[2] for line in log_file if "KR_Event_Logging" in line}
                    data_to_report = dict(sorted(x.items(), key=lambda item: item[1][-4:]))                     # Sort log dict to get correct ending date
                    data_to_report["END"] = list(data_to_report.values())[-1]
                    data_to_report.update({line.split(": ")[1]: "8:00, 1 March, 1937" for line in log_file if "_data" in line})
                    for key, value in data_to_report.items():
                        if "_data" not in key:
                            print("\t\t{: <40} {: <40}".format(key, value))                                      # Print info in console
                try:
                    wdff.fill_google_form(wdff.extract_data_for_webdriver_script(log_data=data_to_report))       # Send logs to forms
                    shutil.move(filename, raw_backup_files_path)
                except wdff.DateException:
                    print("Skipping and saving to exceptional log directory...")
                    shutil.move(filename, exception_path)
                    
        except Exception as ex:
            print(ex)

    if clean_error_log_files:
        print('Cleaning up error.log files')
        logging.info('Cleaning up error.log files')
        try:
            path = Path(APPLICATION_PATH) / 'error_log_files'
            path = str(path / 'error**.log')
            for filepath in glob.iglob(path):
                print(f"{time.strftime('%H:%M', time.localtime())} - Processing {os.path.basename(filepath)}")
                process_error_log(filepath)
        except Exception as ex:
            logging.error(ex)
            print(ex)

    print(f"{time.strftime('%H:%M', time.localtime())} - The session is finished")
    logging.info("The session is finished")
    input("Press any key to exit")


if __name__ == '__main__':
    main()
