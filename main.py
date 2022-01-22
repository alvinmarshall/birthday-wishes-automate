import os


def load_google_sheet():
    google_sheet_url = os.getenv("GOOGLE_SHEET_URL")
    print("sheet", google_sheet_url)


if __name__ == '__main__':
    load_google_sheet()
    pass
