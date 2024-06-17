from random import choice, randint

import pytest

from .testClass import DataTestClass

# cd tests
# pytest -v -s --tb=line  test_data_extraction.py


def test_nobody_answers():
    tester = DataTestClass({"THE SECOND WELTKRIEG": "2:00, 21 December, 1938"},
                           {"Who won the Spanish Civil War?": "Nobody",
                            "When did the Spanish Civil War end?": "Did not end",
                            "Who won the Indochinese War?": "Nobody",
                            "When did the Indochinese civil war end?": "Did not end",
                            "Who won the American Civil War?": "Nobody",
                            "When did the American Civil War end?": "Did not end",
                            "Did Canada intervene in the ACW?": "No",
                            "When did the 2nd Weltkrieg end?": "Did not end",
                            "Who won the Franco-German part of the 2nd Weltkrieg?": "Nobody",
                            "Who won the Russo-German part of the 2nd Weltkrieg?": "Nobody",
                            "Did the Entente collapse?": "No",
                            "If the Entente is alive, when did it join the Weltkrieg?": "Did not join",
                            "If Austria is alive, when did it join the Weltkrieg?": "Did not join",
                            "Did National France land on the mainland?": "No",
                            "Did Canada land on Britain?": "No",
                            "Who won the Argentinian-Chilean war?": "Nobody",
                            "When did the Argentinian-Chilean War end?": "Did not end",
                            "Who won the Argentinian-Brazilian war?": "Did not happen",
                            "Who won the Fourth Balkan War?": "Nobody",
                            "When did the Fourth Balkan War end?": "Did not end",
                            "If the Ottomans went Kemalist and Russia DID NOT intervene against them, who won the War in the Desert?": "Nobody",
                            "Which faction did Greece join?": "None",
                            "When did the Zhifeng War start?": "Did not happen",
                            "When did the Second Sino-Japanese War start?": "Did not happen",
                            "When did the Fading Sun happen?": "Did not happen",
                            "When was Sichuan annexed?": "Did not happen",
                            "When was Yunnan annexed?": "Did not happen",
                            "When was Shanxi annexed?": "Did not happen",
                            "When was Qing annexed?": "Did not happen",
                            "When was Fengtian annexed?": "Did not happen",
                            "Did Japan go to war with Russia?": "No",
                            "Who won the Xinjiang Civil War?": "Nobody",
                            "When did the Xinjiang Civil War end?": "Did not end",
                            "Who won the Northwestern War?": "Nobody",
                            "When did the Northwestern War end?": "Did not end",
                            "Who was the victor of the League War?": "Nobody",
                            "When did the League War end?": "Did not end",
                            "Did the Netherlands go socialist?": "No",
                            "Who won the Battle for Shanxi?": "Nobody",
                            "What was SHX foreign policy towards QIE?": "Did not decide a foreign policy",
                            "Did Shanxi make it to Contender stage?": "No",})
    tester.test_correct_input()

### Civil Wars

def test_SCW_SPA():
    tester = DataTestClass({"Kingdom of Spain WINS SCW": "1:00, 1 January, 1949"},
                           {"Who won the Spanish Civil War?": "Kingdom of Spain",
                            "When did the Spanish Civil War end?": "1949, quarter 1"})
    tester.test_correct_input()


def test_SCW_SWF():
    year = str(randint(1937, 1947))
    tester = DataTestClass({"CNT-FAI WINS SCW": f"1:00, 1 January, {year}"},
                           {"Who won the Spanish Civil War?": "CNT-FAI",
                            "When did the Spanish Civil War end?": f"{year}, quarter 1"})
    tester.test_correct_input()


def test_SCW_SPR():
    year = str(randint(1937, 1947))
    tester = DataTestClass({"Carlists WINS SCW": f"11:00, 1 May, {year}"},
                           {"Who won the Spanish Civil War?": "Carlists",
                            "When did the Spanish Civil War end?": f"{year}, quarter 2"})
    tester.test_correct_input()

def test_ICW_GEA():
    year = str(randint(1937, 1947))
    tester = DataTestClass({"GEA (with or without Vietnam) WINS ICW": f"11:00, 1 May, {year}"},
                           {"Who won the Indochinese War?": "GEA (with or without Vietnam)",
                            "When did the Indochinese civil war end?": f"{year}, quarter 2"})
    tester.test_correct_input()

def test_ICW_INC():
    year = str(randint(1937, 1947))
    tester = DataTestClass({"Indochina WINS ICW": f"11:00, 1 May, {year}"},
                           {"Who won the Indochinese War?": "Indochina",
                            "When did the Indochinese civil war end?": f"{year}, quarter 2"})
    tester.test_correct_input()

def test_nobody_answers_2way_ACW():
    tester = DataTestClass({"CSA JOINS ACW": "12:00, 21 May, 1937"},
                           {"Who won the American Civil War?": "Nobody",
                            "If the American Civil War was a two-way, who won it?": "Nobody",
                            "When did the American Civil War end?": "Did not end"})
    tester.test_correct_input()

def test_nobody_answers_3way_ACW():
    tester = DataTestClass({"CSA JOINS ACW": "12:00, 21 May, 1937",
                            "TEX JOINS ACW": "12:00, 21 May, 1937"},
                           {"Who won the American Civil War?": "Nobody",
                            "If the American Civil War was a three-way, who won it?": "Nobody",
                            "When did the American Civil War end?": "Did not end"})
    tester.test_correct_input()

def test_ACW_4_side_MAC_WEST_nobody():
    tester = DataTestClass({"MAC GOES WEST": "12:00, 21 May, 1937",
                            "CSA JOINS ACW": "12:00, 21 May, 1937",
                            "PSA JOINS ACW": "12:00, 21 May, 1937",
                            "TEX JOINS ACW": "12:00, 21 May, 1937"},
                           {"If MacArthur retreated WEST, who won the ACW?": "Nobody",
                            "Who won the American Civil War?": "Nobody",
                            "When did the American Civil War end?": "Did not end"})
    tester.test_correct_input()

