import os.path
import polars as pl

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import src.domain.march_madness.paths as p

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1dB_QszHFnHQfmoGH_EZ-0JXSzsHgeLU3dAahWrQBIPc"
SAMPLE_RANGE_NAME = "All Picks"


def main():
  """Shows basic usage of the Sheets API.
  Prints values from a sample spreadsheet.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists(p.GOOGLE_API_TOKEN):
    creds = Credentials.from_authorized_user_file(p.GOOGLE_API_TOKEN, SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          p.GOOGLE_API_CREDENTIALS, SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open(p.GOOGLE_API_TOKEN, "w") as token:
      token.write(creds.to_json())

  try:
    service = build("sheets", "v4", credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = (
        sheet.values()
        .get(
          spreadsheetId=SAMPLE_SPREADSHEET_ID,
          range=SAMPLE_RANGE_NAME
        )
        .execute()
    )
    values = result.get("values", [])

    if not values:
      print("No data found.")
      return

    columns = values[4]
    data = values[5:72]

    df = pl.DataFrame(data=data, schema=columns, orient='row')
  except HttpError as err:
    print(err)


if __name__ == "__main__":
  main()