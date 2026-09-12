@echo off
cd /d C:\Projetos\repos\homura-cards
uvicorn api.main:app --reload
pause