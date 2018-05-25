#!/bin/bash
echo " run script"
export cmd="python excel_create_PythonFile_sh.py"
exec $cmd
printf "%s\n" "------------------------------------------"
python excel_create_DataFile_sh.py
printf "%s\n" "------------------------------------------"
python excel_color_change_sh.py
