import gspread
import os
import traceback
import pytz

# don't remove this unused import its initialize google cred key
from src.main.ninetales_objects import NinetalesObjects as nb
# from base_utils.common.skulk_objects import SkulkObjects as sb
# from base_utils.error_book.errorbook import ErrorBook
from datetime import datetime

log = None
error = None

class GSheet:
    def __init__(self, logger, workbook="Vulpix-Results"):
        global log, error
        log = logger
        self.gc = gspread.service_account(filename=os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
        self.wb = self.gc.open(workbook)


    def appendRow(self, sheet_name, row):
        try:
            ws = self.wb.worksheet(sheet_name)
            ws.append_row(row, table_range='A1')
        except Exception as ex:
            error.handle(ex, traceback.format_exc(),self.wb.title, sheet_name, row)

    def deletesheet(self, sheet_name):
        try:
            worksheet_list = self.wb.worksheets()
            for sheet in worksheet_list:
                if sheet.title == sheet_name:
                    ws = self.wb.worksheet(sheet_name)
                    self.wb.del_worksheet(ws)
                    break
        except Exception as ex:
            error.handle(ex, traceback.format_exc(), self.wb.title, sheet_name)

    # It will delete, if sheet exist & recreate it.
    def newResultSheet(self):
        try:
            tz_India = pytz.timezone('Asia/Kolkata')
            datetime_India = datetime.now(tz_India)
            title = datetime_India.strftime("%d-%m-%Y_%I-%M_%p")
            self.deletesheet(title)
            worksheet = self.wb.add_worksheet(title=title, rows="500", cols="10")
            worksheet.append_row(nb.result_sheet_head)
            return worksheet.title
        except Exception as ex:
            error.handle(ex, traceback.format_exc())

if __name__ == "__main__":
    gs = GSheet(None)
    gs.newRandomResultSheet()
