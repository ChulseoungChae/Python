# -*- coding: utf-8 -*-
#엑셀파일 셀 색상 변경하기

import openpyxl
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Color


if __name__ == '__main__':
    print("엑셀의 셀 색상 변경")
    excel_file = openpyxl.load_workbook("sh_test_new.xlsx")
    sheet = excel_file.active

    a = raw_input("시작 셀번호를 입력하세요: ")
    b = raw_input("끝 셀번호를 입력하세요: ")
    cell_range = sheet[a:b]
    for row in cell_range:
        for cell in row:
            cell.fill = PatternFill(patternType='solid',fgColor=Color('FFFF00'))

    excel_file.save("sh_test_new.xlsx")
