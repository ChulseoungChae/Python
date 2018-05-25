# -*- coding: utf-8 -*-
# 엑셀파일 오픈하고 값 입력
import openpyxl
if __name__ == '__main__':
    excel_file = openpyxl.load_workbook('test_in.xlsx')     # test_in.xlsx파일 열기

    sheet = excel_file['Sheet1']                             # 작업을 원하는 시트 지정

    all_rows = sheet.rows
    row_num = 0
    for row in all_rows:
        row_num += 1
        sheet.cell(row = row_num, column = 3, value = str(row[0].value))
        if row_num == 1:
            sheet.cell(row=row_num, column=4, value=row[1].value)
        else:
            if row[1].value == None :
                sheet.cell(row = row_num, column = 4, value = None)
            elif row[1].value < 1:
                sheet.cell(row=row_num, column=4, value=0)
            else :
                sheet.cell(row = row_num, column = 4, value = 1)

    excel_file.save("test_in_new.xlsx")






