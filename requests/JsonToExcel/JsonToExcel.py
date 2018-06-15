# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
import json
import openpyxl
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Color

#import pandas

def input_filename():
    usage = "\n usage : python %s {FileName} " %sys.argv[0]
    print ( usage + '\n'  )

    _len = len(sys.argv)

    if _len < 1:
        print (" 파일 이름을 입력해주세요 ")
        print (" check *run.sh* file ")
        exit (" You need to input File name, please try again \n")

    file_name = sys.argv[1]

    return file_name


def WriteDataInExcel(_dict):
    col_num = 1

    for one_dict in _dict:
        for k, v in one_dict.iteritems():
            if k == 'period':
                sheet.cell(row=1, column=1, value=k).fill = PatternFill(patternType='solid', fgColor=Color('4785F0'))
                sheet.cell(row=1, column=2, value=v).fill = PatternFill(patternType='solid', fgColor=Color('FFFF00'))


            if k == 'data':
                for _list in v:
                    for kt, pv in _list.iteritems():
                        if kt == 'carid':
                            sheet.cell(row=3, column=col_num, value=kt).fill = PatternFill(patternType='solid', fgColor=Color('FF0000'))
                            sheet.cell(row=3, column=col_num+1, value=pv).fill = PatternFill(patternType='solid', fgColor=Color('FFFF00'))

                        if kt == 'count':
                            sheet.cell(row=4, column=col_num, value=kt).fill = PatternFill(patternType='solid', fgColor=Color('FF0000'))
                            sheet.cell(row=4, column=col_num+1, value=pv).fill = PatternFill(patternType='solid', fgColor=Color('FFFF00'))

                        if kt == 'time':
                            row_num = 6
                            sheet.cell(row=row_num, column=col_num, value=kt).fill = PatternFill(patternType='solid', fgColor=Color('FF0000'))
                            for pv_list in pv:
                                sheet.cell(row=row_num, column=col_num+1, value=pv_list).fill = PatternFill(patternType='solid', fgColor=Color('FFFF00'))
                                row_num += 1

                    col_num += 4

        #print(col_num)
        col_num +=3

        for k, v in one_dict.iteritems():
            if k == "timestamp_count":
                sheet.cell(row=4, column=col_num, value=k).fill = PatternFill(patternType='solid', fgColor=Color('FF0000'))
                row_num = 6
                for td_k, td_v in v.iteritems():
                    sheet.cell(row=row_num, column=col_num, value=td_k).fill = PatternFill(patternType='solid', fgColor=Color('00FF00'))
                    sheet.cell(row=row_num, column=col_num+1, value=td_v).fill = PatternFill(patternType='solid', fgColor=Color('CCEEFF'))
                    row_num += 1
                    if row_num == 15006:
                        row_num = 6
                        col_num += 4

        #print(col_num)

    return None


if __name__ == "__main__":
    fn = input_filename()

    excel_file = Workbook()
    sheet = excel_file.active

    json_data=open(fn)
    dict = json.load(json_data)
    #print(dict[0]['data'][0]['carid'])

    WriteDataInExcel(dict)

    excel_file.save(fn + '.xlsx')

    #pandas.read_json(fn).to_excel(fn + '.xlsx')
