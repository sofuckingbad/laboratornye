from flask import Flask, request, render_template

app = Flask(__name__)

submitted_data = {}
@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    surname = request.form['surname']
    name = request.form['name']
    patronymic = request.form['patronymic']
    email = request.form['email']
    country = request.form['country']
    city = request.form['city']
    languages = request.form.getlist('languages')
    professions = request.form.getlist('professions')
    password = request.form['password']
    additional_info = request.form['additional-info']
    student = request.form['student']

    print(f"Отправленные данные: {surname}, {name}, {patronymic}, {email}, {country}, {city}, {languages}, {professions}, {password}, {additional_info}, {student}")

    global submitted_data
    submitted_data = {  # Сохраняем данные в глобальную переменную
        'surname': surname,
        'name': name,
        'patronymic': patronymic,
        'email': email,
        'country': country,
        'city': city,
        'languages': languages,
        'professions': professions,
        'password': password,
        'additional_info': additional_info,
        'student': student
    }

    return render_template('form.html', **submitted_data)


@app.route('/form_load')
def load_form():
    return render_template('form_load.html')

@app.route('/load_data', methods=['GET'])
def load_data():
    return submitted_data

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5500)
