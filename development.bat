@echo off

uvicorn "main:app" "--reload" "--port" "5000" "--host" "0.0.0.0"