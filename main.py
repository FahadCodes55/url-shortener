from flask import Flask, request, render_template, redirect
from flask_mysqldb import MySQL
import pyshorteners

app = Flask(__name__, template_folder='template')

# MySQL database configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'url_shortener'

mysql = MySQL(app)

# Create a pyshorteners object
s = pyshorteners.Shortener()


@app.route('/')
def home():
    return render_template('homepage.html')


@app.route('/index', methods=["GET"])
def index():
    return render_template('index.html')


@app.route('/shorten', methods=["POST"])
def shorten_url():
    original_url = request.form.get('original_url')
    if original_url:
        short_code = s.tinyurl.short(original_url)
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO urls (original_url, short_code) VALUES (%s, %s)", (original_url, short_code))
        mysql.connection.commit()
        return render_template('short_url.html', short_code=short_code, original_url=original_url)
    return render_template('index.html', error='Please provide an original URL')


@app.route('/<short_code>')
def redirect_to_original_url(short_code):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT original_url FROM urls WHERE short_url = %s", (short_code,))
    result = cursor.fetchone()
    if result:
        return redirect(result['original_url'])
    return render_template('index.html', error='Short URL not found')


if __name__ == '__main__':
    app.run(debug=True)