def test_ACW_4_side_MAC_EAST_nobody():
    tester = DataTestClass({"MAC GOES EAST": "12:00, 21 May, 1937",
                            "CSA JOINS ACW": "12:00, 21 May, 1937",
                            "PSA JOINS ACW": "12:00, 21 May, 1937",
                            "TEX JOINS ACW": "12:00, 21 May, 1937"},
                           {"If MacArthur retreated EAST, who won the ACW?": "Nobody",
                            "Who won the American Civil War?": "Nobody",
                            "When did the American Civil War end?": "Did not end"})
    tester.test_correct_input()

def test_ACW_4_side_MAC_NO_RETREAT_nobody():
    tester = DataTestClass({"CSA JOINS ACW": "12:00, 21 May, 1937",
                            "PSA JOINS ACW": "12:00, 21 May, 1937",
                            "TEX JOINS ACW": "12:00, 21 May, 1937"},
                           {"If MacArthur did NOT retreat, who won the ACW?": "Nobody",
                            "Who won the American Civil War?": "Nobody",
                            "When did the American Civil War end?": "Did not end"})
    tester.test_correct_input()

def test_ACW_2_side():
    year = str(randint(1937, 1945))
    winner = choice(["CSA", "USA", "TEX", "NEE"])
    tester = DataTestClass({"CSA JOINS ACW": "12:00, 21 May, 1937",
                            f"{winner} WINS ACW": f"11:00, 1 August, {year}"},
                           {"If the American Civil War was a two-way, who won it?": f"{winner}",
                            "When did the American Civil War end?": f"{year}, quarter 3"})
    tester.test_correct_input()

def test_ACW_3_side():
    year = str(randint(1937, 1945))
    winner = choice(["CSA", "USA", "TEX", "NEE"])
    tester = DataTestClass({"TEX JOINS ACW": "12:00, 21 May, 1937",
                            "CSA JOINS ACW": "12:00, 21 May, 1937",
                            f"{winner} WINS ACW": f"11:00, 1 August, {year}"},
                           {"If the American Civil War was a three-way, who won it?": f"{winner}",
                            "When did the American Civil War end?": f"{year}, quarter 3"})
    tester.test_correct_input()

def test_ACW_4_side_MAC_WEST():
    year = str(randint(1937, 1945))
    winner = choice(["CSA", "USA", "PSA", "TEX", "NEE"])
    tester = DataTestClass({"MAC GOES WEST": "12:00, 21 May, 1937",
                            "CSA JOINS ACW": "12:00, 21 May, 1937",
                            "PSA JOINS ACW": "12:00, 21 May, 1937",
                            "TEX JOINS ACW": "12:00, 21 May, 1937",
                            f"{winner} WINS ACW": f"11:00, 1 August, {year}"},
                           {"If MacArthur retreated WEST, who won the ACW?": f"{winner}",
                            "When did the American Civil War end?": f"{year}, quarter 3"})
    tester.test_correct_input()

def test_ACW_4_side_MAC_EAST():
    year = str(randint(1946, 1999))
    winner = choice(["CSA", "USA", "PSA", "TEX", "NEE"])
    tester = DataTestClass({"MAC GOES EAST": "12:00, 21 May, 1937",
                            "CSA JOINS ACW": "12:00, 21 May, 1937",
                            "PSA JOINS ACW": "12:00, 21 May, 1937",
                            "TEX JOINS ACW": "12:00, 21 May, 1937",
                            f"{winner} WINS ACW": f"11:00, 1 August, {year}"},
                           {"If MacArthur retreated EAST, who won the ACW?": f"{winner}",
                            "When did the American Civil War end?": f"{year}, quarter 3"})
    tester.test_correct_input()

def test_ACW_4_side_MAC_NO_RETREAT():
    year = str(randint(1937, 1945))
    winner = choice(["CSA", "USA", "PSA", "TEX", "NEE"])
    tester = DataTestClass({"CSA JOINS ACW": "12:00, 21 May, 1937",
                            "PSA JOINS ACW": "12:00, 21 May, 1937",
                            "TEX JOINS ACW": "12:00, 21 May, 1937",
                            f"{winner} WINS ACW": f"11:00, 1 August, {year}"},
                           {"If MacArthur did NOT retreat, who won the ACW?": f"{winner}",
                            "When did the American Civil War end?": f"{year}, quarter 3"})
    tester.test_correct_input()

def test_ACW_CAN_intervention_PSA():
    tester = DataTestClass({"CANADA INTERVENES IN ACW - Sided with PSA": "12:00, 21 May, 1937"},
                           {"Did Canada intervene in the ACW?": "Sided with PSA"})
    tester.test_correct_input()

def test_ACW_CAN_intervention_USA():
    tester = DataTestClass({"CANADA INTERVENES IN ACW - Sided with USA": "12:00, 21 May, 1937"},
                           {"Did Canada intervene in the ACW?": "Sided with USA"})
    tester.test_correct_input()

def test_ACW_CAN_intervention_AUS():
    tester = DataTestClass({"CANADA INTERVENES IN ACW - Sided with TEX": "12:00, 21 May, 1937"},
                           {"Did Canada intervene in the ACW?": "Sided with TEX"})
    tester.test_correct_input()

def test_ACW_CAN_intervention_NEE():
    tester = DataTestClass({"CANADA INTERVENES IN ACW - Sided with NEE": "12:00, 21 May, 1937"},
                           {"Did Canada intervene in the ACW?": "Sided with NEE"})
    tester.test_correct_input()

def test_ACW_CAN_intervention_CSA():
    tester = DataTestClass({"CANADA INTERVENES IN ACW - Attacked CSA": "12:00, 21 May, 1937"},
                           {"Did Canada intervene in the ACW?": "Attacked CSA"})
    tester.test_correct_input()

### The Second Weltkrieg

def test_2WK_start_before():
    tester = DataTestClass({"THE SECOND WELTKRIEG": "2:00, 21 December, 1938"},
                           {"When did the 2nd Weltkrieg start?": "Before 1939"})
    tester.test_correct_input()

