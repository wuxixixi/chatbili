@echo off
REM 关闭命令回显

REM 激活 conda 虚拟环境 chatbili
call conda activate chatbili

REM 运行 Streamlit 脚本 main.py
streamlit run main.py