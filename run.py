import gspread
from google.oauth2.service_account import Credentials


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("love_sandwiches")


def get_sales_data():
    """
    Get sales figures from the user.
    Run a while loop to collect a valid string of data from the user
    via the terminal, which must be a string of 6 integers separated
    by commas. The loop will repeatedly request data until it is valid.
    """
    while True:
        print("Please enter sales data form the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here:")

        sales_data = data_str.split(",")

        if validate_data(sales_data):
            break

    return sales_data


def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True


def update_worksheet(data: list, worksheet: str):
    """Updates a worksheet with a list of integers.

    Receives a list of integers to be inserted into a worksheet.
    Update the relevant worksheet with the data provided. Data
    is appended as last row in worksheet.

    Args:
        data : data list to be appended to a worksheet
        worksheet : name of the worksheet to be updated
    """
    print(f"Updating {worksheet} worksheet...\n")
    current_worksheet = SHEET.worksheet(worksheet)
    current_worksheet.append_row(data)
    print(f"{worksheet} worksheet updated successfully.\n".capitalize())


def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.

    The surplus is defined as the sales figure subtracted from the stock:
    - Positive surplus indicates waste.
    - Negative surplus indicates extra made when stock was sold out.
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    stock_row_data = [int(num) for num in stock_row]
    surplus_data = [x - y for x, y, in zip(stock_row_data, sales_row)]

    return surplus_data


def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(surplus_data, "surplus")


print("Welcome to Love Sandwiches Data Automation")
main()