log_lines_early_1939 = [
    "2:00, 15 March, 1939",
    "1:00, 1 January, 1939",
    "2:00, 1 March, 1939",
    "2:00, 1 March, 1939",
    "2:00, 30 March, 1939",
    "21:00, 1 February, 1939",
]

@pytest.mark.parametrize("log_line", log_lines_early_1939)
def test_2WK_start_early_1939(log_line):
    tester = DataTestClass({"THE SECOND WELTKRIEG": log_line},
                           {"When did the 2nd Weltkrieg start?": "Early 1939"})
    tester.test_correct_input()

log_lines_mid_1939 = [
    "2:00, 10 May, 1939",
    "1:00, 28 July, 1939",
    "2:00, 2 August, 1939",
    "2:00, 2 May, 1939",
    "1:00, 1 July, 1939",
    "2:00, 9 May, 1939",
    "2:00, 9 May, 1939",
    "2:00, 9 May, 1939",
]

@pytest.mark.parametrize("log_line", log_lines_mid_1939)
def test_2WK_start_mid_1939(log_line):
    tester = DataTestClass({"THE SECOND WELTKRIEG": log_line},
                           {"When did the 2nd Weltkrieg start?": "Mid 1939"})
    tester.test_correct_input()

log_lines_late_1939 = [
    "1:00, 1 November, 1939",
    "2:00, 26 September, 1939",
    "1:00, 1 December, 1939",
    "2:00, 17 October, 1939",
    "2:00, 17 October, 1939",
    "2:00, 31 October, 1939",
    "2:00, 21 November, 1939",
    "2:00, 26 September, 1939",
]

@pytest.mark.parametrize("log_line", log_lines_late_1939)
def test_2WK_start_late_1939(log_line):
    tester = DataTestClass({"THE SECOND WELTKRIEG": log_line},
                           {"When did the 2nd Weltkrieg start?": "Late 1939"})
    tester.test_correct_input()

log_lines_early_1940 = [
    "2:00, 15 March, 1940",
    "1:00, 1 January, 1940",
    "2:00, 15 March, 1940",
    "2:00, 18 April, 1940",
    "2:00, 15 March, 1940",
    "1:00, 1 January, 1940",
    "2:00, 1 March, 1940",
    "2:00, 1 March, 1940",
    "2:00, 30 March, 1940",
    "21:00, 1 February, 1940",
]

@pytest.mark.parametrize("log_line", log_lines_early_1940)
def test_2WK_start_early_1940(log_line):
    tester = DataTestClass({"THE SECOND WELTKRIEG": log_line},
                           {"When did the 2nd Weltkrieg start?": "Early 1940"})
    tester.test_correct_input()

log_lines_mid_1940 = [
    "2:00, 2 May, 1940",
    "1:00, 1 July, 1940",
    "2:00, 9 May, 1940",
    "2:00, 9 May, 1940",
    "2:00, 9 May, 1940",
    "2:00, 10 May, 1940",
    "1:00, 28 July, 1940",
    "2:00, 2 August, 1940",
    "2:00, 2 May, 1940",
]

@pytest.mark.parametrize("log_line", log_lines_mid_1940)
def test_2WK_start_mid_1940(log_line):
    tester = DataTestClass({"THE SECOND WELTKRIEG": log_line},
                           {"When did the 2nd Weltkrieg start?": "Mid 1940"})
    tester.test_correct_input()

log_lines_late_1940 = [
    "2:00, 26 September, 1940",
    "1:00, 1 December, 1940",
    "2:00, 17 October, 1940",
    "2:00, 17 October, 1940",
    "2:00, 31 October, 1940",
    "2:00, 21 November, 1940",
    "2:00, 26 September, 1940",
]

@pytest.mark.parametrize("log_line", log_lines_late_1940)
def test_2WK_start_late_1940(log_line):
    tester = DataTestClass({"THE SECOND WELTKRIEG": log_line},
                           {"When did the 2nd Weltkrieg start?": "Late 1940"})
    tester.test_correct_input()

log_lines_1941 = [
    "2:00, 15 March, 1941",
    "1:00, 1 January, 1941",
    "2:00, 31 October, 1942",
    "2:00, 21 November, 1941",
    "2:00, 26 September, 1943",
]

@pytest.mark.parametrize("log_line", log_lines_1941)
def test_2WK_start_1941(log_line):
    tester = DataTestClass({"THE SECOND WELTKRIEG": log_line},
                           {"When did the 2nd Weltkrieg start?": "1941 or after"})
    tester.test_correct_input()

def test_GER_falls_SOV():
    year = str(randint(1939, 1945))
    tester = DataTestClass({"GER FALLS": f"11:00, 1 August, {year}",
                            "SOV WINS RCW": "12:00, 21 May, 1936"},
                           {"Who won the Franco-German part of the 2nd Weltkrieg?": "Internationale",
                            "If the Reichspakt lost the 2nd Weltkrieg, when did they fall?": f"{year}, quarter 3",
                            "When did the 2nd Weltkrieg end?": f"{year}, quarter 3",
                            "Who won the Russo-German part of the 2nd Weltkrieg?": "Socialist Russia"})
    tester.test_correct_input()

def test_GER_falls_RUS():
    year = str(randint(1946, 1999))
    tester = DataTestClass({"GER FALLS": f"11:00, 1 August, {year}"},
                           {"Who won the Franco-German part of the 2nd Weltkrieg?": "Internationale",
                            "If the Reichspakt lost the 2nd Weltkrieg, when did they fall?": f"{year}, quarter 3",
                            "When did the 2nd Weltkrieg end?": f"{year}, quarter 3",
                            "Who won the Russo-German part of the 2nd Weltkrieg?": "Russia"})
    tester.test_correct_input()

