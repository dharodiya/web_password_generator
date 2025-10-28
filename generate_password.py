from flask import Flask, render_template, request, send_file
import random
import string
import io  
import os
print(os.getcwd())

app = Flask(__name__)

def get_characters(include_upper, include_lower, include_digits, include_punct):
    characters = ""
    if include_upper:
        characters += string.ascii_uppercase
    if include_lower:
        characters += string.ascii_lowercase
    if include_digits:
        characters += string.digits
    if include_punct:
        characters += string.punctuation
    if not characters:
        raise ValueError("At least one character type must be selected.")
    return characters

def ensure_strength(password, include_upper, include_lower, include_digits, include_punct):
    if include_upper and not any(c.isupper() for c in password):
        password = password[:-1] + random.choice(string.ascii_uppercase)
    if include_lower and not any(c.islower() for c in password):
        password = password[:-1] + random.choice(string.ascii_lowercase)
    if include_digits and not any(c.isdigit() for c in password):
        password = password[:-1] + random.choice(string.digits)
    if include_punct and not any(c in string.punctuation for c in password):
        password = password[:-1] + random.choice(string.punctuation)
    return password

def generate_passwords(length, count, include_upper, include_lower, include_digits, include_punct):
    characters = get_characters(include_upper, include_lower, include_digits, include_punct)
    passwords = []
    for _ in range(count):
        password = ''.join(random.choice(characters) for _ in range(length))
        password = ensure_strength(password, include_upper, include_lower, include_digits, include_punct)
        passwords.append(password)
    return passwords

@app.route('/', methods=['GET', 'POST'])
def index():
    passwords = []
    if request.method == 'POST':
        try:
            length = int(request.form['length'])
            count = int(request.form['count'])
            include_upper = 'upper' in request.form
            include_lower = 'lower' in request.form
            include_digits = 'digits' in request.form
            include_punct = 'punct' in request.form
            if length < 1 or count < 1:
                raise ValueError("Length and count must be at least 1.")
            passwords = generate_passwords(length, count, include_upper, include_lower, include_digits, include_punct)
        except ValueError as e:
            passwords = [f"Error: {e}"]
    return render_template('index.html', passwords=passwords)

@app.route('/download')
def download():
    passwords = request.args.getlist('passwords')
    if not passwords:
        return "No passwords to download."
    output = io.StringIO()
    for pwd in passwords:
        output.write(pwd + '\n')
    output.seek(0)
    return send_file(io.BytesIO(output.getvalue().encode()), as_attachment=True, download_name='passwords.txt', mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=True)