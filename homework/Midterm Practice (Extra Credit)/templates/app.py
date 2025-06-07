from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)

# --- User Model ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    messages = db.relationship('Message', backref='user', lazy=True)
    threads = db.relationship('Thread', backref='user', lazy=True)

# --- Thread Model ---
class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    messages = db.relationship('Message', backref='thread', lazy=True)

# --- Message Model ---
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# --- Routes ---
@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('chat_threads'))
    return "<a href='/login'>Login</a> | <a href='/signup'>Sign Up</a>"

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'error')
            return redirect(url_for('signup'))
        new_user = User(username=username, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        session['user_id'] = new_user.id
        flash('Signup successful!', 'success')
        return redirect(url_for('chat_threads'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('chat_threads'))
        else:
            flash('Invalid credentials.', 'error')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('home'))

@app.route('/threads')
def chat_threads():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    threads = Thread.query.filter_by(user_id=user.id).order_by(Thread.created_at.desc()).all()
    return render_template('threads.html', threads=threads, user=user)

@app.route('/thread/new', methods=['POST'])
def new_thread():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    title = request.form['title'].strip()
    if not title:
        flash('Thread title is required.', 'error')
        return redirect(url_for('chat_threads'))
    thread = Thread(title=title, user_id=session['user_id'])
    db.session.add(thread)
    db.session.commit()
    return redirect(url_for('chat', thread_id=thread.id))

@app.route('/chat/<int:thread_id>')
def chat(thread_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    thread = Thread.query.get_or_404(thread_id)
    if thread.user_id != session['user_id']:
        flash('Unauthorized access.', 'error')
        return redirect(url_for('chat_threads'))
    messages = Message.query.filter_by(thread_id=thread.id).order_by(Message.created_at.asc()).all()
    return render_template('chat.html', messages=messages, thread=thread)

@app.route('/ask/<int:thread_id>', methods=['POST'])
def ask(thread_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    thread = Thread.query.get_or_404(thread_id)
    if thread.user_id != session['user_id']:
        return jsonify({'error': 'Unauthorized'}), 403
    prompt = request.form['prompt']
    response_text = call_groq_api(prompt)
    msg = Message(user_id=session['user_id'], thread_id=thread.id, content=prompt, response=response_text)
    db.session.add(msg)
    db.session.commit()
    return jsonify({ 'reply': response_text })

# --- Groq API ---
def call_groq_api(prompt):
    headers = {
        'Authorization': 'Bearer your_groq_api_key_here',  # 替換為你自己的金鑰
        'Content-Type': 'application/json'
    }
    data = {
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "model": "mixtral-8x7b-32768",
        "temperature": 0.7
    }
    response = requests.post('https://api.groq.com/openai/v1/chat/completions', headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    return "[Error calling AI API]"

# --- 啟動應用 ---
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
