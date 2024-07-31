import os

def create_batch_file_for_each_student_deletion(student_no, file_name):
    # 사용자 계정과 홈 디렉토리 삭제
    batch_code = f"""@echo off
chcp 65001 >nul
REM 이 배치 파일은 특정 번호의 학생 계정과 그에 대한 홈 디렉토리를 삭제합니다.

REM 관리자 권한 확인 및 권한 상승 요청
>nul 2>&1 "%SYSTEMROOT%\\system32\\cacls.exe" "%SYSTEMROOT%\\system32\\config\\system"
if '%errorlevel%' NEQ '0' (
    echo 요청: 관리자 권한이 필요합니다.
    echo 이 배치 파일을 다시 관리자 모드로 실행합니다...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

REM 사용자 계정과 홈 디렉토리 삭제
echo 삭제할 사용자 계정과 홈 디렉토리를 삭제합니다...

    # 1학년 전체와 2학년 2반의 사용자 계정 및 홈 디렉토리 삭제
    for %%A in (1 2 3) do (
        for %%B in (1 2 3) do (
            set "user=24%%A%%B{student_no:02}"
            echo 삭제 중: %%user%%
            net user %%user%% /delete
            rmdir /s /q "C:\\Users\\%%user%%"
        )
    )

    set "user=2422{student_no:02}"
    echo 삭제 중: %%user%%
    net user %%user%% /delete
    rmdir /s /q "C:\\Users\\%%user%%"

REM 게스트 계정 및 홈 디렉토리 삭제
set "guest=Guest"
echo 삭제할 게스트 계정 및 홈 디렉토리를 삭제합니다...
net user %guest% /delete
rmdir /s /q "C:\\Users\\%guest%"

echo 모든 사용자 계정과 관련 홈 디렉토리가 성공적으로 삭제되었습니다.
pause
"""

    # 배치 파일을 UTF-8로 저장
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(batch_code)

    print(f"계정 및 홈 디렉토리 삭제용 배치 파일 '{file_name}'이(가) 생성되었습니다.")

# 예시 실행 - 1번부터 30번 학생을 위한 계정 및 홈 디렉토리 삭제 배치 파일 생성
for student_no in range(1, 31):  # 학생 번호 1부터 30까지의 배치 파일 생성
    file_name = f"delete_users_and_files_student_{student_no:02}.bat"
    create_batch_file_for_each_student_deletion(student_no, file_name)
