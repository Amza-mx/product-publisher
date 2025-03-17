from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from config import settings


class GoogleSheetsAPI:
    def __init__(
            self,
            credentials_file: str = settings.GOOGLE_SHEETS_CREDENTIALS_FILE,
            spreadsheet_id: str = settings.GOOGLE_SHEETS_SPREADSHEET_ID,
            range_name: str = settings.GOOGLE_SHEETS_RANGE_NAME
        ):
        self.credentials_file = credentials_file
        self.spreadsheet_id = spreadsheet_id
        self.range_name = range_name
        self.credentials = self.get_credentials()
        self.service = self.get_service()
        self.sheet = self.service.spreadsheets()
        self.values = self.get_values()


    def get_credentials(self):
        """
        Retrieves the Google service account credentials.

        This method loads the credentials from the file specified by the
        `credentials_file` attribute using the `Credentials.from_service_account_file`
        method from the Google Auth library.

        Returns:
            google.auth.credentials.Credentials: An instance containing the service account credentials.

        Raises:
            Any exceptions thrown due to issues with loading the credentials file, such as
            a FileNotFoundError if the file does not exist or a ValueError if the file is malformed.
        """
        return Credentials.from_service_account_file(self.credentials_file)
    
    def get_service(self):
        """
        Returns a Google Sheets API service object.

        This method builds and returns an instance of the Google Sheets API service using the
        configured credentials. The service object can be used to make API requests to interact
        with Google Sheets.

        Returns:
            googleapiclient.discovery.Resource: An instance of the Google Sheets API service.
        """
        return build('sheets', 'v4', credentials=self.credentials)
    
    def get_values(self):
        """
        Retrieve values from a specified range in the Google Sheet.

        This method uses the Google Sheets API to fetch cell values from the sheet
        identified by the instance's `spreadsheet_id` and bounded by `range_name`.
        The returned value is a list of rows, where each row is a list of cell values.
        If no data is present in the specified range, an empty list is returned.

        Returns:
            list: A list of rows (each row being a list of values); returns an empty list if
            no values are found.
        """
        result = self.sheet.values().get(spreadsheetId=self.spreadsheet_id, range=self.range_name).execute()
        return result.get('values', [])
    
    def update_values(self, data: list[list]) -> int:
        """
        Updates cell values in the specified Google Sheet range.

        This method constructs a request body with the given data and sends an update
        request to the Google Sheets API. The API call uses the 'RAW' value input option,
        meaning that the values are interpreted exactly as provided, without any conversion.

        Args:
            data (list[list[Any]]): A two-dimensional array where each inner list represents
                a row of values to update in the sheet.

        Returns:
            int: The number of cells that were updated as reported by the API response.

        Raises:
            googleapiclient.errors.HttpError: If the API request fails.
        """
        body = {
            'values': data
        }

        result = self.sheet.values().update(
            spreadsheetId=self.spreadsheet_id,
            range=self.range_name,
            valueInputOption='RAW',
            body=body
        ).execute()

        return result.get('updatedCells')
    
    def get_columns(self, columns: list[str]) -> list[list]:
        """
        Retrieves specified columns from the data set stored in self.values.

        This method treats the first row of self.values as the header containing column names, and
        all subsequent rows as data. For each row in the data, it extracts the values corresponding
        to the columns provided in the "columns" parameter by determining their index from the header row.

        Parameters:
            columns (list of str): The list of column names to extract from each data row.

        Returns:
            list of list: A list where each sublist contains the values from a data row corresponding to
                          the specified columns.
        """
        headers = self.values[0]
        data = self.values[1:]
        return [[row[headers.index(column)] for column in columns] for row in data]
    
    def update_column(self, column: str, data: list) -> list:
        """
        Updates the specified column in the sheet's values using the internal state.

        This method locates the column by its header name and updates each cell in that column
        with the corresponding value from the internally stored data. Then, it calls update_values()
        to persist the modified data.

        Parameters:
            column (str): The name of the column header whose values are to be updated.
            data (list): A list of new values intended for the column. Note that in the current
                         implementation, this parameter is overwritten by the existing internal
                         data (i.e., self.values[1:]), so its provided value has no effect.

        Raises:
            ValueError: If the specified column name is not found in the header row.

        Returns:
            list: The updated data after the column values have been modified.
        """
        headers = self.values[0]
        data = self.values[1:]
        column_index = headers.index(column)

        for i, row in enumerate(data):
            row[column_index] = data[i]

        self.update_values(data)
        return data

    # Get the ASINS from the Google Sheet
    def get_asins_from_sheet(self):
        asins = self.get_columns(['ASIN',])
        return [asin[0] for asin in asins]

