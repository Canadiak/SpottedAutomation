from __future__ import print_function
from googleapiclient.discovery import build
from google.oauth2 import service_account

#Row 7216 has the reference formatting formula
class Sheets_Controller:
    def __init__(self, spreadsheet_id, sheet_id):
        # Go to service accounts and create credentials
        self.SERVICE_ACCOUNT_FILE = 'sheet_keys.json'
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

        self.creds = None
        self.creds = service_account.Credentials.from_service_account_file(
                self.SERVICE_ACCOUNT_FILE, scopes=self.SCOPES)

        # The ID of a sample spreadsheet.
        self.spreadsheet_id = spreadsheet_id
        self.sheet_id = sheet_id
        self.service = build('sheets', 'v4', credentials=self.creds)
        print("Service: ")
        print(self.service)
   

    def get_confessions_object(self, cell_range):
        subsheet = self.service.spreadsheets()
        print("Subsheet: ")
        print(subsheet)
        print("Cell range: ")
        print(cell_range)
        result = subsheet.values().get(spreadsheetId=self.spreadsheet_id,
                                range=cell_range).execute()
        print("Result: ")
        print(result)
        values = result.get('values', [])
        print("Values: ")
        print(values)
        return values

    def update_sheet(self, values, cell_range):
        
        body = {
            'values' : values
        }

        result = self.service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheet_id, range=cell_range,
            valueInputOption="USER_ENTERED", body=body).execute()
        print('{0} cells updated.'.format(result.get('updatedCells')))

    def update_row_formatting(self, cell_row):
        request_body = {
            'requests': [
                {
                    'repeatCell':{
                        'range': {
                            "sheetId": self.sheet_id,
                            "startRowIndex": cell_row-2,
                            "endRowIndex": str(int(cell_row)-1)
                        },
                        "cell":{
                            'userEnteredFormat':{
                                'backgroundColor': {
                                    'red': float(161/255),
                                    'green': float(212/255),
                                    'blue': float(164/255),
                                }
                            #    'numberFormat' :{
                            #        'type': 'CURRENCY',
                            #
                            #    }
                            }
                        },
                        'fields': 'userEnteredFormat(backgroundColor)'
                    }
                }
            ]
        }

        response = self.service.spreadsheets().batchUpdate(
            spreadsheetId = self.spreadsheet_id,
            body=request_body
        ).execute()
        print("Active row: ")
        print(cell_row)

