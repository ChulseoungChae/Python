# -*- coding: utf-8 -*-
#엑셀파일 - 사용자에게 데이터 입력받아 새로운 excel파일, python파일 생성

import openpyxl
from openpyxl import Workbook

if __name__ == '__main__':
    excel_file = Workbook()
    file = open("ABC.py", 'w')
    sheet = excel_file.active                             

    a = raw_input("시작 셀번호를 입력하세요: ")
    b = raw_input("끝 셀번호를 입력하세요: ")
    d = list()
    cell_range = sheet[a:b]
    for row in cell_range:
        for cell in row:
            c = raw_input("%s 셀의 데이터값을 입력하세요: " %cell)
            cell.value = c
            d.append(c)

    data1 = '''if __name__ == "__main__":
    a = list() 
    '''
    file.write("%s\n"%data1)

    for e in d:
        data2 = "    a.append('%s')\n" % e
        file.write(data2)

    data3 = "    print(a)"
    file.write(data3)

    file.close()

    excel_file.save("sample.xlsx")
