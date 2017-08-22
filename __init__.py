from flask import Flask, render_template, redirect, url_for, request, g
import sqlite3
import string

app = Flask(__name__)


def caesar(plaintext, shift):
    import unicodedata
    plaintext = unicodedata.normalize('NFKD', plaintext).encode('ascii','ignore')
    alphabet = '1fsf34sfa324e32d3vylker2fb'
    shifted_alphabet = alphabet[shift:] + alphabet[:shift]
    table = string.maketrans(alphabet, shifted_alphabet)
    return plaintext.translate(table)

# niko pass 'pass_123'
def check_password(hashed_password, user_password):
    return hashed_password == caesar(user_password, 2)

def validate(username, password):
    con = sqlite3.connect('static/UserXor.db')
    completion = False
    with con:
                cur = con.cursor()
                cur.execute("SELECT * FROM Users")
                rows = cur.fetchall()
                for row in rows:
                    dbUser = row[0]
                    dbPass = row[1]
                    if dbUser==username:
                        completion=check_password(dbPass, password)
    return completion


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        completion = validate(username, password)
        if completion ==False:
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('secret'))
    return render_template('login.html', error=error)

@app.route('/secret')
def secret():
    return "You have successfully logged in"

if __name__ == '__main__':
    app.run(debug=True)
