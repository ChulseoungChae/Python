## ● Openpyxl 을 이용한 엑셀파일 수정기능 개발
--> openpyxl은 엑셀파일을 읽고 수정하는 모듈에 관련된 기본 동작 코드들 입니다.

### ◆ 필요한 라이브러리 설치 및 방법
> - https://github.com/jeonghoonkang/keti/blob/master/BootCamp/cschai/openpyxl/openpyxl_directions.md

#### ◎ excel_read.py 
#### ◎ excel_read.md
> 'test_in.xlsx'의 1번째 시트에서 A5 ~ A10까지 데이터를 읽고 출력해주는 프로그램입니다.

> excel_read.py의 코드들의 설명을 써놓은 파일입니다.

#### ◎ excel_write.py	
#### ◎ excel_write.md
> 'test_in.xlsx'파일의 A열 데이터값을 C열에 입력하고 B열의 데이터값들은 1보다 작으면 0으로,1보다 크거나 같으면 1로 D열에 입력하는 프로그램입니다.

> excel_write.py 코드 설명 파일입니다.

#### ◎ excel_color_change.py	
#### ◎ excel_color_change.md
> 사용자에게 셀 범위를 입력받아 그 범위의 색상을 바꾸는 프로그램입니다.

> excel_color_change.py 코드 설명 파일입니다.

#### ◎ excel_create_DataFile.py	
#### ◎ excel_create_DataFile.md
> 데이터 값을 조건에 따라서 1보다 큰값만 적힌것과 작은값만 적힌 새로운 txt파일로 만드는 프로그램입니다.

> excel_create_DataFile.py 코드 설명 파일입니다.

#### ◎ excel_create_PythonFile.py	
#### ◎ excel_create_PythonFile.md
> 사용자에게 데이터 입력받아 새로운 excel파일과 python파일 생성하는 프로그램입니다.

> excel_create_PythonFile.py 코드 설명 파일입니다.

#### ◎ openpyxl_directions.md
> openpyxl의 설치법과 기본 메서드들을 설명해놓은 파일입니다.

#### ◎ test_in.xlsx
> excel_read.py와 excel_write.py에서 사용되는 엑셀파일입니다.

#### ◎ test_in_new.xlsx
> excel_write.py프로그램을 이용해 생성한 파일입니다.

#### ◎ excel_shell_script폴더
>셸 스크립트를 이용하여 각각의 기능을 하는 파이썬 파일을 합쳐 한번에 구동할 수 있도록한 파일입니다.

#### ◎ image폴더
> 마크다운 작성에 사용한 그림파일입니다.

#### 향후 작업 내용

- To do list
  - run.sh 파일을 만들어서 실행하도록 BASH(배쉬) 스크립트 작성
  - 각 파일로 나누어진 기능을 하나의 파일로 통합하여 구현한 여러개 기능을 하나의 파일로 제공하도록 업그레이드하여 개발

- 완료
  - __name__ == '__main__' 이용하여 코드 작성
  - 실행시에 python {실행파일명} 옵션
    - 에서 sys.args 관련 예제를 추가
  - 실행시에 A5, A10 입력을 받아, 해당 셀의 색깔을 바꾼다
  - 실행시에 입력받은 범위의 데이터를 list 형태의 파일로 저장한다. A5~A10 값을 리스트로 만들고. 해당 리스트를 ABC.py 파일로 저장
  - 조건에 따라 1, 0 으로 표시했던 예제를 업그레이드 하여,
    - 조건에 따라 1로 표시된 데이터만 들어있는 리스트파일 생성
    - 나머지 조건에 따라 0으로 표시된 데이터만 들어있는 리스트파일 생성
    
    
