#!/usr/bin/env python3
"""
pip3 install garth requests readchar

export EMAIL=<your garmin email>
export PASSWORD=<your garmin password>

"""
import datetime
import json
import logging
import os
import sys
from getpass import getpass

import requests
from garth.exc import GarthHTTPError

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
tokenstore = os.getenv("GARMINTOKENS") or "~/.garminconnect"
api = None

# Example selections and settings
today = datetime.date.today()
startdate = today - datetime.timedelta(days=7)  # Select past week
start = 0
limit = 100
start_badge = 1  # Badge related calls calls start counting at 1
activitytype = ""  # Possible values are: cycling, running, swimming, multi_sport, fitness_equipment, hiking, walking, other
activityfile = "MY_ACTIVITY.fit"  # Supported file types are: .fit .gpx .tcx
weight = 69
weightunit = 'kg'

def display_json(api_call, output):
    """Format API output for better readability."""

    dashed = "-" * 20
    header = f"{dashed} {api_call} {dashed}"
    footer = "-" * len(header)

    print(header)

    if isinstance(output, (int, str, dict, list)):
        print(json.dumps(output, indent=4))
    else:
        print(output)

    print(footer)

def get_credentials():
    """Get user credentials."""

    email = input("Login e-mail: ")
    password = getpass("Enter password: ")

    return email, password


def init_api(email, password):
    """Initialize Garmin API with your credentials."""

    try:
        print(
            f"Trying to login to Garmin Connect using token data from '{tokenstore}'...\n"
        )
        garmin = Garmin()
        garmin.login(tokenstore)
    except (FileNotFoundError, GarthHTTPError, GarminConnectAuthenticationError):
        # Session is expired. You'll need to log in again
        print(
            "Login tokens not present, login with your Garmin Connect credentials to generate them.\n"
            f"They will be stored in '{tokenstore}' for future use.\n"
        )
        try:
            # Ask for credentials if not set as environment variables
            if not email or not password:
                email, password = get_credentials()

            garmin = Garmin(email, password)
            garmin.login()
            # Save tokens for next login
            garmin.garth.dump(tokenstore)

        except (FileNotFoundError, GarthHTTPError, GarminConnectAuthenticationError, requests.exceptions.HTTPError) as err:
            logger.error(err)
            return None

    return garmin

def post_health_stats_to_mem(api):
    """Post today's health stats to mem.ai"""
    try:
        today_health_stats = api.get_stats(today.isoformat())
        mem_api_key = os.getenv("MEM_API_KEY")

        if not mem_api_key:
            print("No mem.ai API key set. Unable to post today's health stats to mem.ai")
            return

        mem_url = 'https://api.mem.ai/v0/mems'
        mem_headers = {'Authorization': f'ApiAccessToken {mem_api_key}'}
        mem_payload = {
            'content': f"# {today.strftime('%d/%b/%Y')} | Health stats | Vitals\n\n"
                    "#HealthStats #Garmin\n\n"
                    "```\n"
                    f"{json.dumps(today_health_stats, indent=4)}\n"
                    "```\n"
                    "\n"
        }


        mem_response = requests.post(mem_url, headers=mem_headers, json=mem_payload)

        if mem_response.status_code == 200:
            print("==================================================")
            print("Posted today's health stats to mem.ai successfully")
            print("==================================================\n")
            
            display_json(
                f"Today's health stats: (using api call = api.get_stats('{today.isoformat()}'))",
                today_health_stats,
            )
        else:
            print(f"Failed to post today's health stats to mem.ai. Status code: {mem_response.status_code}, Response: {mem_response.text}")

    except requests.RequestException as e:
        print(f"An error occurred while posting to mem.ai: {e}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

api = init_api(email, password)
post_health_stats_to_mem(api)