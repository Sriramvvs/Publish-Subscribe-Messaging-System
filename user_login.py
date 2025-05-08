from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import time
import sqlite3

port = 25678
host = 'localhost'

def create_database():
    with sqlite3.connect('data/user_db.db') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS users 
                        (Uname TEXT, name TEXT, pass TEXT, email TEXT, token TEXT)''')


def create_new_user(uname, name, password, email):
    with sqlite3.connect('data/user_db.db') as conn:
        conn.execute('INSERT INTO users (uname, name, pass, email) VALUES (?, ?, ?, ?)', (uname, name, password, email))
        conn.commit()

def get_user_credentials(uname_or_email, passwd):
    with sqlite3.connect('data/user_db.db') as conn:
        cursor = conn.execute('SELECT uname, name, email FROM users WHERE (uname = ? OR email = ?) AND pass = ?', (uname_or_email, uname_or_email, passwd))
        result = cursor.fetchone()
        return result

def check_user_exists(uname, email):
    with sqlite3.connect('data/user_db.db') as conn:
        cursor = conn.execute('SELECT uname FROM users WHERE uname = ? OR email = ?', (uname, email))
        result = cursor.fetchone()
        return result

def update_user_token(uname, token):
    with sqlite3.connect('data/user_db.db') as conn:
        conn.execute('UPDATE users SET token = ? WHERE uname = ?', (token, uname))
        conn.commit()

def get_uname_from_token(token):
    with sqlite3.connect('data/user_db.db') as conn:
        cursor = conn.execute('SELECT uname FROM users WHERE token = ?', (token,))
        result = cursor.fetchone()
        return result[0] if result else None

def action_register(name, uname, passwd, email):
    if check_user_exists(uname, email) is None:
        try:
            create_new_user(uname, name, passwd, email)
            return {'error': False, 'message': 'Registration complete, Please login'}
        except:
            return {'error': True, 'message': 'something went wrong on our end!!!'}
    else:
        return {'error': True, 'message': 'Username/Email already Exists'}

def action_login(uname, passwd):
    user_records = get_user_credentials(uname, passwd)
    print(user_records)
    if user_records is None or user_records[0] == '':
        return {'error': True, 'message': 'Invalid credentials'}
    else:
        timestamp = int(time.time())
        token = user_records[0] + str(timestamp)
        update_user_token(user_records[0], token)
        return {'error': False, 'message': 'Hello, ' + user_records[0] + '!', 'token': token,
                'uname': user_records[0], 'name': user_records[1], 'email': user_records[2]}

def action_subscribe(uname, topic):
    try:
        with sqlite3.connect('data/topics.db') as conn:
            cursor = conn.execute('SELECT subscribers FROM topics WHERE name = ?', (topic,))
            row = cursor.fetchone()
            if row:
                subscribers = row[0].split(',') if row[0] else []
                if uname not in subscribers:
                    subscribers.append(uname)
                    conn.execute('UPDATE topics SET subscribers = ? WHERE name = ?', (','.join(subscribers), topic))
            else:
                conn.execute('INSERT INTO topics (name, subscribers) VALUES (?, ?)', (topic, uname))
            conn.commit()
        return {'error': False, 'message': f'{uname} subscribed to {topic}'}
    except Exception as e:
        print("Subscribe error:", e)
        return {'error': True, 'message': 'Subscription failed. Try again later.'}


class MyServer(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        request_body = self.rfile.read(content_length).decode('utf-8')
        request_data = json.loads(request_body)

        if request_data['action'] == 'register':
            response_data = action_register(request_data['name'], request_data['uname'], request_data['pass'], request_data['email'])
        elif request_data['action'] == 'login':
            response_data = action_login(request_data['uname'], request_data['pass'])
        elif request_data['action'] == 'subscribe':
            response_data = action_subscribe(request_data['uname'], request_data['topic'])
        else:
            response_data = {'error': True, 'message': 'Unknown action'}

        response_body = json.dumps(response_data).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(response_body))
        self.end_headers()
        self.wfile.write(response_body)

server = HTTPServer((host, port), MyServer)
print('Starting server...')
server.serve_forever()
