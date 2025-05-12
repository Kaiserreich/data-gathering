from selenium import webdriver                                    # Webdriver
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager          # Auto-download webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait           # Explicit wait for verification
from selenium.webdriver.support import expected_conditions as EC  # Explicit wait condition
from selenium.webdriver.common.by import By                       # Readable selectors
from selenium.webdriver.chrome.options import Options
import re                                                         # Regex for parsing
from timeit import default_timer as timer                         # Timer
import time                                                       # Auto-generating data
import logging                                                    # Logging
import json                                                       # Work with config file
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
# from brotli import compress
# import _cffi_backend

WEBDRIVER_SCRIPT_TIMEOUT = 300
WEBDRIVER_SCRIPT_AUTOSEND_FORM = False
BUTTON_SEND = "(//form//div[@data-shuffle-seed]//div[@role='button'])[1]"

logging.basicConfig(filename='selenium_script.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', filemode='w')


class DateException(Exception):
    """DateException is used so that generic exceptions get caught by the catch-all instead of being treated as short logs

    Args:
        Exception (_type_): _description_
    """
    pass


def read_config_file() -> dict:
    """
    Function to parse .JSON file and extract data as dict\n
    - Input - JSON file in the same folder where script is launched\n
    - Output - JSON object converted to dict
    - The frozen part is needed to correctly import config file if packed into exe
    """
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    elif __file__:
        application_path = os.path.dirname(__file__)
    with open(Path(application_path) / 'config.json', 'r') as file:
        json_obj = file.read()
    return json.loads(json_obj)


def generate_text_field_output(m: str, log_data: str) -> str:
    if log_data[m.group(0)].month in [1, 2, 3]:
        text_output = f"{log_data[m.group(0)].year}, quarter 1"
    elif log_data[m.group(0)].month in [4, 5, 6]:
        text_output = f"{log_data[m.group(0)].year}, quarter 2"
    elif log_data[m.group(0)].month in [7, 8, 9]:
        text_output = f"{log_data[m.group(0)].year}, quarter 3"
    elif log_data[m.group(0)].month in [10, 11, 12]:
        text_output = f"{log_data[m.group(0)].year}, quarter 4"
    return text_output


def compress_data_dict(data_dict: dict) -> str:
    data_dict = str(data_dict)
    return data_dict.replace("January", "01").replace("February", "02").replace("March", "03").replace("April", "04").replace("May", "05").replace("June", "06").replace("July", "07").replace("August", "08").replace("September", "09").replace("October", "10").replace("November", "11").replace("December", "12").replace("'", "").replace(" ", "").replace(",19", ",")[3:-1]


