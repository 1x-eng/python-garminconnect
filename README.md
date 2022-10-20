# Python: Garmin Connect

Python 3 API wrapper for Garmin Connect to get your statistics.

## About

This package allows you to request your device, activity and health data from your Garmin Connect account.
See <https://connect.garmin.com/>

## Installation

```bash
pip3 install garminconnect
```

## API Demo Program 

Usefull for tesing all API calls
Documenting session store and loading

```python
#!/usr/bin/env python3
"""
pip3 install cloudscaper readchar requests json

export EMAIL=<your garmin email>
export PASSWORD=<your garmin password>

"""
import datetime
import json
import logging
import os
import sys

import readchar
import requests

from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
)

# Configure debug logging
# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables if defined
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")
api = None

# Example ranges
today = datetime.date.today()
startdate = today - datetime.timedelta(days=7)
start = 0
limit = 100
start_badge = 1  # badges calls start counting at 1
activitytype = ""  # Possible values are [cycling, running, swimming, multi_sport, fitness_equipment, hiking, walking, other]

menu_options = {
    "1": "Get fullname",
    "2": "Get unit system",
    "3": f"Get activity data for today '{today.isoformat()}'",
    "4": "Get activity data (to be compatible with garminconnect-ha)",
    "5": f"Get body composition data for today '{today.isoformat()}' (to be compatible with garminconnect-ha)",
    "6": f"Get body composition data for from lastweek '{startdate.isoformat()}' to today '{today.isoformat()}' (to be compatible with garminconnect-ha)",
    "7": f"Get stats and body composition data for today '{today.isoformat()}'",
    "8": f"Get steps data for today '{today.isoformat()}'",
    "9": f"Get heart rate data for today '{today.isoformat()}'",
    "a": f"Get resting heart rate data for today {today.isoformat()}'",
    "b": f"Get hydration data for today '{today.isoformat()}'",
    "c": f"Get sleep data for today '{today.isoformat()}'",
    "d": f"Get stress data for today '{today.isoformat()}'",
    "e": f"Get respiration data for today '{today.isoformat()}'",
    "f": f"Get SpO2 data for today '{today.isoformat()}'",
    "g": f"Get max metric data (like vo2MaxValue and fitnessAge) for today '{today.isoformat()}'",
    "h": "Get personal record for user",
    "i": "Get earned badges for user",
    "j": f"Get adhoc challenges data from start '{start}' and limit '{limit}'",
    "k": f"Get available badge challenges data from '{start_badge}' and limit '{limit}'",
    "l": f"Get badge challenges data from '{start_badge}' and limit '{limit}'",
    "m": f"Get non completed badge challenges data from '{start_badge}' and limit '{limit}'",
    "n": f"Download activities data from lastweek '{startdate.isoformat()}' to today '{today.isoformat()}'",
    "o": f"Get activities data from '{start}' and limit '{limit}'",
    "p": "Get Garmin device info",
    "Z": "Logout Garmin Connect portal",
    "q": "Exit",
}


def get_credentials():
    """Get user credentials."""
    email = input("Login e-mail: ")
    password = input("Password: ")

    return email, password


def init_api(email, password):
    """Initialize Garmin API with your credentials."""

    try:
        ## Try to load the previous session
        with open("session.json") as f:
            saved_session = json.load(f)

            print(
                "Login to Garmin Connect using session loaded from 'session.json'...\n"
            )

            # Use the loaded session for initializing the API (without need for credentials)
            api = Garmin(session_data=saved_session)

            # Login using the
            api.login()

    except (FileNotFoundError, GarminConnectAuthenticationError):
        # Login to Garmin Connect portal with credentials since session is invalid or not presentlastweek.
        print(
            "Session file not present or invalid, login with your credentials, please wait...\n"
        )
        try:
            api = Garmin(email, password)
            api.login()

            # Save session dictionary to json file for future use
            with open("session.json", "w", encoding="utf-8") as f:
                json.dump(api.session_data, f, ensure_ascii=False, indent=4)
        except (
            GarminConnectConnectionError,
            GarminConnectAuthenticationError,
            GarminConnectTooManyRequestsError,
            requests.exceptions.HTTPError,
        ) as err:
            logger.error("Error occurred during Garmin Connect communication: %s", err)
            return None

    return api


def print_menu():
    """Print examples menu."""
    for key in menu_options.keys():
        print(f"{key} -- {menu_options[key]}")
    print("Make your selection: ", end="", flush=True)


def switch(api, i):
    """Run selected API call."""

    # Exit example program
    if i == "q":
        print("Bye!")
        sys.exit()

    # Skip requests if login failed
    if api:
        try:
            print(f"\n\nExecuting: {menu_options[i]}\n")

            # USER BASICS
            if i == "1":
                # Get full name from profile
                logger.info(api.get_full_name())
            elif i == "2":
                ## Get unit system from profile
                logger.info(api.get_unit_system())

            # USER STATISTIC SUMMARIES
            elif i == "3":
                ## Get activity data for today 'YYYY-MM-DD'
                logger.info(api.get_stats(today.isoformat()))
            elif i == "4":
                ## Get activity data (to be compatible with garminconnect-ha)
                logger.info(api.get_user_summary(today.isoformat()))
            elif i == "5":
                ## Get body composition data for today 'YYYY-MM-DD' (to be compatible with garminconnect-ha)
                logger.info(api.get_body_composition(today.isoformat()))
            elif i == "6":
                ## Get body composition data for multiple days 'YYYY-MM-DD' (to be compatible with garminconnect-ha)
                logger.info(
                    api.get_body_composition(startdate.isoformat(), today.isoformat())
                )
            elif i == "7":
                ## Get stats and body composition data for today 'YYYY-MM-DD'
                logger.info(api.get_stats_and_body(today.isoformat()))

            # USER STATISTICS LOGGED
            elif i == "8":
                ## Get steps data for today 'YYYY-MM-DD'
                logger.info(api.get_steps_data(today.isoformat()))
            elif i == "9":
                ## Get heart rate data for today 'YYYY-MM-DD'
                logger.info(api.get_heart_rates(today.isoformat()))
            elif i == "a":
                ## Get resting heart rate data for today 'YYYY-MM-DD'
                logger.info(api.get_rhr_day(today.isoformat()))
            elif i == "b":
                ## Get hydration data 'YYYY-MM-DD'
                logger.info(api.get_hydration_data(today.isoformat()))
            elif i == "c":
                ## Get sleep data for today 'YYYY-MM-DD'
                logger.info(api.get_sleep_data(today.isoformat()))
            elif i == "d":
                ## Get stress data for today 'YYYY-MM-DD'
                logger.info(api.get_stress_data(today.isoformat()))
            elif i == "e":
                ## Get respiration data for today 'YYYY-MM-DD'
                logger.info(api.get_respiration_data(today.isoformat()))
            elif i == "f":
                ## Get SpO2 data for today 'YYYY-MM-DD'
                logger.info(api.get_spo2_data(today.isoformat()))
            elif i == "g":
                ## Get max metric data (like vo2MaxValue and fitnessAge) for today 'YYYY-MM-DD'
                logger.info(api.get_max_metrics(today.isoformat()))
            elif i == "h":
                ## Get personal record for user
                logger.info(api.get_personal_record())
            elif i == "i":
                ## Get earned badges for user
                logger.info(api.get_earned_badges())
            elif i == "j":
                ## Get adhoc challenges data from start and limit
                logger.info(
                    api.get_adhoc_challenges(start, limit)
                )  # 1=start, 100=limit
            elif i == "k":
                # Get available badge challenges data from start and limit
                logger.info(
                    api.get_available_badge_challenges(start_badge, limit)
                )  # 1=start, 100=limit
            elif i == "l":
                # Get badge challenges data from start and limit
                logger.info(
                    api.get_badge_challenges(start_badge, limit)
                )  # 1=start, 100=limit
            elif i == "m":
                # Get non completed badge challenges data from start and limit
                logger.info(
                    api.get_non_completed_badge_challenges(start_badge, limit)
                )  # 1=start, 100=limit

            # ACTIVITIES
            elif i == "m":
                # Get activities data from start and limit
                activities = api.get_activities(start, limit)  # 0=start, 1=limit
                logger.info(activities)
            elif i == "n":
                # Get activities data from startdate 'YYYY-MM-DD' to enddate 'YYYY-MM-DD', with (optional) activitytype
                # Possible values are [cycling, running, swimming, multi_sport, fitness_equipment, hiking, walking, other]
                activities = api.get_activities_by_date(
                    startdate.isoformat(), today.isoformat(), activitytype
                )

                # Get last activity
                logger.info(api.get_last_activity())

                ## Download an Activity
                for activity in activities:
                    activity_id = activity["activityId"]
                    logger.info("api.download_activities(%s)", activity_id)

                    gpx_data = api.download_activity(
                        activity_id, dl_fmt=api.ActivityDownloadFormat.GPX
                    )
                    output_file = f"./{str(activity_id)}.gpx"
                    with open(output_file, "wb") as fb:
                        fb.write(gpx_data)

                    tcx_data = api.download_activity(
                        activity_id, dl_fmt=api.ActivityDownloadFormat.TCX
                    )
                    output_file = f"./{str(activity_id)}.tcx"
                    with open(output_file, "wb") as fb:
                        fb.write(tcx_data)

                    zip_data = api.download_activity(
                        activity_id, dl_fmt=api.ActivityDownloadFormat.ORIGINAL
                    )
                    output_file = f"./{str(activity_id)}.zip"
                    with open(output_file, "wb") as fb:
                        fb.write(zip_data)

                    csv_data = api.download_activity(
                        activity_id, dl_fmt=api.ActivityDownloadFormat.CSV
                    )
                    output_file = f"./{str(activity_id)}.csv"
                    with open(output_file, "wb") as fb:
                        fb.write(csv_data)

            elif i == "o":
                # Get activities data from start and limit
                activities = api.get_activities(0, 1)  # 0=start, 1=limit

                ## Get activity splits
                first_activity_id = activities[0].get("activityId")
                owner_display_name = activities[0].get("ownerDisplayName")
                logger.info(owner_display_name)

                logger.info(api.get_activity_splits(first_activity_id))

                ## Get activity split summaries for activity id
                logger.info(api.get_activity_split_summaries(first_activity_id))

                ## Get activity weather data for activity
                logger.info(api.get_activity_weather(first_activity_id))

                ## Get activity hr timezones id
                logger.info(api.get_activity_hr_in_timezones(first_activity_id))

                ## Get activity details for activity id
                logger.info(api.get_activity_details(first_activity_id))

                # ## Get gear data for activity id
                logger.info(api.get_activity_gear(first_activity_id))

                ## Activity self evaluation data for activity id
                logger.info(api.get_activity_evaluation(first_activity_id))

            # DEVICES
            elif i == "p":
                ## Get Garmin devices
                devices = api.get_devices()
                logger.info(devices)

                ## Get device last used
                device_last_used = api.get_device_last_used()
                logger.info(device_last_used)

                for device in devices:
                    device_id = device["deviceId"]
                    logger.info(api.get_device_settings(device_id))

                ## Get device settings
                for device in devices:
                    device_id = device["deviceId"]
                    logger.info(api.get_device_settings(device_id))

            elif i == "Z":
                # Logout Garmin Connect portal
                api.logout()
                api = None

        except (
            GarminConnectConnectionError,
            GarminConnectAuthenticationError,
            GarminConnectTooManyRequestsError,
            requests.exceptions.HTTPError,
        ) as err:
            logger.error("Error occurred during Garmin Connect communication: %s", err)
        except KeyError:
            # Invalid menu option choosen
            pass
    else:
        print("Could not login to Garmin Connect, try again later.")


# Ask for credentials if not set as environment variables
if not email or not password:
    email, password = get_credentials()

# Main program loop
while True:
    # Display header and login
    print("\n*** Garmin Connect API Demo by Cyberjunky ***\n")

    # Init API
    if not api:
        api = init_api(email, password)

    # Display menu
    print_menu()

    option = readchar.readkey()
    switch(api, option)

```
