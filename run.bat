@echo off
call venv\Scripts\activate
cd src
uvicorn server:app --reload