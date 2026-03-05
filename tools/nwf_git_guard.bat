@echo off
echo ===============================
echo NWF Git Guard System
echo ===============================
echo.

echo [1] Repository status
git status
echo.

echo [2] Current branch
git branch
echo.

echo [3] Last commits
git log --oneline -5
echo.

echo [4] Remote check
git remote -v
echo.

echo [5] SSH connection test
ssh -T git@github.com
echo.

echo ===============================
echo Guard check complete
echo ===============================
pause