import json
import subprocess

def read_settings():
    with open('Setting.json', 'r') as temp:
        settings = json.load(temp)
    return settings

def start_file_server(file_root:str, port:int):
    cmd1 = f'start powershell cd {file_root};python -m http.server {port}'
    subprocess.run(cmd1, shell=True)
    cmd2 = f'start powershell .env\\Scripts\\python.exe app.py'
    subprocess.run(cmd2, shell=True)


if __name__ == '__main__':
    settings = read_settings()
    start_file_server(
        file_root=settings['image_path'],
        port=settings['adress']['port']
    )
