@ echo off
echo     / /    / /   _______   _______      / /    
echo    / /____/ /   / ___  /  / _____/     / /______
echo   /  ____  /   / /  / /   \_____ \    /  ____  /
echo  / /    / /   / /__/ /__   ____\ \   / /    / /
echo / /    / /   /_________/  /______/  / /    / /
echo *********编译Hash Checker*****************
echo 使用pyinstaller将文件转换成exe...
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
    echo 文件夹已成功删除。
) else (
    echo 文件夹 %buildFolder% 不存在
)

if exist "%sourceFolder%%distFolder%\%executable%" (
    move /y "%sourceFolder%%distFolder%\%executable%" "%sourceFolder%"
)

if exist "%sourceFolder%%distFolder%" (
    rd /s /q "%sourceFolder%%distFolder%"
) else (
    echo 文件夹 "%sourceFolder%%distFolder%" 不存在
)