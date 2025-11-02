@echo off
echo LSC Portal GitHub Push Script
echo =============================
echo.
echo This script will help you push your LSC Portal project to GitHub.
echo.
set /p username="Enter your GitHub username: "
set /p repo="Enter your repository name: "
echo.
echo Adding remote repository...
git remote add origin https://github.com/%username%/%repo%.git
echo.
echo Setting branch to main...
git branch -M main
echo.
echo Pushing to GitHub...
git push -u origin main
echo.
echo Done! Your project should now be on GitHub.
echo Visit: https://github.com/%username%/%repo%
pause