def test_FRA_falls():
    year = str(randint(1939, 1945))
    tester = DataTestClass({"FRA FALLS": f"11:00, 1 August, {year}"},
                           {"Who won the Franco-German part of the 2nd Weltkrieg?": "Reichspakt",
                            "When did the 2nd Weltkrieg end?": f"{year}, quarter 3",
                            "If the Internationale lost the 2nd Weltkrieg, when did France fall?": f"{year}, quarter 3",})
    tester.test_correct_input()

def test_FRA_falls2():
    year = str(randint(1936, 1938))
    tester = DataTestClass({"FRA FALLS": f"11:00, 1 August, {year}",
                            "RUS LOSING WKII - MOSCOW": "11:00, 1 August, 1942"},
                           {"Who won the Franco-German part of the 2nd Weltkrieg?": "Reichspakt",
                            "If the Internationale lost the 2nd Weltkrieg, when did France fall?": f"{year}, quarter 3",
                            "When did the 2nd Weltkrieg end?": f"{year}, quarter 3",
                            "Who won the Russo-German part of the 2nd Weltkrieg?": "Reichspakt"})
    tester.test_correct_input()

def test_RUS_falls():
    year = str(randint(1939, 1945))
    tester = DataTestClass({"RUS FALLS": f"11:00, 1 August, {year}"},
                           {"Who won the Russo-German part of the 2nd Weltkrieg?": "Reichspakt",
                            "If Russia lost the 2nd Weltkrieg, when did they fall?": f"{year}, quarter 3"})
    tester.test_correct_input()

def test_SOV_falls():
    year = str(randint(1939, 1945))
    tester = DataTestClass({"SOV FALLS": f"11:00, 1 August, {year}"},
                           {"Who won the Russo-German part of the 2nd Weltkrieg?": "Reichspakt",
                            "If Russia lost the 2nd Weltkrieg, when did they fall?": f"{year}, quarter 3"})
    tester.test_correct_input()

def test_ENG_falls():
    year = str(randint(1939, 1945))
    tester = DataTestClass({"ENG FALLS": f"11:00, 1 August, {year}"},
                           {"If the Internationale lost the 2nd Weltkrieg, when did Britain fall?": f"{year}, quarter 3"})
    tester.test_correct_input()

def test_ENG_2PWH():
    tester = DataTestClass({"TREATY OF LONDON": "14:00, 21 December, 1939"},
                           {"If the Internationale lost the 2nd Weltkrieg, when did Britain fall?": "Treaty of London"})
    tester.test_correct_input()

def test_CAN_falls_Before_WK():
    year = str(randint(1936, 1938))
    tester = DataTestClass({"CAN FALLS - BY CSA": f"11:00, 1 August, {year}"},
                           {"If Canada was defeated, when did they fall?": f"{year}, quarter 3",
                            "If Canada was defeated, who caused it?": "CSA",
                            "Did the Entente collapse?": "Yes, before WK2"})
    tester.test_correct_input()


def test_CAN_falls_During():
    year = str(randint(1940, 1945))
    tester = DataTestClass({"CAN FALLS - BY ENG": f"11:00, 1 August, {year}",
                            "ENTENTE ENTERS 2WK": "14:00, 21 June, 1940"},
                           {"If Canada was defeated, when did they fall?": f"{year}, quarter 3",
                            "If Canada was defeated, who caused it?": "Internationale",
                            "Did the Entente collapse?": "Yes, during or after WK2"})
    tester.test_correct_input()

def test_NFA_falls_FRA():
    year = str(randint(1939, 1945))
    tester = DataTestClass({"NFA FALLS - BY FRA": f"11:00, 1 August, {year}"},
                           {"If National France was defeated, who did it?": "FRA",
                            "If National France was defeated, when did they fall?": f"{year}, quarter 3"})
    tester.test_correct_input()

def test_NFA_falls_INT():
    year = str(randint(1939, 1945))
    winner = choice(["ENG", "SRI", "SWF"])
    tester = DataTestClass({f"NFA FALLS - BY {winner}": f"11:00, 1 August, {year}"},
                           {"If National France was defeated, who did it?": "Internationale (not France)",
                            "If National France was defeated, when did they fall?": f"{year}, quarter 3"})
    tester.test_correct_input()

def test_NFA_falls_RP():
    year = str(randint(1939, 1945))
    winner = choice(["GER", "AUS"])
    tester = DataTestClass({f"NFA FALLS - BY {winner}": f"11:00, 1 August, {year}"},
                           {"If National France was defeated, who did it?": "Reichspakt",
                            "If National France was defeated, when did they fall?": f"{year}, quarter 3"})
    tester.test_correct_input()

def test_NFA_falls_cairo():
    year = str(randint(1939, 1945))
    tester = DataTestClass({"NFA FALLS - BY EGY": f"11:00, 1 August, {year}"},
                           {"If National France was defeated, who did it?": "Cairo Pact",
                            "If National France was defeated, when did they fall?": f"{year}, quarter 3"})
    tester.test_correct_input()

def test_NFA_falls_OTT():
    year = str(randint(1939, 1945))
    tester = DataTestClass({"NFA FALLS - BY OTT": f"11:00, 1 August, {year}"},
                           {"If National France was defeated, who did it?": "OTT",
                            "If National France was defeated, when did they fall?": f"{year}, quarter 3"})
    tester.test_correct_input()


def test_NFA_falls_natives():
    year = str(randint(1939, 1945))
    winner = choice(["CHA", "NGR", "VOL", "MLI", "GNA", "MRT", "TUN"])
    tester = DataTestClass({f"NFA FALLS - BY {winner}": f"11:00, 1 August, {year}"},
                           {"If National France was defeated, who did it?": "Native Rebels",
                            "If National France was defeated, when did they fall?": f"{year}, quarter 3"})
    tester.test_correct_input()


def test_NFA_falls_else():
    year = str(randint(1939, 1945))
    tester = DataTestClass({"NFA FALLS - BY IRE": f"11:00, 1 August, {year}"},
                           {"If National France was defeated, who did it?": "Someone else",
                            "If National France was defeated, when did they fall?": f"{year}, quarter 3"})
    tester.test_correct_input()

