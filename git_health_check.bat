@echo off
echo ================================
echo NWF Git Health Check
echo ================================

echo.
echo --- CURRENT STATUS ---
git status

echo.
echo --- BRANCHES ---
git branch -a

echo.
echo --- RECENT COMMITS ---
git log --oneline --decorate -5

echo.
echo --- TAGS ---
git tag

echo.
echo --- REMOTES ---
git remote -v

echo.
echo --- TRACKED FILE COUNT ---
git ls-files | find /c /v ""

echo.
echo --- CURRENT HEAD ---
git rev-parse HEAD

echo.
echo ================================
echo Health Check Complete
echo ================================
pause