def extract_data_for_webdriver_script(log_data: dict) -> list:
    global WEBDRIVER_SCRIPT_AUTOSEND_FORM
    """
    A function to prepate selectors for webdriver as dict with questions : answers, as well as lists for questions where you need to select multiple options
    - Input - a dict with "event : year"
    - Output - a list with:
    1. dict with "selector" : "value" for google form
    2. list with OTT revolters
    """

    try:
        for key, value in log_data.items():
            parts = value.rsplit(".", 1)  # Split into date and hour
            date_part, hour_part = parts[0], parts[1]
            if hour_part == "24":
                date_obj = datetime.strptime(date_part, "%Y.%m.%d") + timedelta(days=1)
            else:
                date_obj = datetime.strptime(value, "%Y.%m.%d.%H")

            log_data[key] = date_obj   # Create datetime object as key values

        game_results = {
            "When did you play to?": log_data["END"].year if log_data["END"] < datetime.fromisoformat("1951-01-01") else "Past 1950",
            # Section with default values for some form questions - overwritten later if encountered in log
            "Did Canada intervene in the ACW?": "No",
            "When did Canada intervene in the American Civil War?": "Did not intervene",
            "Did the Entente collapse?": "No",
            "If the Entente is alive, when did it join the Weltkrieg?": "Did not join",
            "If Austria is alive, when did it join the Weltkrieg?": "Did not join",
            "Did National France land on the mainland?": "No",
            "Did Canada land on Britain?": "No",
            "Did the Netherlands go socialist?": "No",
            "Who controls most of the Indian subcontinent?": "Split between starting nations",
            "Which faction did Greece join?": "None",
            "Did Poland join the Donau-Adriabund?": "No",
            "Who won the Spanish Civil War?": "Nobody",
            "When did the Spanish Civil War end?": "Did not end",
            "Who won the Indochinese War?": "Did not happen",
            "Who won the American Civil War?": "Nobody",
            "When did the American Civil War end?": "Did not end",
            "When did the 2nd Weltkrieg end?": "Did not end",
            "Who won the Franco-German part of the 2nd Weltkrieg?": "Nobody",
            "Who won the Russo-German part of the 2nd Weltkrieg?": "Nobody",
            "Who won the Argentinian-Chilean war?": "Nobody",
            "When did the Argentinian-Chilean War end?": "Did not end",
            "Who won the Argentinian-Brazilian war?": "Did not happen",
            "Who won the Fourth Balkan War?": "Nobody",
            "When did the Fourth Balkan War end?": "Did not end",
            "When did the Levant Crisis end?": "Did not end",
            "Who unified Arabia?": "Jabal Shammar unified Arabia",
            "When did the Zhifeng War start?": "Did not happen",
            "When did the Second Sino-Japanese War start?": "Did not happen",
            "When did the Fading Sun happen?": "Did not happen",
            "When was Sichuan annexed?": "Did not happen",
            "When was Yunnan annexed?": "Did not happen",
            "When was Qing annexed?": "Did not happen",
            "When was Fengtian annexed?": "Did not happen",
            "When was Shanxi annexed?": "Did not happen",
            "Did Japan go to war with Russia?": "No",
            "Who united China?": "Nobody",
            "Who won the Xinjiang Civil War?": "Nobody",
            "When did the Xinjiang Civil War end?": "Did not end",
            "Who won the Northwestern War?": "Nobody",
            "When did the Northwestern War end?": "Did not end",
            "Who was the victor of the League War?": "Nobody",
            "When did the League War end?": "Did not end",
            "Who controls most of the Italian peninsula?": "Split between starting nations",
            "If Poland revolted, which side rebelled?": "Poland did not rebel",
            "SHX Game Progression": "default answer",
            "Who won German-Japanese war?": "Did not happen",
            "Did the GXC civil war happen?": "No",
            "When was Italy unified?": "Did not happen",
            "What path did Germany take?": "Schleicher Cabinet",
            "Has Scandinavia been formed?": "No",
            "What was the outcome of the Gateway to the Atlantic minigame?": "Ireland stayed neutral in the Gateway influence game",
            "Who won IREs far-right Balance of Power?": "The Balance of Power never happened",
            "If Ireland willingly joins a faction, what faction do they join?": "Ireland never joined a faction",
            "If Ireland gets a guarantee, who is it from?": "Ireland did not get a guarantee",
            "Did Ireland remove the Ulster Privileges?": "No",
            "What path did Russia take?": "No path was decided on",
            "Did Fengtians Unification Conference succeed?": "Did not happen"
        }
        if log_data["END"] < datetime.fromisoformat("1944-01-01"):
            raise DateException

        config_data = read_config_file()

        if config_data["role"] in ["Kaiserdev", "Dev", "Contributor"]:
            game_results["What is the highest role you have in the team?"] = config_data["role"]
        else:
            game_results["What is the highest role you have in the team?"] = "None of the above"

        if "form_autosubmit" in config_data.keys():
            if config_data.get("form_autosubmit") is True:
                WEBDRIVER_SCRIPT_AUTOSEND_FORM = True
    # raising this here so it gets caught the caller in main.py and pass to the right handler
    except DateException:
        print("Log too short (pre-1944). This may have happened because your time limit was too short, the game crashed, or something else funny happened. If you're sure it's not the first one, please report to #data-gathering")
        raise DateException
    except Exception as ex:
        logging.error(f"Error while creating initial dict before parsing the data {ex}", exc_info=True)
        raise

    try:
        # log_data_metrics = [key for key in log_data.keys() if [i for i in ["KR_tension_data", "KR_division_data", "KR_industry_data"] if i in key]]                # Metrics dict                                                                                                                       # Original dict that contains metrics
        log_data = {key: value for key, value in log_data.items() if not [i for i in ["KR_tension_data", "KR_division_data", "KR_industry_data"] if i in key]}     # Non-metrics dict
        # ACW initial answers
        ACW_participants = len([i for i in log_data.keys() if "JOINS ACW" in i]) + 1
        if ACW_participants == 2:
            game_results["If the American Civil War was a two-way, who won it?"] = "Nobody"
        elif ACW_participants == 3:
            game_results["If the American Civil War was a three-way, who won it?"] = "Nobody"
        elif "MAC GOES EAST" not in log_data.keys() and "MAC GOES WEST" not in log_data.keys():
            game_results["If MacArthur did NOT retreat, who won the ACW?"] = "Nobody"
        NFA_native_tags = ["ALG", "TUN", "SEN", "GNA", "MLI", "NGR", "CHA", "IVO", "VOL", "SIE", "MRT"]

        # EGY-OTT initial answers
        OTT_revolters = []
        NFA_revolters = []
        if "OTT FEDERALIST" not in log_data.keys() and "RUS INTERVENE AGAINST OTT" not in log_data.keys():
            game_results["If the Ottomans went Kemalist and Russia DID NOT intervene against them, who won the Levant Crisis?"] = "Nobody"
        elif "OTT FEDERALIST" not in log_data.keys() and "RUS INTERVENE AGAINST OTT" in log_data.keys():
            game_results["If the Ottomans went Kemalist and Russia DID intervene against them, who won the Levant Crisis?"] = "Nobody"
        elif "OTT FEDERALIST" in log_data.keys() and "RUS INTERVENE AGAINST OTT" not in log_data.keys():
            game_results["If the Ottomans went Federalist and Russia DID NOT intervene against them, who won the Levant Crisis?"] = "Nobody"
        elif "OTT FEDERALIST" in log_data.keys() and "RUS INTERVENE AGAINST OTT" in log_data.keys():
            game_results["If the Ottomans went Federalist and Russia DID intervene against them, who won the Levant Crisis?"] = "Nobody"

        for i in log_data.keys():
            answer = None

        # Civil Wars

            if m := re.match(r'(.*) WINS SCW', i):
                game_results["Who won the Spanish Civil War?"] = m.group(1)
                game_results["When did the Spanish Civil War end?"] = generate_text_field_output(m=m, log_data=log_data)

            elif m := re.match(r'ICW STARTS', i):
                game_results["Who won the Indochinese War?"] = "Nobody"
                game_results["When did the Indochinese civil war end?"] = "Did not end"

            elif m := re.match(r'(.*) WINS ICW', i):
                game_results["Who won the Indochinese War?"] = m.group(1)
                game_results["When did the Indochinese civil war end?"] = generate_text_field_output(m=m, log_data=log_data)

            elif m := re.match(r'MAC GOES (.*)', i):
                mac_direction = m.group(1)
                game_results[f"If MacArthur retreated {mac_direction}, who won the ACW?"] = "Nobody"

            elif m := re.match(r'(.*) WINS ACW', i):
                if 'mac_direction' not in locals():             # Check if Mac direction exists
                    mac_direction = None
                answer = m.group(1)
                game_results["Who won the American Civil War?"] = answer
                game_results["When did the American Civil War end?"] = generate_text_field_output(m=m, log_data=log_data)
                if answer and ACW_participants == 2:
                    game_results["If the American Civil War was a two-way, who won it?"] = answer
                elif answer and ACW_participants == 3:
                    game_results["If the American Civil War was a three-way, who won it?"] = answer
                elif answer and ACW_participants == 4 and mac_direction is not None:
                    game_results[f"If MacArthur retreated {mac_direction}, who won the ACW?"] = answer
                elif answer and ACW_participants == 4 and mac_direction is None:
                    game_results["If MacArthur did NOT retreat, who won the ACW?"] = answer

            elif m := re.match(r'CANADA INTERVENES IN ACW - (.*)', i):
                game_results["Did Canada intervene in the ACW?"] = m.group(1)
                game_results["When did Canada intervene in the American Civil War?"] = generate_text_field_output(m=m, log_data=log_data)

            elif m := re.match(r'3RD BOER WAR (.*)', i):
                if m.group(1) == "NAT WINS":
                    game_results["Who won the 3rd Boer War"] = "Natal"
                elif m.group(1) == "SAF WINS":
                    game_results["Who won the 3rd Boer War"] = "South Africa"
                else:
                    game_results["Who won the 3rd Boer War"] = "White peace"

        # Second Weltkrieg

            elif m := re.match(r'THE SECOND WELTKRIEG', i):
                if log_data[m.group(0)].year < 1939:
                    game_results["When did the 2nd Weltkrieg start?"] = "Before 1939"
                elif log_data[m.group(0)].year >= 1941:
                    game_results["When did the 2nd Weltkrieg start?"] = "1941 or after"
                elif log_data[m.group(0)].month in [1, 2, 3, 4]:
                    game_results["When did the 2nd Weltkrieg start?"] = f"Early {log_data[m.group(0)].year}"
                elif log_data[m.group(0)].month in [5, 6, 7, 8]:
                    game_results["When did the 2nd Weltkrieg start?"] = f"Mid {log_data[m.group(0)].year}"
                elif log_data[m.group(0)].month in [9, 10, 11, 12]:
                    game_results["When did the 2nd Weltkrieg start?"] = f"Late {log_data[m.group(0)].year}"

            elif m := re.match(r'GER FALLS', i):
                game_results["Who won the Franco-German part of the 2nd Weltkrieg?"] = "Internationale"
                game_results["If the Reichspakt lost the 2nd Weltkrieg, when did they fall?"] = generate_text_field_output(m=m, log_data=log_data)
                game_results["Who won the Russo-German part of the 2nd Weltkrieg?"] = "Russia"
                game_results["When did the 2nd Weltkrieg end?"] = generate_text_field_output(m=m, log_data=log_data)
                if "AUS ENACTED MILITARY OCCUPATION" in log_data.keys():
                    game_results["If Austria collapsed, who won the western front of the Second World War?"] = "Internationale"
                    game_results["If Austria collapsed, who won the eastern front of the Second World War?"] = "Russia"
                else:
                    game_results["If Austria did not collapse, who won the western front of the Second World War?"] = "Internationale"
                    game_results["If Austria did not collapse, who won the eastern front of the Second World War?"] = "Russia"

            elif m := re.match(r'FRA FALLS', i):
                game_results["Who won the Franco-German part of the 2nd Weltkrieg?"] = "Reichspakt"
                game_results["If the Internationale lost the 2nd Weltkrieg, when did France fall?"] = generate_text_field_output(m=m, log_data=log_data)
                game_results["When did the 2nd Weltkrieg end?"] = generate_text_field_output(m=m, log_data=log_data)
                if "AUS ENACTED MILITARY OCCUPATION" in log_data.keys():
                    game_results["If Austria collapsed, who won the western front of the Second World War?"] = "Reichspakt"
                else:
                    game_results["If Austria did not collapse, who won the western front of the Second World War?"] = "Reichspakt"

            elif m := re.match(r'RUS LOSING WKII - MOSCOW', i):
                if "GER FALLS" not in log_data.keys() and "FRA FALLS" in log_data.keys():
                    game_results["Who won the Russo-German part of the 2nd Weltkrieg?"] = "Reichspakt"
                    if "AUS ENACTED MILITARY OCCUPATION" in log_data.keys():
                        game_results["If Austria collapsed, who won the eastern front of the Second World War?"] = "Reichspakt"
                    else:
                        game_results["If Austria did not collapse, who won the eastern front of the Second World War?"] = "Reichspakt"

            elif m := re.match(r'RUS FALLS', i):
                game_results["Who won the Russo-German part of the 2nd Weltkrieg?"] = "Reichspakt"
                game_results["If Russia lost the 2nd Weltkrieg, when did they fall?"] = generate_text_field_output(m=m, log_data=log_data)
                if "AUS ENACTED MILITARY OCCUPATION" in log_data.keys():
                    game_results["If Austria collapsed, who won the eastern front of the Second World War?"] = "Reichspakt"
                else:
                    game_results["If Austria did not collapse, who won the eastern front of the Second World War?"] = "Reichspakt"

            elif m := re.match(r'ENG FALLS', i):
                if "TREATY OF LONDON" not in log_data.keys():
                    game_results["If the Internationale lost the 2nd Weltkrieg, when did Britain fall?"] = generate_text_field_output(m=m, log_data=log_data)

            elif m := re.match(r'TREATY OF LONDON', i):
                game_results["If the Internationale lost the 2nd Weltkrieg, when did Britain fall?"] = "Treaty of London"

            elif m := re.match(r'ENTENTE ENTERS 2WK', i):
                game_results["If the Entente is alive, when did it join the Weltkrieg?"] = generate_text_field_output(m=m, log_data=log_data)

            elif m := re.match(r'CAN FALLS - BY (.*)', i):
                if m.group(1) not in ["USA", "CSA", "PSA", "TEX", "NEE", "GER", "AUS", "ENG", "FRA"]:
                    answer = "Someone else"
                elif m.group(1) == "FRA" or m.group(1) == "ENG":
                    answer = "Internationale"
                elif m.group(1) == "GER" or m.group(1) == "AUS":
                    answer = "Reichspakt"
                else:
                    answer = m.group(1)
                game_results["If Canada was defeated, who caused it?"] = answer
                game_results["If Canada was defeated, when did they fall?"] = generate_text_field_output(m=m, log_data=log_data)
                game_results["Did the Entente collapse?"] = "Yes, during or after WK2" if "ENTENTE ENTERS 2WK" in log_data.keys() and log_data[m.group(0)] >= log_data["ENTENTE ENTERS 2WK"] else "Yes, before WK2"

            elif m := re.match(r'NFA FALLS - BY (.*)', i):
                if m.group(1) not in ["FRA", "EGY", "MOR", "OTT", "GER", "AUS", "FRA", "ENG", "SRI", "SWF"] and m.group(1) not in NFA_native_tags:
                    answer = "Someone else"
                elif m.group(1) == "ENG" or m.group(1) == "SRI" or m.group(1) == "SWF":
                    answer = "Internationale (not France)"
                elif m.group(1) == "GER" or m.group(1) == "AUS":
                    answer = "Reichspakt"
                elif m.group(1) == "EGY" or m.group(1) == "MOR":
                    answer = "Cairo Pact"
                elif m.group(1) in NFA_native_tags:
                    answer = "Native Rebels"
                else:
                    answer = m.group(1)
                game_results["If National France was defeated, who did it?"] = answer
                game_results["If National France was defeated, when did they fall?"] = generate_text_field_output(m=m, log_data=log_data)

            elif m := re.match(r'AUSTRIA IN 2WK', i):
                game_results["If Austria is alive, when did it join the Weltkrieg?"] = generate_text_field_output(m=m, log_data=log_data)

            elif m := re.match(r'AUSTRIA ANNEXED INTO GERMANY', i):
                game_results["If Austria is alive, when did it join the Weltkrieg?"] = "Austria annexed themselves into Germany"

            elif m := re.match(r'AUS FALLS', i):
                game_results["If Austria intervened in the Weltkrieg and lost, when did they fall?"] = generate_text_field_output(m=m, log_data=log_data)
                if "PACT IN 2WK" in log_data.keys() and log_data["AUS FALLS"] > log_data["PACT IN 2WK"]:
                    game_results["Did the Belgrade Pact win against Austria?"] = "Yes, during or after WK2"
                if "YUGOSLAVIA FORMED" in log_data.keys() and log_data["AUS FALLS"] > log_data["YUGOSLAVIA FORMED"]:
                    game_results["Did the Belgrade Pact win against Austria?"] = "Yes, before WK2"

            elif m := re.match(r'PACT IN 2WK', i):
                if "The Pact WINS 4BW" in log_data.keys():
                    game_results["If the Pact won against Bulgaria, when did they attack Austria?"] = generate_text_field_output(m=m, log_data=log_data)
                    if "AUS FALLS" not in log_data.keys():
                        game_results["Did the Belgrade Pact win against Austria?"] = "No"

            elif m := re.match(r'YUGOSLAVIA FORMED', i):
                if "AUS FALLS" not in log_data.keys():
                    game_results["Did the Belgrade Pact win against Austria?"] = "Yes, before WK2"

            elif m := re.match(r'FRANCE LANDS IN FRANCE', i):
                game_results["Did National France land on the mainland?"] = "Yes, successfully" if "FRA FALLS" in log_data.keys() else "Yes, was repelled"

            elif m := re.match(r'CANADA LANDS IN BRITAIN', i):
                game_results["Did Canada land on Britain?"] = "Yes, successfully" if "ENG FALLS" in log_data.keys() else "Yes, was repelled"

        # Regional Conflicts
            elif m := re.match(r'GER Political Path - (.*)', i):
                game_results["What path did Germany take?"] = m.group(1)

            elif m := re.match(r'GER Unpreparedness Modifier - (.*)', i):
                game_results["What was German Unpreparedness modifier when the 2nd WK started?"] = m.group(1)

            elif m := re.match(r'AUS AUSGLEICH PATH - (.*)', i):
                game_results["What path did Austria choose during Ausgleich?"] = m.group(1)

            elif m := re.match(r'(.*) UNIFIES ITALY', i):
                game_results["Who controls most of the Italian peninsula?"] = m.group(1)
                game_results["When was Italy unified?"] = generate_text_field_output(m=m, log_data=log_data)

            elif m := re.match(r'ARG POLITICAL PATH - (.*)', i):
                game_results["What path did Argentina take?"] = m.group(1)

            elif m := re.match(r'(.*) WINS ARG-CHL WAR', i):
                if 'ARGENTINA REUNIFIES IN PEACE' not in log_data.keys():
                    game_results["Who won the Argentinian-Chilean war?"] = m.group(1)
                    game_results["When did the Argentinian-Chilean War end?"] = generate_text_field_output(m=m, log_data=log_data)

            elif m := re.match(r'ARGENTINA REUNIFIES IN PEACE', i):
                game_results["Who won the Argentinian-Chilean war?"] = "Peaceful Reunification"
                game_results["When did the Argentinian-Chilean War end?"] = "Peaceful Reunification"

            elif m := re.match(r'(.*) WINS ARG-BRA WAR', i):
                game_results["Who won the Argentinian-Brazilian war?"] = m.group(1)

            elif m := re.match(r'(.*) WINS 4BW', i):
                game_results["When did the Fourth Balkan War end?"] = generate_text_field_output(m=m, log_data=log_data)
                game_results["Who won the Fourth Balkan War?"] = m.group(1)
                if m.group(1) == "The Pact" and "PACT IN 2WK" not in log_data.keys():
                    game_results["If the Pact won against Bulgaria, when did they attack Austria?"] = "Did not join"

            elif m := re.match(r'(.*) WINS IN THE LEVANT', i):
                answer = m.group(1)
                game_results["When did the Levant Crisis end?"] = generate_text_field_output(m=m, log_data=log_data)

                if "OTT FEDERALIST" in log_data.keys():
                    if "RUS INTERVENE AGAINST OTT" in log_data.keys() and log_data["RUS INTERVENE AGAINST OTT"] < log_data[m.group(0)]:
                        game_results["If the Ottomans went Federalist and Russia DID intervene against them, who won the Levant Crisis?"] = answer
                    else:
                        game_results["If the Ottomans went Federalist and Russia DID NOT intervene against them, who won the Levant Crisis?"] = answer
                else:
                    if "RUS INTERVENE AGAINST OTT" in log_data.keys() and log_data["RUS INTERVENE AGAINST OTT"] < log_data[m.group(0)]:
                        game_results["If the Ottomans went Kemalist and Russia DID intervene against them, who won the Levant Crisis?"] = answer
                    else:
                        game_results["If the Ottomans went Kemalist and Russia DID NOT intervene against them, who won the Levant Crisis?"] = answer

            elif m := re.match(r'SAUDIS UNIFY ARABIA', i):
                game_results["Who unified Arabia?"] = "Saudis unified Arabia"

            elif m := re.match(r'(.*) UNIFIES INDIA', i):
                if "INDIA IS CONQUERED BY FOREIGN POWER" not in log_data.keys():
                    game_results["Who controls most of the Indian subcontinent?"] = m.group(1)

            elif m := re.match(r'INDIA IS CONQUERED BY FOREIGN POWER', i):
                game_results["Who controls most of the Indian subcontinent?"] = "Puppeted by a foreign power"

            elif m := re.match(r'POLAND GOVERNMENT (.*)', i):
                game_results["As of 1.1.1939, what is the current ruling government of Poland?"] = m.group(1)

            elif m := re.match(r'POLAND REVOLTS - (.*)', i):
                game_results["If Poland revolted, which side rebelled?"] = m.group(1)

            elif m := re.match(r'HOL GOES SOCIALIST', i):
                game_results["Did the Netherlands go socialist?"] = "Yes"

            elif m := re.match(r'GRE ALLIANCE - (.*)', i):
                game_results["Which faction did Greece join?"] = m.group(1)

            elif m := re.match(r'POL ALLIANCE - Donau-Adriabund', i):
                game_results["Did Poland join the Donau-Adriabund?"] = "Yes"

            elif m := re.match(r'BAT POLITICAL PATH - (.*)', i):
                game_results["Which political path did the United Baltic Duchy go down?"] = m.group(1)

            elif m := re.match(r'PHI Path - (.*)', i):
                game_results["What political path did the Philippines go down in 1939?"] = m.group(1)

            elif m := re.match(r'PHI ForPol - (.*)', i):
                game_results["PHI Game Progression"] = m.group(1)

            elif m := re.match(r'FNG-QIE WAR START', i):
                game_results["When did the Zhifeng War start?"] = generate_text_field_output(m=m, log_data=log_data)

            elif m := re.match(r'JAP ICHI-GOU', i):
                if log_data[m.group(0)].year < 1938:
                    game_results["When did the Second Sino-Japanese War start?"] = "Before 1938"
                elif log_data[m.group(0)].year > 1945:
                    game_results["When did the Second Sino-Japanese War start?"] = "After 1945"
                else:
                    game_results["When did the Second Sino-Japanese War start?"] = log_data[m.group(0)].year

            elif m := re.match(r'JAPAN FADING SUN', i):
                game_results["How far did Japan push into China"] = "Pushed back (with or without the Fading Sun)"
                if log_data[m.group(0)].year < 1938:
                    game_results["When did the Fading Sun happen?"] = "Before 1938"
                elif log_data[m.group(0)].year > 1945:
                    game_results["When did the Fading Sun happen?"] = "After 1945"
                else:
                    game_results["When did the Fading Sun happen?"] = log_data[m.group(0)].year

            elif m := re.match(r'SZC FALLS', i):
                if log_data[m.group(0)].year < 1938:
                    game_results["When was Sichuan annexed?"] = "Before 1938"
                elif log_data[m.group(0)].year > 1945:
                    game_results["When was Sichuan annexed?"] = "After 1945"
                else:
                    game_results["When was Sichuan annexed?"] = log_data[m.group(0)].year

            elif m := re.match(r'YUN FALLS', i):
                if log_data[m.group(0)].year < 1938:
                    game_results["When was Yunnan annexed?"] = "Before 1938"
                elif log_data[m.group(0)].year > 1945:
                    game_results["When was Yunnan annexed?"] = "After 1945"
                else:
                    game_results["When was Yunnan annexed?"] = log_data[m.group(0)].year

            elif m := re.match(r'QIE FALLS', i):
                if log_data[m.group(0)].year < 1938:
                    game_results["When was Qing annexed?"] = "Before 1938"
                elif log_data[m.group(0)].year > 1945:
                    game_results["When was Qing annexed?"] = "After 1945"
                else:
                    game_results["When was Qing annexed?"] = log_data[m.group(0)].year

            elif m := re.match(r'FNG FALLS', i):
                if log_data[m.group(0)].year < 1938:
                    game_results["When was Fengtian annexed?"] = "Before 1938"
                elif log_data[m.group(0)].year > 1945:
                    game_results["When was Fengtian annexed?"] = "After 1945"
                else:
                    game_results["When was Fengtian annexed?"] = log_data[m.group(0)].year

            elif m := re.match(r'SHX FALLS', i):
                if log_data[m.group(0)].year < 1938:
                    game_results["When was Shanxi annexed?"] = "Before 1938"
                elif log_data[m.group(0)].year > 1945:
                    game_results["When was Shanxi annexed?"] = "After 1945"
                else:
                    game_results["When was Shanxi annexed?"] = log_data[m.group(0)].year

            elif m := re.match(r'RUS DECLARES ON [TRM|JAP]', i):
                game_results["Did Japan go to war with Russia?"] = "Started by Russia"

            elif m := re.match(r'JAP DECLARES ON RUS', i):
                game_results["Did Japan go to war with Russia?"] = "Started by Japan"

            elif m := re.match(r'TRM DECLARES ON RUS', i):
                game_results["Did Japan go to war with Russia?"] = "Started by Transamur"

            elif m := re.match(r'CHINA UNITED BY (.*)', i):
                game_results["Who united China?"] = m.group(1)

            elif m := re.match(r'JAP WAR PROGRESS - (.*)', i):
                if "JAPAN FADING SUN" in log_data.keys():
                    game_results["How far did Japan push into China"] = "Pushed back (with or without the Fading Sun)"
                elif "JAP ICHI-GOU" in log_data.keys():
                    game_results["How far did Japan push into China"] = m.group(1)

            elif m := re.match(r'(.*) WINS XINJIANG WAR', i):
                game_results["Who won the Xinjiang Civil War?"] = m.group(1)
                game_results["When did the Xinjiang Civil War end?"] = log_data[m.group(0)].year if log_data[m.group(0)] < datetime.fromisoformat("1946-01-01") else "After 1945"

            elif m := re.match(r'NORTHWESTERN WAR RESULT - (.*)', i):
                game_results["Who won the Northwestern War?"] = m.group(1)
                game_results["When did the Northwestern War end?"] = log_data[m.group(0)].year if log_data[m.group(0)] < datetime.fromisoformat("1946-01-01") else "After 1945"

            elif m := re.match(r'(.*) WINS LEP WAR', i):
                game_results["Who was the victor of the League War?"] = m.group(1)
                if "SHD INTERVENES IN LEP WAR" in log_data.keys():
                    game_results["If Shandong intervened in the League War, who won?"] = m.group(1)
                else:
                    game_results["If Shandong did not intervene in the League War, who won?"] = m.group(1)
                if log_data[m.group(0)].year < 1938:
                    if log_data[m.group(0)].month in [1, 2, 3]:
                        if log_data[m.group(0)].year == 1936 or log_data[m.group(0)].year == 1937:
                            game_results["When did the League War end?"] = f"Quarter 1, {log_data[m.group(0)].year}"
                    elif log_data[m.group(0)].month in [4, 5, 6]:
                        if log_data[m.group(0)].year == 1936 or log_data[m.group(0)].year == 1937:
                            game_results["When did the League War end?"] = f"Quarter 2, {log_data[m.group(0)].year}"
                    elif log_data[m.group(0)].month in [7, 8, 9]:
                        if log_data[m.group(0)].year == 1936 or log_data[m.group(0)].year == 1937:
                            game_results["When did the League War end?"] = f"Quarter 3, {log_data[m.group(0)].year}"
                    elif log_data[m.group(0)].month in [10, 11, 12]:
                        if log_data[m.group(0)].year == 1936 or log_data[m.group(0)].year == 1937:
                            game_results["When did the League War end?"] = f"Quarter 4, {log_data[m.group(0)].year}"
                else:
                    game_results["When did the League War end?"] = "1938 or later"

            elif m := re.match(r'FENGTIAN UNIFICATION CONFERENCE RESULT - (.*)', i):
                game_results["Did Fengtians Unification Conference succeed?"] = m.group(1)

            elif m := re.match(r'GXC CIVIL WAR WINNER - (.*)', i):
                game_results["Did the GXC civil war happen?"] = "Yes"
                game_results["Who won the GXC civil war?"] = m.group(1)
                game_results["When did the GXC civil war end?"] = generate_text_field_output(m=m, log_data=log_data)

            elif m := re.match(r'GXC CIVIL WAR AVOIDED - (.*)', i):
                game_results["Did the GXC civil war happen?"] = f"Avoided - {m.group(1)}"

            elif m := re.match(r'RUSSIA POLITICAL PATH - (.*)', i):
                game_results["What path did Russia take?"] = m.group(1)

            elif m := re.match(r'(.*) REVOLTS AGAINST OTT', i):
                OTT_revolters.append(m.group(1))

            elif m := re.match(r'(...) REVOLTS AGAINST NFA', i):
                NFA_revolters.append(m.group(1))

            elif m := re.match(r'SHX Game Progression - (.*)', i):
                game_results["SHX Game Progression"] = m.group(1)

            elif m := re.match(r'GEA-JAP WAR START', i):
                game_results["When did German-Japanese war start?"] = generate_text_field_output(m=m, log_data=log_data)
                game_results["Who won German-Japanese war?"] = "Nobody"

            elif m := re.match(r'(.*) WINS GEA-JAP WAR', i):
                game_results["Who won German-Japanese war?"] = m.group(1)
                game_results[f"If {'GEA' if m.group(1) == 'JAP' else 'JAP'} lost in GEA-JAP war, when did it fall?"] = generate_text_field_output(m=m, log_data=log_data)

            elif m := re.match(r'SCA Formed', i):
                game_results["Has Scandinavia been formed?"] = "Yes"

            elif m := re.match(r'(Ireland elects .*)', i):
                game_results["What was the outcome of IRE 1937 election?"] = m.group(1)

            elif m := re.match(r'(Blueshirts coup .*)', i):
                game_results["What was the outcome of IRE 1937 election?"] = m.group(1)

            elif m := re.match(r'Influence minigame IRE - (.*)', i):
                game_results["What was the outcome of the Gateway to the Atlantic minigame?"] = m.group(1)

            elif m := re.match(r'IRE Balance of Power - (.*)', i):
                game_results["Who won IREs far-right Balance of Power?"] = m.group(1)

            elif m := re.match(r'Ireland joins (.*)', i):
                game_results["If Ireland willingly joins a faction, what faction do they join?"] = m.group(1)

            elif m := re.match(r'(.*) guarantees Ireland', i):
                game_results["If Ireland gets a guarantee, who is it from?"] = f"{m.group(1)} guarantees Ireland"

            elif m := re.match(r'Ireland removes Ulster Privileges', i):
                game_results["Did Ireland remove the Ulster Privileges?"] = "Yes"

            elif m := re.match(r'HNN Power Struggle - (.*)', i):
                game_results["Hunan Power Struggle"] = m.group(1)

    except Exception as ex:
        logging.error(f"Error while parsing the data and preparing questions {ex}", exc_info=True)
        raise

    # tension_data = {i.split(";")[1]: round(float(i.split(";")[2]), 2) for i in log_data_metrics if "KR_tension_data" in i}
    # tension_data = {key: value if value != 1.0 else 1 for key, value in tension_data.items()}

    # industry_data = {}
    # for i in [i for i in log_data_metrics if "KR_industry_data" in i]:
    #     x = i.split(";")[1]
    #     y = i.split(";", 2)[2]
    #     if x not in industry_data.keys():
    #         industry_data[x] = [y]
    #     else:
    #         industry_data[x].append(y)

    # division_data = {}
    # for i in [i for i in log_data_metrics if "KR_division_data" in i]:
    #     x = i.split(";")[1]
    #     y = i.split(";", 2)[2]
    #     if x not in division_data.keys():
    #         division_data[x] = [y]
    #     else:
    #         division_data[x].append(y)

    # # Convert dicts to str and remove excessive symbols to speed up data sending - saves 25-50% size depending on dict type by internal compression and another 70-80% by brotli compression
    # tension_data = compress(compress_data_dict(tension_data).encode('ascii'))
    # industry_data = compress(compress_data_dict(industry_data).encode('ascii'))
    # division_data = compress(compress_data_dict(division_data).encode('ascii'))

    # return [game_results, OTT_revolters, tension_data, industry_data, division_data, NFA_revolters]
    return [game_results, OTT_revolters, NFA_revolters]