def test_AUS_in_2WK():
    year = str(randint(1939, 1945))
    tester = DataTestClass({"AUSTRIA IN 2WK": f"11:00, 1 August, {year}"},
                           {"If Austria is alive, when did it join the Weltkrieg?": f"{year}, quarter 3"})
    tester.test_correct_input()

def test_AUS_FALLS():
    year = str(randint(1939, 1945))
    tester = DataTestClass({"AUS FALLS": f"11:00, 1 August, {year}"},
                           {"If Austria intervened in the Weltkrieg and lost, when did they fall?": f"{year}, quarter 3"})
    tester.test_correct_input()

def test_PACT_WINS_AGAINST_AUS():
    tester = DataTestClass({"AUS FALLS": "14:00, 21 December, 1942",
                            "YUGOSLAVIA FORMED": "14:00, 21 June, 1940"},
                           {"Did the Belgrade Pact win against Austria?": "Yes, before WK2"})
    tester.test_correct_input()

def test_PACT_WINS_AGAINST_AUS_DURING():
    tester = DataTestClass({"PACT IN 2WK": "14:00, 21 December, 1939",
                            "AUS FALLS": "14:00, 22 December, 1939",
                            "YUGOSLAVIA FORMED": "14:00, 25 December, 1939"},
                           {"Did the Belgrade Pact win against Austria?": "Yes, during or after WK2"})
    tester.test_correct_input()

def test_PACT_in_2WK():
    year = str(randint(1939, 1945))
    tester = DataTestClass({"PACT IN 2WK": f"11:00, 1 August, {year}",
                            "The Pact WINS 4BW": "14:00, 22 December, 1938"},
                           {"If the Pact won against Bulgaria, when did they attack Austria?": f"{year}, quarter 3"})
    tester.test_correct_input()

### Regional Conflicts

def test_united_italy_SRI_on_its_own():
    tester = DataTestClass({"Socialist Republic of Italy, on its own UNIFIES ITALY": "14:00, 21 December, 1939"},
                           {"Who controls most of the Italian peninsula?": "Socialist Republic of Italy, on its own"})
    tester.test_correct_input()

def test_united_italy_SRI_with_int_help():
    tester = DataTestClass({"Socialist Republic of Italy, with INT aid UNIFIES ITALY": "14:00, 21 December, 1939"},
                           {"Who controls most of the Italian peninsula?": "Socialist Republic of Italy, with INT aid"})
    tester.test_correct_input()

def test_united_italy_SIC():
    tester = DataTestClass({"Two Sicilies UNIFIES ITALY": "14:00, 21 December, 1939"},
                           {"Who controls most of the Italian peninsula?": "Two Sicilies"})
    tester.test_correct_input()

def test_united_italy_SRD():
    tester = DataTestClass({"Sardinia UNIFIES ITALY": "14:00, 21 December, 1939"},
                           {"Who controls most of the Italian peninsula?": "Sardinia"})
    tester.test_correct_input()

def test_united_italy_ANI():
    tester = DataTestClass({"ANI Italy UNIFIES ITALY": "14:00, 21 December, 1939"},
                           {"Who controls most of the Italian peninsula?": "ANI Italy"})
    tester.test_correct_input()

def test_united_italy_ITA():
    tester = DataTestClass({"Italian Republic/Federation UNIFIES ITALY": "14:00, 21 December, 1939"},
                           {"Who controls most of the Italian peninsula?": "Italian Republic/Federation"})
    tester.test_correct_input()

def test_FOP_KILLS_ARG():
    tester = DataTestClass({"Chile WINS ARG-CHL WAR": "14:00, 21 December, 1939"},
                           {"Who won the Argentinian-Chilean war?": "Chile",
                            "When did the Argentinian-Chilean War end?": "1939, quarter 4"})
    tester.test_correct_input()

def test_ARG_KILLS_FOP():
    tester = DataTestClass({"Argentina WINS ARG-CHL WAR": "14:00, 21 December, 1939"},
                           {"Who won the Argentinian-Chilean war?": "Argentina",
                            "When did the Argentinian-Chilean War end?": "1939, quarter 4"})
    tester.test_correct_input()

def test_ARG_FOP_PEACE():
    tester = DataTestClass({"Argentina WINS ARG-CHL WAR": "14:00, 21 December, 1939",
                            "ARGENTINA REUNIFIES IN PEACE": "14:00, 21 December, 1937"},
                           {"Who won the Argentinian-Chilean war?": "Peaceful Reunification",
                            "When did the Argentinian-Chilean War end?": "Peaceful Reunification"})
    tester.test_correct_input()


def test_PACT_WINS_4BW():
    tester = DataTestClass({"The Pact WINS 4BW": "14:00, 21 December, 1939"},
                           {"Who won the Fourth Balkan War?": "The Pact",
                            "When did the Fourth Balkan War end?": "1939, quarter 4"})
    tester.test_correct_input()


def test_BUL_WINS_4BW():
    tester = DataTestClass({"Bulgaria WINS 4BW": "14:00, 21 December, 1939"},
                           {"Who won the Fourth Balkan War?": "Bulgaria",
                            "When did the Fourth Balkan War end?": "1939, quarter 4"})
    tester.test_correct_input()


def test_EGY_WINS_IN_LEVANT():
    tester = DataTestClass({"The Cairo Pact WINS IN THE LEVANT": "14:00, 21 December, 1939",
                            "OTT FEDERALIST": "12:00, 21 May, 1936"},
                           {"If the Ottomans went Federalist and Russia DID NOT intervene against them, who won the War in the Desert?": "The Cairo Pact",
                            "When did the War in the Desert end?": "1939, quarter 4"})
    tester.test_correct_input()


def test_OTT_WINS_IN_LEVANT():
    tester = DataTestClass({"The Ottoman Empire WINS IN THE LEVANT": "14:00, 21 December, 1940"},
                           {"If the Ottomans went Kemalist and Russia DID NOT intervene against them, who won the War in the Desert?": "The Ottoman Empire",
                            "When did the War in the Desert end?": "1940, quarter 4"})
    tester.test_correct_input()


