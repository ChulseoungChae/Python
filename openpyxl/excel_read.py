#-*- coding: utf-8 -*-

# A5 ~ A10까지 데이터를 읽고 출력해주는 프로그램
import openpyxl

if __name__ == '__main__':
    excel_file = openpyxl.load_workbook('test_in.xlsx')     # test_in.xlsx파일 열기

    print(excel_file.sheetnames)                              # 해당 excel파일의 모든 시트이름 출력
    sheet = excel_file['Sheet1']                             # 작업을 원하는 시트 지정
    cell_range = sheet['A5':'A10']                           # cell의 범위 지정


    for row in cell_range:
        for cell in row:

            print(cell.value)                                 # cell 범위 내의 값을 출력
