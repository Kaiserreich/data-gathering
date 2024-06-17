# Kaiserreich Automated Data Generation

## What is Automated Data Generation and Why Kaiserreich Adopted It

One of the main development activities, aside from creating new content and fixing bugs, is balancing. Kaiserreich has a huge number of country paths and regional conflicts, and to keep the state of the game healthy, these should be frequently balanced.

Earlier, the Kaiserreich team relied on people manually playing games and, after each one, manually filling out a Google form with various questions.

While this system worked for some time, the obvious drawback of such a solution is the need for people to run hundreds of games manually. HoI4 sessions require a lot of time, so the number of filled forms was bound to be limited, leading to people burning out. Another issue was that it was time-consuming to fill out forms.

To solve this issue, we created scripts to:
- Run the game automatically without the need to play the game yourself.
- Analyze logs and automatically fill out the Google form.

This allowed us to drastically increase the number of filled forms without the need to spend any time.

## Requirements

The only thing that is needed to automatically generate data is a decent PC:
- At least 4 physical CPU cores (Intel-7xxx and higher, Ryzen 3xxx and higher)
- At least 16 GB RAM
- Using notebooks is strongly NOT recommended due to cooling problems
- Windows OS

While you will still be able to run the scripts with fewer CPUs or RAM, games will take much longer. Please be mindful of computer temperatures as well.

## How to Install Data Generation Scripts

1. Using this [Dropbox link: Download Link](#):
   - Download the latest version of Logalyzer (.zip file)
   - Extract the .zip to any folder on your PC

### Data Generation Scripts

The script allows the user to launch multiple copies of HoI4 simultaneously, run them for a fixed amount of time, stop them, copy logs to storage, and start HoI4 again, all with the press of a single button. It then processes the generated .log files and automatically fills Google forms.

The archive contains the following files:
- **.exe file** - Use it to launch data generation
- **false_positives.txt file** - System file, no need to touch it
- **config.json file** - Configuration file, PLEASE EDIT IT BEFORE STARTING THE .EXE FILE
- Folders where logs are stored

### Config File Includes the Following Lines:

```json
{
  "generate_logs": true,
  "hoi4_exe_fullpath": "C:\\SteamLibrary\\steamapps\\common\\Hearts of Iron IV\\hoi4.exe",
  "crash_logging": true,
  "debug_mode": false,
  "times_to_launch": 3,
  "game_duration_minutes": 180,
  "num_of_instances": 2,
  "num_of_threads_per_exe": 4,
  "publish_to_google_form": true,
  "form_link": "URL to google form",
  "discord_nickname": "your full discord nickname",
  "role": "Kaiserdev",
  "form_autosubmit": true
}
```

- **generate_logs** - Boolean to define if the game will be launched to generate logs (true/false)
- **hoi4_exe_fullpath** - Path to hoi4.exe file (PATH SHOULD INCLUDE DOUBLE SLASHES \\)
  - Example: `"C:\\SteamLibrary\\steamapps\\common\\Hearts of Iron IV\\hoi4.exe"`
- **crash_logging** - Whether to save additional info upon crash or not (true/false)
- **debug_mode** - Whether to run games in debug mode or not (true/false)
- **times_to_launch** - How many times HoI4 copies will be launched in a loop (e.g., if set to 3, the game will start, run for the defined game duration, and stop itself 3 times)
- **game_duration_minutes** - How long each loop will take (in minutes)
- **num_of_instances** - How many HoI4 copies will run simultaneously. Set it to your number of physical cores divided by 2.
  - Example: for i7-7700k - 2, for R5-3600 - 3. Possible values: 1-8
- **num_of_threads_per_exe** - How threads will be assigned to every .exe process (leave on 4 if not sure). Possible values: 2/4
- **publish_to_google_form** - Boolean to define if the logs from “game_log_files” folders will be automatically reported to Google form (true/false)
- **form_link** - URL to Google form
- **discord_nickname** - Your full Discord nickname
- **role** - Your role in the team. Any of "Kaiserdev", "Dev", or "Contributor". If you don’t have any of those roles, set it to "None"
- **form_autosubmit** - Boolean to define if the form will be automatically submitted (true/false)

### Example

If `num_of_instances` is set to 4, `times_to_launch` set to 3, and `game_duration_minutes` set to 180:
- 4 copies of HoI4 will be launched simultaneously for 180 minutes, 3 times (the whole run will take 180 * 3 = 540 minutes)

Note: The value entered for `game_duration_minutes` will vary based on your hardware. Users will need to determine how many minutes are required to reach 1943/1944 on average with their runs. This is to ensure that wars have enough time to end. In most cases, at least 3 hours (180 minutes) will be required to reach that date. If running in debug mode, this time will need to be longer.

## TL;DR

1. Unpack the content of the zip file to any folder on your PC.
2. Open `config.json` file with any text editor.
3. Change `"hoi4_exe_fullpath"` to the path to your hoi4.exe.
4. Check how many cores/threads your PC has. If it is 4/8, change `"num_of_instances"` to 2 and leave `"num_of_threads_per_exe"` on 4. If it is 6/12, change `"num_of_instances"` to 3, and so on.
5. Change your `"discord_nickname"` and `"role"` (see guide for that).
6. Set `"times_to_launch"` to how many cycles you want to do. It will result in `times_to_launch * game_duration_minutes` minutes of running. For example, 4 * 120 = 8 hrs of running.
7. Start the `main.exe`.
8. The script will launch the game, run it, and then it will report logs to the Google form.

## Issues with the Scripts

The script generates .log files with system info. If something goes wrong, DM Pelmen#2920 and attach either the `loop_script.log` or the `selenium_script_info.log` files for issues regarding the launch script and Logalyzer, respectively.

## Hardware Safety

- Monitor your CPU temperature. If it goes > 75C, increase your fan speed.
  - A program to use could be Aida64 or the utilities that are made by motherboard manufacturers. The former is universal, the latter provides control over fans (so you can tweak your cooling immediately).
- Set the game settings to the minimum before starting log generation (1024x768 resolution, windowed, all settings to min) - no need to load GPU.
- Disable debug mode if the game runs very slowly.
  - One caveat to this would be if we find ourselves in a situation where games are crashing frequently. Having debug enabled helps generate saves to look into the issue if there was a peace conference shortly before the crash.
- Do NOT use notebooks. Do NOT run scripts if your computer cooling is bad.