def test_EGY_WINS_IN_LEVANT_RI():
    tester = DataTestClass({"The Cairo Pact WINS IN THE LEVANT": "14:00, 21 December, 1939",
                            "OTT FEDERALIST": "12:00, 21 May, 1936",
                            "AZR JOINED OTT": "14:00, 11 December, 1939",
                            "RUS INTERVENE AGAINST OTT": "14:00, 15 December, 1939"},
                           {"If the Ottomans went Federalist and Russia DID intervene against them, who won the War in the Desert?": "The Cairo Pact",
                            "Did Azerbaijan join the Ottomans against Persia?": "Yes, but OTT still lost the war",
                            "When did the War in the Desert end?": "1939, quarter 4"})
    tester.test_correct_input()


def test_OTT_WINS_IN_LEVANT_RI():
    tester = DataTestClass({"The Ottoman Empire WINS IN THE LEVANT": "14:00, 21 December, 1939",
                            "AZR JOINED OTT": "14:00, 21 December, 1939",
                            "RUS INTERVENE AGAINST OTT": "14:00, 15 December, 1939"},
                           {"If the Ottomans went Kemalist and Russia DID intervene against them, who won the War in the Desert?": "The Ottoman Empire",
                            "Did Azerbaijan join the Ottomans against Persia?": "Yes, and OTT won the war",
                            "When did the War in the Desert end?": "1939, quarter 4"})
    tester.test_correct_input()


def test_nobody_WINS_IN_LEVANT_fed():
    tester = DataTestClass({"OTT FEDERALIST": "12:00, 21 May, 1936"},
                           {"If the Ottomans went Federalist and Russia DID NOT intervene against them, who won the War in the Desert?": "Nobody"})
    tester.test_correct_input()


def test_nobody_WINS_IN_LEVANT_RI_fed():
    tester = DataTestClass({"OTT FEDERALIST": "12:00, 21 May, 1936",
                            "AZR JOINED OTT": "14:00, 11 December, 1939",
                            "RUS INTERVENE AGAINST OTT": "14:00, 15 December, 1939"},
                           {"If the Ottomans went Federalist and Russia DID intervene against them, who won the War in the Desert?": "Nobody",
                            "Did Azerbaijan join the Ottomans against Persia?": "Yes, and the war did not end"})
    tester.test_correct_input()


def test_nobody_WINS_IN_LEVANT_kemalist():
    tester = DataTestClass({"AZR JOINED OTT": "14:00, 21 December, 1939",
                            "RUS INTERVENE AGAINST OTT": "14:00, 15 December, 1939"},
                           {"If the Ottomans went Kemalist and Russia DID intervene against them, who won the War in the Desert?": "Nobody",
                            "Did Azerbaijan join the Ottomans against Persia?": "Yes, and the war did not end"})
    tester.test_correct_input()


def test_OTT_WINS_IN_LEVANT_RI_FALSE():
    tester = DataTestClass({"The Ottoman Empire WINS IN THE LEVANT": "14:00, 21 December, 1939",
                            "AZR JOINED OTT": "14:00, 21 December, 1939",
                            "RUS INTERVENE AGAINST OTT": "14:00, 21 June, 1940"},
                           {"If the Ottomans went Kemalist and Russia DID NOT intervene against them, who won the War in the Desert?": "The Ottoman Empire",
                            "Did Azerbaijan join the Ottomans against Persia?": "Yes, and OTT won the war"})
    tester.test_correct_input()


def test_INDIA_UNITED_dominion():
    tester = DataTestClass({"Dominion of India UNIFIES INDIA": "14:00, 21 December, 1939"},
                           {"Who controls most of the Indian subcontinent?": "Dominion of India"})
    tester.test_correct_input()


def test_INDIA_UNITED_federation():
    tester = DataTestClass({"Princely Federation/Hyderabad UNIFIES INDIA": "14:00, 21 December, 1939"},
                           {"Who controls most of the Indian subcontinent?": "Princely Federation/Hyderabad"})
    tester.test_correct_input()


def test_INDIA_UNITED_commune_and_not_happened_tests():
    tester = DataTestClass({"Bharatiya Commune UNIFIES INDIA": "14:00, 21 December, 1939"},
                           {"Who controls most of the Indian subcontinent?": "Bharatiya Commune",
                            "When did the Zhifeng War start?": "Did not happen",
                            "When did the Second Sino-Japanese War start?": "Did not happen",
                            "When did the Fading Sun happen?": "Did not happen",
                            "When was Sichuan annexed?": "Did not happen",
                            "When was Yunnan annexed?": "Did not happen",
                            "When was Shanxi annexed?": "Did not happen",
                            "When was Qing annexed?": "Did not happen",
                            "When was Fengtian annexed?": "Did not happen",
                            "Did Shanxi make it to Contender stage?": "No",
                            })
    tester.test_correct_input()


POL_government_list = [
    "Market Liberal",
    "Authoritarian Democrat",
    "Social Conservative",
    "Social Liberal/Social Democrat",
]


@pytest.mark.parametrize("government", POL_government_list)
def test_POL_govenment(government):
    year = str(randint(1938, 1945))
    tester = DataTestClass({f"POLAND GOVERNMENT {government}": f"14:00, 21 December, {year}"},
                           {"As of 1.1.1939, what is the current ruling government of Poland?": government})
    tester.test_correct_input()


POL_revolter_list = [
    "Nationalists",
    "Socialists",
    "Operation Parasol",
]


@pytest.mark.parametrize("government", POL_revolter_list)
def test_POL_revolter(government):
    year = str(randint(1938, 1945))
    tester = DataTestClass({f"POLAND REVOLTS - {government}": f"14:00, 21 December, {year}"},
                           {"If Poland revolted, which side rebelled?": government})
    tester.test_correct_input()


factions_list = [
    "Third Internationale",
    "Entente",
    "Reichspakt",
    "Belgrade Pact",
    "Donau-Adriabund",
    "Moscow Accord",
]


