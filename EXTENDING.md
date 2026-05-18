# Extending the Data Gatherer

## How to Add New Logging

Reference guide to addd new questions for data gathering

### 1. Add the Log Entry in Your Event/Decision/On_action etc

In your Kaiserreich event file, use the KR_Event_Logging callback:

```
log = "KR_Event_Logging;NORTHWESTERN WAR RESULT - Tibet (Mongolia lost to XSM)"
```

Format: `KR_Event_Logging;<EVENT_NAME> [optional info]`

The game automatically appends the timestamp, so the resulting log line will be:
```
[10:37:49][1936.05.26.02][effectbase.cpp:1781]: KR_Event_Logging;NORTHWESTERN WAR RESULT - Tibet (Mongolia lost to XSM)
```

### 2. Add Default Answer to game_results Dictionary

Open `webdriver_form_filler.py` and locate the `game_results` dictionary (around line 91).

Add your question with a sensible default:

```python
game_results = {
    # ... existing entries ...
    "Who won the Northwestern War?": "Nobody",
    "When did the Northwestern War end?": "Did not end",
}
```

If the event never occurs in a playthrough, these defaults are submitted.

### 3. Add Parsing Logic

In the same file, find the main parsing loop (around line 172). Add your event pattern using regex:

```python
elif m := re.match(r'NORTHWESTERN WAR RESULT - (.*)', i):
    game_results["Who won the Northwestern War?"] = m.group(1)
    game_results["When did the Northwestern War end?"] = generate_text_field_output(m=m, log_data=log_data)
```

## Regex Patterns

### Simple Match (Fixed Text)

```python
elif m := re.match(r'FRANCE GOES MONARCHIST', i):
    game_results["Did France restore the monarchy?"] = "Yes"
```

Matches: `FRANCE GOES MONARCHIST`

### Capture Dynamic Text

```python
elif m := re.match(r'NORTHWESTERN WAR RESULT - (.*)', i):
    answer = m.group(1)
    game_results["Who won the Northwestern War?"] = answer
```

Matches: `NORTHWESTERN WAR RESULT - Tibet (Mongolia lost to XSM)`
- `m.group(1)` extracts: `Tibet (Mongolia lost to XSM)`

### Capture with Alternatives

```python
elif m := re.match(r'(USA|GER|RUS) JOINS WAR', i):
    game_results["Who joined the war?"] = m.group(1)
```

### Extract Timestamp

Use `log_data[m.group(0)]` to get the datetime object:

```python
game_results["When?"] = generate_text_field_output(m=m, log_data=log_data)
```

This formats the date as `YYYY, quarter Q` (e.g., `1940, quarter 2`).

## Conditional Logic

Check if other events occurred before deciding what to submit:

```python
elif m := re.match(r'(.*) WINS WAR', i):
    if 'ENEMY SURRENDERED' in log_data.keys():
        game_results["How did war end?"] = "Surrender"
    else:
        game_results["How did war end?"] = "Military victory"
```

## Testing Your Changes

1. Add test log line to a game log file
2. Run `python main.py` with `"generate_logs": false` in config.json
3. Check `selenium_script.log` for parsing errors
4. Verify the form submission contains your expected answer

## Common Patterns in Codebase

**Multiple capture groups:**
```python
elif m := re.match(r'(.*) WINS (.*) WAR', i):
    winner = m.group(1)
    war_type = m.group(2)
```

**Conditional with date comparison:**
```python
elif m := re.match(r'EVENT', i):
    if log_data['OTHER_EVENT'] < log_data[m.group(0)]:
        game_results["question"] = "yes"
```

**Flag variables for later use:**
```python
wk2_start_date = False
# ...
elif m := re.match(r'THE SECOND WELTKRIEG', i):
    wk2_start_date = log_data[m.group(0)]
```

Then reference later:
```python
if wk2_start_date and other_condition:
    game_results["question"] = "answer"
```
