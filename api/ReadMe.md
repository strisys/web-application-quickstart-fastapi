# FastApi Web App Server

## Virtual Environment Setup (Windows)

1. Open VSCode in the current directory and then open a terminal window.
2. Verify python3 is installed (`py --version` or  `python3 --version `or `python --version`).
3. Run `py -m venv .venv` or `python3 -m venv .venv` to create a virtual environment.  
4. Select the app.py and verify the virtual environment is activated (see [image](./docs/1.png))
5. Run `pip install -r requirements.txt` to install the packages in the requirements.txt file.

Alternaltively, there is a PowerShell script called `setup-venv.ps1` in the scripts folder that uses python3.

## Running the API

To run the server in the debugger simply using the FastAPI debugging configuration.  Otherwise use `run-server.ps1` in the scripts folder.
