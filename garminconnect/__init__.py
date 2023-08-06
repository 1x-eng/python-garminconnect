# -*- coding: utf-8 -*-

"""Python 3 API wrapper for Garmin Connect to get your statistics."""

import logging
import os
from enum import Enum, auto
from typing import Any, Dict, List, Optional

import garth


logger = logging.getLogger(__name__)


class Garmin:
    """Class for fetching data from Garmin Connect."""

    def __init__(self, email=None, password=None, is_cn=False):
        """Create a new class instance."""
        self.username = email
        self.password = password
        self.is_cn = is_cn

        self.garmin_connect_base_url = "https://connect.garmin.com"
        self.garmin_connect_sso_url = "sso.garmin.com/sso"
        self.garmin_connect_modern_url = "connect.garmin.com/modern"
        self.garmin_connect_css_url = "https://static.garmincdn.com/com.garmin.connect/ui/css/gauth-custom-v1.2-min.css"
        self.garmin_connect_login_url = self.garmin_connect_base_url + "/en-US/signin"

        if self.is_cn:
            self.garmin_connect_base_url = "https://connect.garmin.cn"
            self.garmin_connect_sso_url = "sso.garmin.cn/sso"
            self.garmin_connect_modern_url = "connect.garmin.cn/modern"
            self.garmin_connect_css_url = "https://static.garmincdn.cn/cn.garmin.connect/ui/css/gauth-custom-v1.2-min.css"
            self.garmin_connect_login_url = self.garmin_connect_base_url + "/zh-CN/signin"

        self.garmin_connect_sso_login = "signin"

        self.garmin_connect_devices_url = (
            "proxy/device-service/deviceregistration/devices"
        )
        self.garmin_connect_device_url = "proxy/device-service/deviceservice"
        self.garmin_connect_weight_url = "proxy/weight-service/weight/dateRange"
        self.garmin_connect_daily_summary_url = (
            "proxy/usersummary-service/usersummary/daily"
        )
        self.garmin_connect_metrics_url = "proxy/metrics-service/metrics/maxmet/daily"
        self.garmin_connect_daily_hydration_url = (
            "proxy/usersummary-service/usersummary/hydration/daily"
        )
        self.garmin_connect_daily_stats_steps_url = (
            "proxy/usersummary-service/stats/steps/daily"
        )
        self.garmin_connect_personal_record_url = (
            "proxy/personalrecord-service/personalrecord/prs"
        )
        self.garmin_connect_earned_badges_url = "proxy/badge-service/badge/earned"
        self.garmin_connect_adhoc_challenges_url = (
            "proxy/adhocchallenge-service/adHocChallenge/historical"
        )
        self.garmin_connect_badge_challenges_url = (
            "proxy/badgechallenge-service/badgeChallenge/completed"
        )
        self.garmin_connect_available_badge_challenges_url = (
            "proxy/badgechallenge-service/badgeChallenge/available"
        )
        self.garmin_connect_non_completed_badge_challenges_url = (
            "proxy/badgechallenge-service/badgeChallenge/non-completed"
        )
        self.garmin_connect_daily_sleep_url = (
            "proxy/wellness-service/wellness/dailySleepData"
        )
        self.garmin_connect_daily_stress_url = (
            "proxy/wellness-service/wellness/dailyStress"
        )

        self.garmin_connect_daily_body_battery_url = (
            "proxy/wellness-service/wellness/bodyBattery/reports/daily"
        )

        self.garmin_connect_blood_pressure_endpoint = (
            "proxy/bloodpressure-service/bloodpressure/range"
        )

        self.garmin_connect_goals_url = "proxy/goal-service/goal/goals"

        self.garmin_connect_rhr_url = "proxy/userstats-service/wellness/daily"

        self.garmin_connect_hrv_url = "proxy/hrv-service/hrv"

        self.garmin_connect_training_readiness_url = "proxy/metrics-service/metrics/trainingreadiness"

        self.garmin_connect_training_status_url = "proxy/metrics-service/metrics/trainingstatus/aggregated"

        self.garmin_connect_user_summary_chart = (
            "proxy/wellness-service/wellness/dailySummaryChart"
        )
        self.garmin_connect_floors_chart_daily_url = (
            "proxy/wellness-service/wellness/floorsChartData/daily"
        )
        self.garmin_connect_heartrates_daily_url = (
            "proxy/wellness-service/wellness/dailyHeartRate"
        )
        self.garmin_connect_daily_respiration_url = (
            "proxy/wellness-service/wellness/daily/respiration"
        )
        self.garmin_connect_daily_spo2_url = (
            "proxy/wellness-service/wellness/daily/spo2"
        )
        self.garmin_connect_activities = (
            "proxy/activitylist-service/activities/search/activities"
        )
        self.garmin_connect_activity = "proxy/activity-service/activity"
        self.garmin_connect_activity_types = "proxy/activity-service/activity/activityTypes"

        self.garmin_connect_fitnessstats = "proxy/fitnessstats-service/activity"

        self.garmin_connect_fit_download = "proxy/download-service/files/activity"
        self.garmin_connect_tcx_download = "proxy/download-service/export/tcx/activity"
        self.garmin_connect_gpx_download = "proxy/download-service/export/gpx/activity"
        self.garmin_connect_kml_download = "proxy/download-service/export/kml/activity"
        self.garmin_connect_csv_download = "proxy/download-service/export/csv/activity"

        self.garmin_connect_upload = "proxy/upload-service/upload"

        self.garmin_connect_gear = "proxy/gear-service/gear/filterGear"
        self.garmin_connect_gear_baseurl = "proxy/gear-service/gear/"

        self.garmin_connect_logout = "auth/logout/?url="

        self.garmin_headers = {"NK": "NT"}

        self.garth = garth.Client(domain="garmin.cn" if is_cn else "garmin.com")

        self.display_name = None
        self.full_name = None
        self.unit_system = None

    def connectapi(self, url, **kwargs):
        path = url.lstrip("proxy")
        return self.garth.connectapi(path, **kwargs)

    def login(self, /, garth_home: Optional[str]=None):
        """Log in using Garth"""
        garth_home = garth_home or os.getenv("GARTH_HOME")

        if garth_home:
            self.garth.load(garth_home)
        else:
            self.garth.login(self.username, self.password)
        
        profile = self.garth.connectapi("/userprofile-service/socialProfile")
        self.display_name = profile["displayName"]
        self.full_name = profile["fullName"]

        settings = self.garth.connectapi(
            "/userprofile-service/userprofile/user-settings"
        )
        self.unit_system = settings['userData']['measurementSystem']
        
        return True

    def get_full_name(self):
        """Return full name."""

        return self.full_name

    def get_unit_system(self):
        """Return unit system."""

        return self.unit_system

    def get_stats(self, cdate: str) -> Dict[str, Any]:
        """Return user activity summary for 'cdate' format 'YYYY-MM-DD' (compat for garminconnect)."""

        return self.get_user_summary(cdate)

    def get_user_summary(self, cdate: str) -> Dict[str, Any]:
        """Return user activity summary for 'cdate' format 'YYYY-MM-DD'."""

        url = f"{self.garmin_connect_daily_summary_url}/{self.display_name}"
        params = {
            "calendarDate": str(cdate)
        }
        logger.debug("Requesting user summary")

        response = self.connectapi(url, params=params)

        if response["privacyProtected"] is True:
            raise GarminConnectAuthenticationError("Authentication error")

        return response

    def get_steps_data(self, cdate):
        """Fetch available steps data 'cDate' format 'YYYY-MM-DD'."""

        url = f"{self.garmin_connect_user_summary_chart}/{self.display_name}"
        params = {
            "date": str(cdate)
        }
        logger.debug("Requesting steps data")

        return self.connectapi(url, params=params)

    def get_floors(self, cdate):
        """Fetch available floors data 'cDate' format 'YYYY-MM-DD'."""

        url = f'{self.garmin_connect_floors_chart_daily_url}/{cdate}'
        logger.debug("Requesting floors data")

        return self.connectapi(url)

    def get_daily_steps(self, start, end):
        """Fetch available steps data 'start' and 'end' format 'YYYY-MM-DD'."""

        url = f'{self.garmin_connect_daily_stats_steps_url}/{start}/{end}'
        logger.debug("Requesting daily steps data")

        return self.connectapi(url)

    def get_heart_rates(self, cdate):
        """Fetch available heart rates data 'cDate' format 'YYYY-MM-DD'."""

        url = f"{self.garmin_connect_heartrates_daily_url}/{self.display_name}"
        params = {
            "date": str(cdate)
        }
        logger.debug("Requesting heart rates")

        return self.connectapi(url, params=params)

    def get_stats_and_body(self, cdate):
        """Return activity data and body composition (compat for garminconnect)."""

        return {
            **self.get_stats(cdate),
            **self.get_body_composition(cdate)["totalAverage"],
        }

    def get_body_composition(self, startdate: str, enddate=None) -> Dict[str, Any]:
        """Return available body composition data for 'startdate' format 'YYYY-MM-DD' through enddate 'YYYY-MM-DD'."""

        if enddate is None:
            enddate = startdate
        url = self.garmin_connect_weight_url
        params = {"startDate": str(startdate), "endDate": str(enddate)}
        logger.debug("Requesting body composition")

        return self.connectapi(url, params=params)

    def get_body_battery(self, startdate: str, enddate=None) -> List[Dict[str, Any]]:
        """Return body battery values by day for 'startdate' format 'YYYY-MM-DD' through enddate 'YYYY-MM-DD'"""

        if enddate is None:
            enddate = startdate
        url = self.garmin_connect_daily_body_battery_url
        params = {"startDate": str(startdate), "endDate": str(enddate)}
        logger.debug("Requesting body battery data")

        return self.connectapi(url, params=params)

    def get_blood_pressure(self, startdate: str, enddate=None) -> Dict[str, Any]:
        """Returns blood pressure by day for 'startdate' format 'YYYY-MM-DD' through enddate 'YYYY-MM-DD'"""

        if enddate is None:
            enddate = startdate
        url = f"{self.garmin_connect_blood_pressure_endpoint}/{startdate}/{enddate}"
        params = {"includeAll": True}
        logger.debug("Requesting blood pressure data")

        return self.connectapi(url, params=params)

    def get_max_metrics(self, cdate: str) -> Dict[str, Any]:
        """Return available max metric data for 'cdate' format 'YYYY-MM-DD'."""

        url = f"{self.garmin_connect_metrics_url}/{cdate}/{cdate}"
        logger.debug("Requesting max metrics")

        return self.connectapi(url)

    def get_hydration_data(self, cdate: str) -> Dict[str, Any]:
        """Return available hydration data 'cdate' format 'YYYY-MM-DD'."""

        url = f"{self.garmin_connect_daily_hydration_url}/{cdate}"
        logger.debug("Requesting hydration data")

        return self.connectapi(url)

    def get_respiration_data(self, cdate: str) -> Dict[str, Any]:
        """Return available respiration data 'cdate' format 'YYYY-MM-DD'."""

        url = f"{self.garmin_connect_daily_respiration_url}/{cdate}"
        logger.debug("Requesting respiration data")

        return self.connectapi(url)

    def get_spo2_data(self, cdate: str) -> Dict[str, Any]:
        """Return available SpO2 data 'cdate' format 'YYYY-MM-DD'."""

        url = f"{self.garmin_connect_daily_spo2_url}/{cdate}"
        logger.debug("Requesting SpO2 data")

        return self.connectapi(url)

    def get_personal_record(self) -> Dict[str, Any]:
        """Return personal records for current user."""

        url = f"{self.garmin_connect_personal_record_url}/{self.display_name}"
        logger.debug("Requesting personal records for user")

        return self.connectapi(url)

    def get_earned_badges(self) -> Dict[str, Any]:
        """Return earned badges for current user."""

        url = self.garmin_connect_earned_badges_url
        logger.debug("Requesting earned badges for user")

        return self.connectapi(url)

    def get_adhoc_challenges(self, start, limit) -> Dict[str, Any]:
        """Return adhoc challenges for current user."""

        url = self.garmin_connect_adhoc_challenges_url
        params = {"start": str(start), "limit": str(limit)}
        logger.debug("Requesting adhoc challenges for user")

        return self.connectapi(url, params=params)

    def get_badge_challenges(self, start, limit) -> Dict[str, Any]:
        """Return badge challenges for current user."""

        url = self.garmin_connect_badge_challenges_url
        params = {"start": str(start), "limit": str(limit)}
        logger.debug("Requesting badge challenges for user")

        return self.connectapi(url, params=params)

    def get_available_badge_challenges(self, start, limit) -> Dict[str, Any]:
        """Return available badge challenges."""

        url = self.garmin_connect_available_badge_challenges_url
        params = {"start": str(start), "limit": str(limit)}
        logger.debug("Requesting available badge challenges")

        return self.connectapi(url, params=params)

    def get_non_completed_badge_challenges(self, start, limit) -> Dict[str, Any]:
        """Return badge non-completed challenges for current user."""

        url = self.garmin_connect_non_completed_badge_challenges_url
        params = {"start": str(start), "limit": str(limit)}
        logger.debug("Requesting badge challenges for user")

        return self.connectapi(url, params=params)

    def get_sleep_data(self, cdate: str) -> Dict[str, Any]:
        """Return sleep data for current user."""

        url = f"{self.garmin_connect_daily_sleep_url}/{self.display_name}"
        params = {"date": str(cdate), "nonSleepBufferMinutes": 60}
        logger.debug("Requesting sleep data")

        return self.connectapi(url, params=params)

    def get_stress_data(self, cdate: str) -> Dict[str, Any]:
        """Return stress data for current user."""

        url = f"{self.garmin_connect_daily_stress_url}/{cdate}"
        logger.debug("Requesting stress data")

        return self.connectapi(url)

    def get_rhr_day(self, cdate: str) -> Dict[str, Any]:
        """Return resting heartrate data for current user."""

        url = f"{self.garmin_connect_rhr_url}/{self.display_name}"
        params = {"fromDate": str(cdate), "untilDate": str(cdate), "metricId": 60}
        logger.debug("Requesting resting heartrate data")

        return self.connectapi(url, params=params)

    def get_hrv_data(self, cdate: str) -> Dict[str, Any]:
        """Return Heart Rate Variability (hrv) data for current user."""

        url = f"{self.garmin_connect_hrv_url}/{cdate}"
        logger.debug("Requesting Heart Rate Variability (hrv) data")

        return self.connectapi(url)

    def get_training_readiness(self, cdate: str) -> Dict[str, Any]:
        """Return training readiness data for current user."""

        url = f"{self.garmin_connect_training_readiness_url}/{cdate}"
        logger.debug("Requesting training readiness data")

        return self.connectapi(url)

    def get_training_status(self, cdate: str) -> Dict[str, Any]:
        """Return training status data for current user."""

        url = f"{self.garmin_connect_training_status_url}/{cdate}"
        logger.debug("Requesting training status data")

        return self.connectapi(url)

    def get_devices(self) -> Dict[str, Any]:
        """Return available devices for the current user account."""

        url = self.garmin_connect_devices_url
        logger.debug("Requesting devices")

        return self.connectapi(url)

    def get_device_settings(self, device_id: str) -> Dict[str, Any]:
        """Return device settings for device with 'device_id'."""

        url = f"{self.garmin_connect_device_url}/device-info/settings/{device_id}"
        logger.debug("Requesting device settings")

        return self.connectapi(url)

    def get_device_alarms(self) -> Dict[str, Any]:
        """Get list of active alarms from all devices."""

        logger.debug("Requesting device alarms")

        alarms = []
        devices = self.get_devices()
        for device in devices:
            device_settings = self.get_device_settings(device["deviceId"])
            device_alarms = device_settings["alarms"]
            if device_alarms is not None:
                alarms += device_alarms
        return alarms

    def get_device_last_used(self):
        """Return device last used."""

        url = f"{self.garmin_connect_device_url}/mylastused"
        logger.debug("Requesting device last used")

        return self.connectapi(url)

    def get_activities(self, start, limit):
        """Return available activities."""

        url = self.garmin_connect_activities
        params = {"start": str(start), "limit": str(limit)}
        logger.debug("Requesting activities")

        return self.connectapi(url, params=params)

    def get_last_activity(self):
        """Return last activity."""

        activities = self.get_activities(0, 1)
        if activities:
            return activities[-1]

        return None

    def upload_activity(self, activity_path: str):
        """Upload activity in fit format from file."""
        # This code is borrowed from python-garminconnect-enhanced ;-)

        file_base_name = os.path.basename(activity_path)
        file_extension = file_base_name.split(".")[-1]
        allowed_file_extension = file_extension.upper() in Garmin.ActivityUploadFormat.__members__

        if allowed_file_extension:
            files = {
                "file": (file_base_name, open(activity_path, "rb" or "r")),
            }
            url = self.garmin_connect_upload
            return self.modern_rest_client.post(url, files=files)
        else:
            raise GarminConnectInvalidFileFormatError(f"Could not upload {activity_path}")

    def get_activities_by_date(self, startdate, enddate, activitytype=None):
        """
        Fetch available activities between specific dates
        :param startdate: String in the format YYYY-MM-DD
        :param enddate: String in the format YYYY-MM-DD
        :param activitytype: (Optional) Type of activity you are searching
                             Possible values are [cycling, running, swimming,
                             multi_sport, fitness_equipment, hiking, walking, other]
        :return: list of JSON activities
        """

        activities = []
        start = 0
        limit = 20
        # mimicking the behavior of the web interface that fetches 20 activities at a time
        # and automatically loads more on scroll
        url = self.garmin_connect_activities
        params = {
            "startDate": str(startdate),
            "endDate": str(enddate),
            "start": str(start),
            "limit": str(limit),
        }
        if activitytype:
            params["activityType"] = str(activitytype)

        logger.debug(f"Requesting activities by date from {startdate} to {enddate}")
        while True:
            params["start"] = str(start)
            logger.debug(f"Requesting activities {start} to {start+limit}")
            act = self.connectapi(url, params=params)
            if act:
                activities.extend(act)
                start = start + limit
            else:
                break

        return activities

    def get_progress_summary_between_dates(self, startdate, enddate, metric="distance"):
        """
        Fetch progress summary data between specific dates
        :param startdate: String in the format YYYY-MM-DD
        :param enddate: String in the format YYYY-MM-DD
        :param metric: metric to be calculated in the summary:
            "elevationGain", "duration", "distance", "movingDuration"
        :return: list of JSON activities with their aggregated progress summary
        """

        url = self.garmin_connect_fitnessstats
        params = {
            "startDate": str(startdate),
            "endDate": str(enddate),
            "aggregation": "lifetime",
            "groupByParentActivityType": "true",
            "metric": str(metric)
            
        }

        logger.debug(
            f"Requesting fitnessstats by date from {startdate} to {enddate}")
        return self.connectapi(url, params=params)

    def get_activity_types(self):
        url = self.garmin_connect_activity_types
        logger.debug(f"Requesting activy types")
        return self.connectapi(url)

    def get_goals(self, status="active", start=1, limit=30):
        """
        Fetch all goals based on status
        :param status: Status of goals (valid options are "active", "future", or "past")
        :type status: str
        :param start: Initial goal index
        :type start: int
        :param limit: Pagination limit when retrieving goals
        :type limit: int
        :return: list of goals in JSON format
        """

        goals = []
        url = self.garmin_connect_goals_url
        params = {
            "status": status,
            "start": str(start),
            "limit": str(limit),
            "sortOrder": "asc"
        }

        logger.debug(f"Requesting {status} goals")
        while True:
            params["start"] = str(start)
            logger.debug(f"Requesting {status} goals {start} to {start + limit - 1}")
            goals_json = self.connectapi(url, params=params)
            if goals_json:
                goals.extend(goals_json)
                start = start + limit
            else:
                break

        return goals

    def get_gear(self, userProfileNumber):
        """Return all user gear."""
        url = f"{self.garmin_connect_gear}?userProfilePk={userProfileNumber}"
        logger.debug("Requesting gear for user %s", userProfileNumber)

        return self.connectapi(url)

    def get_gear_stats(self, gearUUID):
        url = f"{self.garmin_connect_gear_baseurl}stats/{gearUUID}"
        logger.debug("Requesting gear stats for gearUUID %s", gearUUID)
        return self.connectapi(url)

    def get_gear_defaults(self, userProfileNumber):
        url = f"{self.garmin_connect_gear_baseurl}user/{userProfileNumber}/activityTypes"
        logger.debug("Requesting gear for user %s", userProfileNumber)
        return self.connectapi(url)

    def set_gear_default(self, activityType, gearUUID, defaultGear=True):
        defaultGearString = "/default/true" if defaultGear else ""
        method_override = "PUT" if defaultGear else "DELETE"
        url = f"{self.garmin_connect_gear_baseurl}{gearUUID}/activityType/{activityType}{defaultGearString}"
        return self.modern_rest_client.post(
            url, {"x-http-method-override": method_override}
        )

    class ActivityDownloadFormat(Enum):
        """Activity variables."""

        ORIGINAL = auto()
        TCX = auto()
        GPX = auto()
        KML = auto()
        CSV = auto()

    class ActivityUploadFormat(Enum):
        FIT = auto()
        GPX = auto()
        TCX = auto()

    def download_activity(self, activity_id, dl_fmt=ActivityDownloadFormat.TCX):
        """
        Downloads activity in requested format and returns the raw bytes. For
        "Original" will return the zip file content, up to user to extract it.
        "CSV" will return a csv of the splits.
        """
        activity_id = str(activity_id)
        urls = {
            Garmin.ActivityDownloadFormat.ORIGINAL: f"{self.garmin_connect_fit_download}/{activity_id}",
            Garmin.ActivityDownloadFormat.TCX: f"{self.garmin_connect_tcx_download}/{activity_id}",
            Garmin.ActivityDownloadFormat.GPX: f"{self.garmin_connect_gpx_download}/{activity_id}",
            Garmin.ActivityDownloadFormat.KML: f"{self.garmin_connect_kml_download}/{activity_id}",
            Garmin.ActivityDownloadFormat.CSV: f"{self.garmin_connect_csv_download}/{activity_id}",
        }
        if dl_fmt not in urls:
            raise ValueError(f"Unexpected value {dl_fmt} for dl_fmt")
        url = urls[dl_fmt]

        logger.debug("Downloading activities from %s", url)

        return self.connectapi(url).content

    def get_activity_splits(self, activity_id):
        """Return activity splits."""

        activity_id = str(activity_id)
        url = f"{self.garmin_connect_activity}/{activity_id}/splits"
        logger.debug("Requesting splits for activity id %s", activity_id)

        return self.connectapi(url)

    def get_activity_split_summaries(self, activity_id):
        """Return activity split summaries."""

        activity_id = str(activity_id)
        url = f"{self.garmin_connect_activity}/{activity_id}/split_summaries"
        logger.debug("Requesting split summaries for activity id %s", activity_id)

        return self.connectapi(url)

    def get_activity_weather(self, activity_id):
        """Return activity weather."""

        activity_id = str(activity_id)
        url = f"{self.garmin_connect_activity}/{activity_id}/weather"
        logger.debug("Requesting weather for activity id %s", activity_id)

        return self.connectapi(url)

    def get_activity_hr_in_timezones(self, activity_id):
        """Return activity heartrate in timezones."""

        activity_id = str(activity_id)
        url = f"{self.garmin_connect_activity}/{activity_id}/hrTimeInZones"
        logger.debug("Requesting split summaries for activity id %s", activity_id)

        return self.connectapi(url)

    def get_activity_evaluation(self, activity_id):
        """Return activity self evaluation details."""

        activity_id = str(activity_id)
        url = f"{self.garmin_connect_activity}/{activity_id}"
        logger.debug("Requesting self evaluation data for activity id %s", activity_id)

        return self.connectapi(url)

    def get_activity_details(self, activity_id, maxchart=2000, maxpoly=4000):
        """Return activity details."""

        activity_id = str(activity_id)
        params = {
            "maxChartSize": str(maxchart),
            "maxPolylineSize": str(maxpoly),
        }
        url = f"{self.garmin_connect_activity}/{activity_id}/details"
        logger.debug("Requesting details for activity id %s", activity_id)

        return self.connectapi(url, params=params)

    def get_activity_exercise_sets(self, activity_id):
      """Return activity exercise sets."""

      activity_id = str(activity_id)
      url = f"{self.garmin_connect_activity}/{activity_id}/exerciseSets"
      logger.debug("Requesting exercise sets for activity id %s", activity_id)

      return self.connectapi(url)

    def get_activity_gear(self, activity_id):
        """Return gears used for activity id."""

        activity_id = str(activity_id)
        params = {
            "activityId": str(activity_id),
        }
        url = self.garmin_connect_gear
        logger.debug("Requesting gear for activity_id %s", activity_id)

        return self.connectapi(url, params=params)

    def logout(self):
        """Log user out of session."""

        self.modern_rest_client.get(self.garmin_connect_logout)


class GarminConnectConnectionError(Exception):
    """Raised when communication ended in error."""


class GarminConnectTooManyRequestsError(Exception):
    """Raised when rate limit is exceeded."""


class GarminConnectAuthenticationError(Exception):
    """Raised when authentication is failed."""


class GarminConnectInvalidFileFormatError(Exception):
    """Raised when an invalid file format is passed to upload."""