@pytest.mark.parametrize("faction", factions_list)
def test_GRE_faction(faction):
    year = str(randint(1938, 1945))
    tester = DataTestClass({f"GRE ALLIANCE - {faction}": f"14:00, 21 December, {year}"},
                           {"Which faction did Greece join?": faction})
    tester.test_correct_input()


def test_FNG_QIE_war():
    year = str(randint(1938, 1945))
    tester = DataTestClass({"FNG-QIE WAR START": f"14:00, 21 December, {year}"},
                           {"When did the Zhifeng War start?": f"{year}, quarter 4"})
    tester.test_correct_input()


def test_FNG_QIE_war_past_1945():
    tester = DataTestClass({"FNG-QIE WAR START": "14:00, 21 December, 1948"},
                           {"When did the Zhifeng War start?": "1948, quarter 4"})
    tester.test_correct_input()


def test_JAP_war_on_China():
    year = str(randint(1938, 1945))
    tester = DataTestClass({"JAP ICHI-GOU": f"14:00, 21 December, {year}"},
                           {"When did the Second Sino-Japanese War start?": year})
    tester.test_correct_input()


def test_Sichuan_capitulation():
    year = str(randint(1938, 1945))
    tester = DataTestClass({"SZC FALLS": f"14:00, 21 December, {year}"},
                           {"When was Sichuan annexed?": year})
    tester.test_correct_input()


def test_Yunnan_capitulation():
    year = str(randint(1938, 1945))
    tester = DataTestClass({"YUN FALLS": f"14:00, 21 December, {year}"},
                           {"When was Yunnan annexed?": year})
    tester.test_correct_input()


def test_QIE_capitulation():
    year = str(randint(1938, 1945))
    tester = DataTestClass({"QIE FALLS": f"14:00, 21 December, {year}"},
                           {"When was Qing annexed?": year})
    tester.test_correct_input()


def test_FNG_capitulation():
    year = str(randint(1938, 1945))
    tester = DataTestClass({"FNG FALLS": f"14:00, 21 December, {year}"},
                           {"When was Fengtian annexed?": year})
    tester.test_correct_input()


def test_SHX_capitulation():
    year = str(randint(1938, 1945))
    tester = DataTestClass({"SHX FALLS": f"14:00, 21 December, {year}"},
                           {"When was Shanxi annexed?": year})
    tester.test_correct_input()


def test_RUS_war_on_JAP():
    tester = DataTestClass({"RUS DECLARES ON JAP": "14:00, 21 December, 1939"},
                           {"Did Japan go to war with Russia?": "Started by Russia"})
    tester.test_correct_input()


def test_JAP_DECLARES_ON_RUS():
    tester = DataTestClass({"JAP DECLARES ON RUS": "14:00, 21 December, 1939"},
                           {"Did Japan go to war with Russia?": "Started by Japan"})
    tester.test_correct_input()


def test_TRM_DECLARES_ON_RUS():
    tester = DataTestClass({"TRM DECLARES ON RUS": "14:00, 21 December, 1939"},
                           {"Did Japan go to war with Russia?": "Started by Transamur"})
    tester.test_correct_input()


def test_JAP_FADING():
    tester = DataTestClass({"JAPAN FADING SUN": "14:00, 21 February, 1942"},
                           {"How far did Japan push into China": "Pushed back (with or without the Fading Sun)",
                            "When did the Fading Sun happen?": "1942"})
    tester.test_correct_input()


def test_JAP_war_progress():
    tester = DataTestClass({"JAP ICHI-GOU": "14:00, 21 December, 1939",
                            "JAP WAR PROGRESS - Conquered all of China": "14:00, 21 February, 1942"},
                           {"How far did Japan push into China": "Conquered all of China",
                            "When did the Fading Sun happen?": "Did not happen"})
    tester.test_correct_input()


def test_JAP_war_progress2():
    tester = DataTestClass({"JAP ICHI-GOU": "14:00, 21 December, 1939",
                            "JAP WAR PROGRESS - Conquered all but the interior (Sichuan, Yunnan, Shanxi)": "14:00, 21 February, 1942"},
                           {"How far did Japan push into China": "Conquered all but the interior (Sichuan, Yunnan, Shanxi)",
                            "When did the Fading Sun happen?": "Did not happen"})
    tester.test_correct_input()


def test_JAP_war_progress3():
    tester = DataTestClass({"JAP ICHI-GOU": "14:00, 21 December, 1939",
                            "JAP WAR PROGRESS - Conquered only the coastal states": "14:00, 21 February, 1942"},
                           {"How far did Japan push into China": "Conquered only the coastal states",
                            "When did the Fading Sun happen?": "Did not happen"})
    tester.test_correct_input()


def test_JAP_war_progress4():
    tester = DataTestClass({"JAP ICHI-GOU": "14:00, 21 December, 1939",
                            "JAP WAR PROGRESS - Could not push into China": "14:00, 21 February, 1942"},
                           {"How far did Japan push into China": "Could not push into China",
                            "When did the Fading Sun happen?": "Did not happen"})
    tester.test_correct_input()


CHI_tags = [
    "Federalists",
    "Left-KMT",
    "Right-KMT",
    "Sichuanese Exiles",
    "A minor clique",
    "Fengtian alone",
    "Right-KMT",
    "Zhili Qing",
    "Zhili Republic",
    "Manchu Qing",
    "Shanxi",
]
@pytest.mark.parametrize("CHI_tag", CHI_tags)
def test_CHI_unifications(CHI_tag):
    tester = DataTestClass({f"CHINA UNITED BY {CHI_tag}" : "14:00, 21 December, 1939"},
                           {"Who united China?": CHI_tag})
    tester.test_correct_input()


def test_Xinjiang_war_EST():
    tester = DataTestClass({"Republic of East Turkestan WINS XINJIANG WAR": "14:00, 21 December, 1939"},
                           {"Who won the Xinjiang Civil War?": "Republic of East Turkestan",
                            "When did the Xinjiang Civil War end?": "1939"})
    tester.test_correct_input()


