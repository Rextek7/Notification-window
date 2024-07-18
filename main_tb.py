from flask import Flask, render_template, request, jsonify 
import os 
import json 
from bs4 import BeautifulSoup 
from flask_socketio import SocketIO 
import threading  # добавим эту строку 
 
app = Flask(__name__) 
app.config['SECRET_KEY'] = 'secret!' 
socketio = SocketIO(app) 
 
DATA_FILE = 'data.json' 
if os.path.exists(DATA_FILE): 
    with open(DATA_FILE) as f: 
        data = json.load(f) 
else: 
    with open(DATA_FILE, 'w') as f: 
            json.dump({"rows": []},f) 
    data = {"rows": []} 
 
def html_to_json(html_file_path): 
    with open(html_file_path, 'r', encoding='utf-8') as file: 
        html_content = file.read() 
 
    soup = BeautifulSoup(html_content, 'html.parser') 
 
    rows = soup.find_all('tr') 
 
    data = [] 
 
    for row in rows: 
        cols = row.find_all('td') 
        if len(cols) == 4: 
            number = cols[0].text.strip() 
            surname = cols[1].text.strip() 
            name = cols[2].text.strip() 
            status_select = cols[3].find('select') 
            status = status_select.find('option', selected=True).text.strip() if status_select else "" 
 
            new_data = { 
                "number": number, 
                "surname": surname, 
                "name": name, 
                "status": status 
            } 
 
            data.append(new_data) 
 
    with open('data.json', 'w', encoding='utf-8') as json_file: 
            json.dump(data, json_file, ensure_ascii=False, indent=4) 
 
    return data 
 
 
 
def load_data(): 
        with open(DATA_FILE, 'r') as f: 
            return json.load(f) 
 
 
 
def add_data(new_data): 
    data["rows"].append(new_data)    
    with open(DATA_FILE, 'w') as f: 
        json.dump(data, f, indent=4) 
 
 
@app.route('/') 
def index(): 
 
    return render_template('index.html') 
 
 
# @app.route('/get_data', methods=['GET']) 
# def get_data(): 
#     data = load_data() 
#     return jsonify(data) 
 
@app.route('/submit', methods=["POST"]) 
def submit(): 
    new_data = { 
        "number" : request.form["number"], 
        "surname" : request.form["surname"], 
        "name" : request.form["name"], 
        "status" : request.form["status"] 
    } 
     
    add_data(new_data) 
    return jsonify({"result" : "success"}) 
 
 
@app.route('/process_data', methods=["POST"]) 
def process_data(): 
    html_file = request.files['html_file'] 
 
    save_path = 'C:/101/' 
    if not os.path.exists(save_path): 
         os.makedirs(save_path) 
 
     
    file_path = os.path.join(save_path, html_file.filename) 
    html_file.save(file_path) 
     
    result = html_to_json(file_path) 
 
    return result; 
 
 
# @socketio.on('connect') 
# def handle_connect(): 
#     print("Клиент подключен") 
 
# @socketio.on('add_row') 
# def add_row(data_row): 
#     global data 
#     data.append(data_row) 
#     socketio.emit('update_table', data_row, broadcast=True) 
 
# def console_input(): 
#     while True: 
#         number = input("Введите номер: ") 
#         surname = input("Введите фамилию: ") 
#         name = input("Введите имя: ") 
#         status = input("Введите статус готовности: ") 
          
 
#         data_row = {'surname': surname, 'name': name, 'status': status} 
#         socketio.emit('add_row', data_row) 
 
 
 
     
if name == "__main__": 
    socketio.run(app, host="0.0.0.0", port=5101) 
    app.run(debug=True) 
    # try: 
    #     socketio.run(app, host="0.0.0.0", port=8000, reload=True) 
    # except KeyboardInterrupt: 
    #     pass