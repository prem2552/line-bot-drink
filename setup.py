from datetime import datetime
from pythainlp.util import thai_strftime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# from test import Rectangle

now = datetime.now()
today = thai_strftime(now, "%d/%m/%y")
time_now = now.strftime("%H:%M:%S")


def setup():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        "credential/studied-bounty-491202-b7-b54a295d11df.json", scope
    )

    client = gspread.authorize(credentials)
    file_sheet = client.open("Daily Quest of Prem")

    # work_sheet = file_sheet.worksheet(sheet_name)
    return file_sheet
