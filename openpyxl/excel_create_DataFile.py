# -*- coding: utf-8 -*-
# 엑셀파일 - 데이터 값을 조건에 따라서 1보다 큰값만 적힌것과 작은값만 적힌 새로운 txt파일로 만들기
import openpyxl

if __name__ == '__main__':

    file1 = open("small_than_1.txt", 'w')
    file2 = open("large_than_1.txt", 'w')

    excel_file = openpyxl.load_workbook('test_in.xlsx')    
    sheet = excel_file['Sheet1']                           

    all_rows = sheet.rows
    row_num = 0
    small = list()
    large = list()
    for row in all_rows:
        row_num += 1
        sheet.cell(row = row_num, column = 3, value = str(row[0].value))
        if row_num == 1:
            sheet.cell(row=row_num, column=4, value=row[1].value)
            list_name = row[1].value
        else:
            if row[1].value == None :
                sheet.cell(row = row_num, column = 4, value = None)
            elif row[1].value < 1:
                small.append(row[1].value)
                sheet.cell(row=row_num, column=4, value=0)
            else :
                large.append(row[1].value)
                sheet.cell(row = row_num, column = 4, value = 1)

    file1.write('%s\n'% list_name)
    file2.write('%s\n'% list_name)

    #파일1쓰기
    for s1 in small:
        data1 = "%s\n" % s1
        file1.write(data1)

    #파일2 쓰기
    for l1 in large:
        data2 = "%s\n" % l1
        file2.write(data2)

    file1.close()
    file2.close()

    excel_file.save("test_in_new.xlsx")
