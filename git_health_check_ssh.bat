@echo off
echo ================================
echo NWF Git Health Check (SSH)
echo ================================

echo.
echo --- SSH Connection Test ---
ssh -T git@github.com
if %errorlevel% neq 0 (
    echo SSH connection failed!
) else (
    echo SSH connection OK
)

echo.
echo --- CURRENT STATUS ---
git status

echo.
echo --- BRANCHES ---
git branch -a

echo.
echo --- REMOTES ---
git remote -v

echo.
echo --- RECENT COMMITS ---
git log --oneline --decorate -5

echo.
echo --- TAGS ---
git tag

echo.
echo --- CURRENT HEAD ---
git rev-parse HEAD

echo.
echo ================================
echo Health Check Complete
echo ================================
pause