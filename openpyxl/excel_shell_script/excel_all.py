# -*- coding: utf-8 -*-

import openpyxl
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Color

if __name__ == '__main__':
    excel_file = Workbook()
    sheet = excel_file.active
    file = open("ABC.py", 'w')
    file1 = open("small_than_1.txt", 'w')
    file2 = open("large_than_1.txt", 'w')

    print("A와 B 두행에 입력하세요.")
    print("A행은 항목이름 B행은 데이터값.")
    print("ex) 시작 셀번호 : A1, 끝 셀번호 : B5")
    print("     | A 행 |  B행 ")
    print(" ------------------")
    print(" 1열 |  cat |  1.3 ")
    print(" 2열 |  dog |  0.5 ")
    print(" 3열 | wolf |  135 ")
    print(" 4열 |  cow | 0.62 ")
    print("\n")
    a = raw_input("시작 셀번호를 입력하세요: ")
    b = raw_input("끝 셀번호를 입력하세요: ")
    cell_range = sheet[a:b]
    new_py_file = list()

    for row in cell_range:
        for cell in row:
            c = raw_input("%s 셀의 데이터값을 입력하세요: " %cell)
            cell.value = c
            new_py_file.append(c)


    data1 = '''if __name__ == "__main__":
    a = list() 
    '''
    file.write("%s\n"%data1)

    for e in new_py_file:
        data2 = "    a.append('%s')\n" % e
        file.write(data2)

    data3 = "    print(a)"
    file.write(data3)

    file.close()

    excel_file.save("sh_test.xlsx")
    print("입력된 값이 'sh_test.xlsl'파일로 저장되었습니다.")

    print("주어진 데이터값이 1보다 큰값,적은값 각각 txt파일로 저장되었습니다.")

    excel_file = openpyxl.load_workbook('sh_test.xlsx')
    file1 = open("small_than_1.txt", 'w')
    file2 = open("large_than_1.txt", 'w')
    sheet = excel_file.active

    all_rows = sheet.rows
    row_num = 0
    small = list()
    large = list()
    for row in all_rows:
        row_num += 1
        sheet.cell(row=row_num, column=3, value=str(row[0].value))
        if row_num == 1:
            sheet.cell(row=row_num, column=4, value=row[1].value)
            list_name = row[1].value
        else:
            if row[1].value == None:
                sheet.cell(row=row_num, column=4, value=None)
            elif float(row[1].value) < 1:
                small.append(row[1].value)
                sheet.cell(row=row_num, column=4, value=0)
            else:
                large.append(row[1].value)
                sheet.cell(row=row_num, column=4, value=1)

    file1.write('%s\n' % list_name)
    file2.write('%s\n' % list_name)

    # 파일1쓰기
    for s1 in small:
        data1 = "%s\n" % s1
        file1.write(data1)

    # 파일2 쓰기
    for l1 in large:
        data2 = "%s\n" % l1
        file2.write(data2)

    file1.close()
    file2.close()

    excel_file.save("sh_test_new.xlsx")

    print('\n')

    def color_change():
        print("엑셀의 셀 색상 변경")
        excel_file = openpyxl.load_workbook("sh_test_new.xlsx")
        sheet = excel_file.active

        g = raw_input("시작 셀번호를 입력하세요: ")
        h = raw_input("끝 셀번호를 입력하세요: ")
        cell_range = sheet[g:h]
        for row in cell_range:
            for cell in row:
                cell.fill = PatternFill(patternType='solid', fgColor=Color('FFFF00'))

        excel_file.save("sh_test_new.xlsx")

    def question():
        q = raw_input("셀 색상을 변경하시겠습니까?(y/n):")
        if q == 'Y' or q == 'y':
            color_change()
        elif q == 'N' or q == 'n':
            exit()
        else :
            question()

    question()
