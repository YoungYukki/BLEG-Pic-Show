from flask import Flask, render_template
import sqlite3
import json
import os

app = Flask(__name__)

@app.route('/')
def index():
    names = get_names()
    info = []
    for name in names:
        number = get_latest_image(name)
        src = f'{host}:{port}/No.{str(number).zfill(4)}/01.jpg'
        info.append([number, src, name])
    info = sort(info)
    return render_template(
        'index.html',
        adress=f'{host}:{port}',
        info = info
    )

def get_names():
    database = sqlite3.connect('Beautyleg.db')
    cur = database.cursor()
    names = set()
    names_res = cur.execute(f'SELECT name FROM IMAGE;').fetchall()
    database.close()
    for name_res in names_res:
        name = name_res[0]
        names.add(name)
    return tuple(names)

def get_latest_image(name:str):
    return get_numbers(name)[0]

# 排序
def sort(info:list):
    new_info = []
    count = 0
    while True:
        count += 1
        for row in info:
            if row[0] == count:
                new_info.append([row[0],row[1],row[2]])
                break
            else:
                continue
        if len(info) <= len(new_info):
            break
    new_info.reverse()
    return new_info

@app.route('/<name>')
def catalog(name):
    numbers = get_numbers(name)
    info = []
    for number in numbers:
        src = f'{host}:{port}/No.{str(number).zfill(4)}/01.jpg'
        info.append([number, src])
    return render_template(
        'catalog.html',
        name=name,
        info = info
    )


def get_numbers(name:str):
    numbers = []
    database = sqlite3.connect('Beautyleg.db')
    cur = database.cursor()
    sql = f'SELECT number FROM IMAGE WHERE name="{name}" ORDER BY number DESC;'
    numbers_res = cur.execute(sql).fetchall()
    for number_res in numbers_res:
        if os.path.exists(f'{image_path}/No.{str(number_res[0]).zfill(4)}'):
            numbers.append(number_res[0])
        else:
            continue
    return numbers

@app.route('/<name>/<number>')
def image(name, number):
    files = os.listdir(f'{image_path}/No.{str(number).zfill(4)}')
    images = []
    for file in files:
        images.append(f'{host}:{port}/No.{str(number).zfill(4)}/{file}')
    return render_template(
        'image.html',
        images=images,
        name=name,
        number=number
    )

if __name__ == '__main__':
    # 读取配置文件
    with open('Setting.json', 'r') as temp:
        settings = json.load(temp)
    host = settings["adress"]["host"]
    port = settings["adress"]["port"]
    image_path = settings["image_path"]
    
    # # 发布
    app.run(host='0.0.0.0', port=5000)