def fill_google_form(args):
    """
    This function initializes webdriver and fills google form\n
    - list - list with OTT revolters tags
    - Input - [{dict},[list]], where dict - selectors with keys, and list with OTT revolters
    - Output - selenium_script_info.log
    """
    config_data = read_config_file()
    questions_to_fill, OTT_revolters, NFA_revolters = args
    # questions_to_fill, OTT_revolters, tension_data, industry_data, division_data, NFA_revolters = args
    # logging.info(f"Currently stored questions and answers: {questions_to_fill} \nOTT revolters: {OTT_revolters}")

    try:
        start = timer()
        options = Options()
        options.add_argument("--lang=en-GB")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        driver_path = ChromeDriverManager().install()
        if driver_path:
            driver_name = driver_path.split('/')[-1]
            if driver_name != "chromedriver":
                driver_path = "/".join(driver_path.split('/')[:-1]+["chromedriver.exe"]).replace('/', '\\')
                os.chmod(driver_path, 0o755)
        browser = webdriver.Chrome(service=ChromeService(driver_path, options=options))
        # browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install(), options=options))
        browser.get(config_data["form_link"])
        WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, BUTTON_SEND)))                       # Timeout until the page is loaded
        # WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input")))

        # Fill the initial dict
        for question, answer in questions_to_fill.items():
            element_xpath_radio_button = f"//span[contains(text(), '{question}')]//ancestor::div[@jscontroller]//div[@data-value='{answer}']"
            element_xpath_input = f"//span[contains(text(), '{question}')]//ancestor::div[@jscontroller]//input"
            pseudo_xpath_for_logging = f"Selector found: div[data-params*='{question}'][data-value='{answer}']"
            if len(browser.find_elements(By.XPATH, element_xpath_radio_button)) > 0:
                logging.info(pseudo_xpath_for_logging)
                element = browser.find_element(By.XPATH, element_xpath_radio_button)
                # JS click to combat intercepted clicks exception
                WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, element_xpath_radio_button)))
                browser.execute_script("arguments[0].click();", element)
            elif len(browser.find_elements(By.XPATH, element_xpath_input)) > 0:
                logging.info(pseudo_xpath_for_logging)
                WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, element_xpath_input)))
                browser.find_element(By.XPATH, element_xpath_input).send_keys(answer)
            else:
                raise NoSuchElementException((question, answer))

        # Fill the revolters
        for revolter in OTT_revolters:
            element = browser.find_element(By.XPATH, f"//span[contains(text(), 'Which tags revolted against the Ottomans during the course of the game?')]//ancestor::div[@jscontroller]//div[@data-answer-value='{revolter}']")
            browser.execute_script("arguments[0].click();", element)
            logging.info(f"Selector found: OTT revolter {revolter}")

        for revolter in NFA_revolters:
            element = browser.find_element(By.XPATH, f"//span[contains(text(), 'What tags revolted from National France over the course of the game?')]//ancestor::div[@jscontroller]//div[@data-answer-value='{revolter}']")
            browser.execute_script("arguments[0].click();", element)
            logging.info(f"Selector found: NFA revolter {revolter}")

        # Fill text data
        # browser.find_element(By.XPATH, "//span[contains(text(), 'WT Data')]//ancestor::div[@jscontroller]//input").send_keys(str(tension_data))
        # browser.find_element(By.XPATH, "//span[contains(text(), 'Divisions Data')]//ancestor::div[@jscontroller]//input").send_keys(str(division_data))
        # browser.find_element(By.XPATH, "//span[contains(text(), 'Industry Data')]//ancestor::div[@jscontroller]//input").send_keys(str(industry_data))
        browser.find_element(By.XPATH, "//span[contains(text(), 'Who are you? Please use your discord name starting with a capital letter without the numbers')]//ancestor::div[@jscontroller]//input").send_keys(config_data["discord_nickname"])
        logging.info(f"Keys send - discord nickname - {config_data['discord_nickname']}")

        if WEBDRIVER_SCRIPT_AUTOSEND_FORM is True:
            time.sleep(1)
            browser.find_element(By.XPATH, BUTTON_SEND).click()

        end = timer()
        logging.info(f"Form is filled! It took {round(end-start, 2)} seconds")
        try:
            WebDriverWait(browser, WEBDRIVER_SCRIPT_TIMEOUT).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'Thank you!')]")))   # timeout until the script is closed
        except Exception as ex:
            print(ex)
    except Exception as ex:
        logging.error(f"Error while filling the form. Check the selectors! {ex}", exc_info=True)
        raise

    finally:
        browser.quit()


if __name__ == '__main__':
    fill_google_form(extract_data_for_webdriver_script())