def test_Xinjiang_war_KUMUL():
    tester = DataTestClass({"Kumul Khanate WINS XINJIANG WAR": "14:00, 21 December, 1939"},
                           {"Who won the Xinjiang Civil War?": "Kumul Khanate",
                            "When did the Xinjiang Civil War end?": "1939"})
    tester.test_correct_input()


def test_Xinjiang_war_SIK():
    tester = DataTestClass({"Xinjiang Clique WINS XINJIANG WAR": "14:00, 21 December, 1939"},
                           {"Who won the Xinjiang Civil War?": "Xinjiang Clique",
                            "When did the Xinjiang Civil War end?": "1939"})
    tester.test_correct_input()


def test_Northwestern_war():
    tester = DataTestClass({"MA SURVIVES NORTHWESTERN WAR": "12:00, 21 May, 1937"},
                           {"Who won the Northwestern War?": "Ma Clique",
                            "When did the Northwestern War end?": "1937"})
    tester.test_correct_input()


def test_Northwestern_war2():
    tester = DataTestClass({"MA LOSES NORTHWESTERN WAR": "12:00, 21 May, 1937", "MA SURVIVES NORTHWESTERN WAR": "12:00, 21 May, 1937"},
                           {"Who won the Northwestern War?": "Mongolia and Tibet",
                            "When did the Northwestern War end?": "1937"})
    tester.test_correct_input()


def test_LEP_war_LEP():
    tester = DataTestClass({"Nanjing Clique WINS LEP WAR": "11:00, 1 March, 1936"},
                           {"Who was the victor of the League War?": "Nanjing Clique",
                            "When did the League War end?": "Quarter 1, 1936"})
    tester.test_correct_input()


def test_LEP_war_ANQ():
    tester = DataTestClass({"Anqing Clique WINS LEP WAR": "11:00, 11 June, 1937"},
                           {"Who was the victor of the League War?": "Anqing Clique",
                            "When did the League War end?": "Quarter 2, 1937"})
    tester.test_correct_input()


def test_LEP_war_CHI():
    tester = DataTestClass({"Left Kuomintang WINS LEP WAR": "11:00, 1 August, 1939"},
                           {"Who was the victor of the League War?": "Left Kuomintang",
                            "When did the League War end?": "1938 or later"})
    tester.test_correct_input()


def test_LEP_war_SQI():
    tester = DataTestClass({"Shandong Clique WINS LEP WAR": "11:00, 1 December, 1937"},
                           {"Who was the victor of the League War?": "Shandong Clique",
                            "When did the League War end?": "Quarter 4, 1937"})
    tester.test_correct_input()


GXC_civil_war_options = [
    "Ma Ji",
    "Chen Lianbo",
    "Chen Mingshu",
    "Chen Jiongming",
    "Li Zongren",
]
@pytest.mark.parametrize("option", GXC_civil_war_options)
def test_GXC_civil_war(option):
    tester = DataTestClass({f"GXC CIVIL WAR WINNER - {option}": "11:00, 1 December, 1936",
                            "GXC CIVIL WAR START": "11:00, 1 July, 1936"},
                           {"Who won the GXC civil war?": option,
                            "When did the GXC civil war end?": "1936, quarter 4",
                            "Did the GXC civil war happen?": "Yes"})
    tester.test_correct_input()


GXC_civil_war_avoided_options = [
    "Chen Mingshu",
    "Li Zongren",
]
@pytest.mark.parametrize("option", GXC_civil_war_avoided_options)
def test_GXC_civil_war_avoided(option):
    tester = DataTestClass({f"GXC CIVIL WAR AVOIDED - {option}": "11:00, 1 December, 1936"},
                           {"Did the GXC civil war happen?": f"Avoided - {option}"})
    tester.test_correct_input()


def test_SHX_power_struggle():
    options = [
        "Yan Xishan",
        "Feng Yuxiang (balance of power)",
        "Feng Yuxiang (mission timeout)",
        "A Renewed Alliance",
        "The Manchu Coup",
    ]
    x = choice(options)
    tester = DataTestClass({f"SHX POWER STRUGGLE - {x}": "11:00, 1 December, 1937"},
                           {"Who won the Battle for Shanxi?": x})
    tester.test_correct_input()

def test_SHX_foreign_policy():
    options = [
        "Shanxi Marches On",
        "Recognize the Central Government",
    ]
    x = choice(options)
    tester = DataTestClass({f"SHX INDEPENDENCE - {x}": "11:00, 1 December, 1937"},
                           {"What was SHX foreign policy towards QIE?": x})
    tester.test_correct_input()


def test_SHX_contender():
    tester = DataTestClass({f"SHX CONTENDER - Yes": "11:00, 1 December, 1937"},
                           {"Did Shanxi make it to Contender stage?": "Yes"})
    tester.test_correct_input()

def test_JAP_GEA_war_start():
    tester = DataTestClass({f"GEA-JAP WAR START": "11:00, 1 December, 1939"},
                           {"When did German-Japanese war start?": "1939, quarter 4"})
    tester.test_correct_input()

def test_JAP_GEA_war_GEA():
    tester = DataTestClass({f"GEA-JAP WAR START": "11:00, 1 December, 1939",
                            "GEA WINS GEA-JAP WAR": "11:00, 1 December, 1944"},
                           {"When did German-Japanese war start?": "1939, quarter 4",
                            "Who won German-Japanese war?": "GEA",
                            "If JAP lost in GEA-JAP war, when did it fall?": "1944, quarter 4"})
    tester.test_correct_input()

def test_JAP_GEA_war_JAP():
    tester = DataTestClass({f"GEA-JAP WAR START": "11:00, 1 December, 1939",
                            "JAP WINS GEA-JAP WAR": "11:00, 1 December, 1944"},
                           {"When did German-Japanese war start?": "1939, quarter 4",
                            "Who won German-Japanese war?": "JAP",
                            "If GEA lost in GEA-JAP war, when did it fall?": "1944, quarter 4"})
    tester.test_correct_input()
