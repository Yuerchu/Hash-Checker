@ echo off
echo     / /    / /   _______   _______      / /    
echo    / /____/ /   / ___  /  / _____/     / /______
echo   /  ____  /   / /  / /   \_____ \    /  ____  /
echo  / /    / /   / /__/ /__   ____\ \   / /    / /
echo / /    / /   /_________/  /______/  / /    / /
echo *********����Hash Checker*****************
echo ʹ��pyinstaller���ļ�ת����exe...
echo ******************************************
pyinstaller HashChecker.spec
echo ******************************************
setlocal
set "sourceFolder=%~dp0"
set "buildFolder=build"
set "distFolder=dist"
set "executable=HashChecker.exe"

if exist "%sourceFolder%%buildFolder%" (
    rd /s /q %buildFolder%
    echo �ļ����ѳɹ�ɾ����
) else (
    echo �ļ��� %buildFolder% ������
)

if exist "%sourceFolder%%distFolder%\%executable%" (
    move /y "%sourceFolder%%distFolder%\%executable%" "%sourceFolder%"
)

if exist "%sourceFolder%%distFolder%" (
    rd /s /q "%sourceFolder%%distFolder%"
) else (
    echo �ļ��� "%sourceFolder%%distFolder%" ������
)