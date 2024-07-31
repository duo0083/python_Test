def create_batch_file_for_each_student(student_no, file_name):
    # 배치 파일 코드 시작 부분
    batch_code = f"""@echo off
chcp 65001 >nul
REM 이 배치 파일은 특정 번호의 학생 계정을 생성합니다.

REM 관리자 권한 확인 및 권한 상승 요청
>nul 2>&1 "%SYSTEMROOT%\\system32\\cacls.exe" "%SYSTEMROOT%\\system32\\config\\system"
if '%errorlevel%' NEQ '0' (
    echo 요청: 관리자 권한이 필요합니다.
    echo 이 배치 파일을 다시 관리자 모드로 실행합니다...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

REM 사용자 계정 정보 설정
setlocal EnableDelayedExpansion

REM 사용자 계정과 비밀번호 설정 (계정:비밀번호 형식으로 입력)
set "accounts="""

    # 1학년 전체와 2학년 2반의 사용자 계정 정보 추가
    for grade in range(1, 2):  # 1학년
        for class_no in range(1, 4):  # 1학년의 1반부터 3반까지
            user = f"24{grade}{class_no}{student_no:02}"
            password = f"{grade}{class_no}{student_no:02}"
            batch_code += f"{user}:{password} "

    # 2학년 2반
    user = f"24{2}{2}{student_no:02}"
    password = f"{2}{2}{student_no:02}"
    batch_code += f"{user}:{password} "

    # 게스트 계정
    guest_name = "Guest"
    guest_password = "GuestPassword!"
    batch_code += f"""
REM 게스트 계정 이름 및 비밀번호 설정
set "guest={guest_name}"
set "guest_password={guest_password}"

REM 사용자 계정 생성
for %%A in (%accounts%) do (
    for /f "tokens=1,2 delims=:" %%u in ("%%A") do (
        echo Creating user: %%u with password: %%v
        net user %%u %%v /add /expires:never /passwordchg:no
        net localgroup Users %%u /add
    )
)

REM 게스트 계정 생성
echo Creating guest account: %guest%
net user %guest% %guest_password% /add /expires:never /passwordchg:no
net localgroup Guests %guest% /add
net user %guest% /active:yes

echo 모든 사용자 계정과 게스트 계정이 성공적으로 생성되었습니다.
pause
"""

    # 배치 파일을 UTF-8로 저장
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(batch_code)

    print(f"배치 파일 '{file_name}'이(가) 생성되었습니다.")

# 예시 실행 - 1번부터 30번 학생을 위한 배치 파일 생성
for student_no in range(1, 31):  # 학생 번호 1부터 30까지의 배치 파일 생성
    file_name = f"create_users_student_{student_no:02}.bat"
    create_batch_file_for_each_student(student_no, file_name)
