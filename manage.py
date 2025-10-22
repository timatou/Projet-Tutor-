from flask import Flask, render_template

app = Flask(__name__, static_folder='frontend/static', template_folder='templates')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/etudiants')
def etudiants():
    return render_template('etudiants.html')

@app.route('/modules')
def modules():
    return render_template('modules.html')

@app.route('/notes')
def notes():
    return render_template('notes.html')

@app.route('/absences')
def absences():
    return render_template('absences.html')

@app.route('/statistiques')
def statistiques():
    return render_template('statistiques.html')

if __name__ == '__main__':
    app.run(debug=True)
