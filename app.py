from flask import Flask, render_template, request, jsonify
import random, json, os

app = Flask(__name__)

DATA_FILE = "passwords.json"

def load_passwords():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_passwords(passwords):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(passwords, f, ensure_ascii=False, indent=2)

def generate_password(length, use_numbers, use_lower, use_upper, use_symbols, exclude_similar):
    chars = ""
    if use_numbers:
        chars += "0123456789"
    if use_lower:
        chars += "abcdefghijklmnopqrstuvwxyz"
    if use_upper:
        chars += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if use_symbols:
        chars += "~!@#$%^&*()-_=+[]{};:,.<>?/|"

    if exclude_similar:
        chars = chars.replace("o", "").replace("O", "").replace("0", "").replace("l", "").replace("1", "").replace("I", "")

    if not chars:
        return "⚠️ Aucun caractère sélectionné"

    return "".join(random.choice(chars) for _ in range(length))

@app.route('/')
def index():
    passwords = load_passwords()
    return render_template("index.html", passwords=passwords)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    pwd = generate_password(
        int(data['length']),
        data['numbers'],
        data['lowercase'],
        data['uppercase'],
        data['symbols'],
        data['excludeSimilar']
    )
    passwords = load_passwords()
    passwords.append(pwd)
    save_passwords(passwords)
    return jsonify({"password": pwd})

if __name__ == "__main__":
    app.run(debug=True)
