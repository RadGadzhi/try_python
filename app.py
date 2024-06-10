import logging #для логгирования действий пользователей
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Настройка логирования
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s',
                    handlers=[logging.FileHandler("app.log", encoding='utf-8'),
                              logging.StreamHandler()])

logger = logging.getLogger(__name__)

class UserAction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)

@app.route('/')
def form():
    logger.info("Form page accessed")
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    age = request.form['age']
    
    # Логируем ввод данных
    logger.info(f"Data received - Name: {name}, Age: {age}")
    
    # Сохраняем данные в базе данных
    new_action = UserAction(name=name, age=int(age))
    db.session.add(new_action)
    db.session.commit()
    
    return redirect(url_for('table'))

@app.route('/table')
def table():
    logger.info("Table page accessed")
    # Получаем данные из базы данных
    data = UserAction.query.all()
    return render_template('table.html', data=data)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    action = UserAction.query.get_or_404(id)
    if request.method == "POST":
        action.name = request.form['name']
        action.page = request.form['age']
        try:
            db.session.commit()
            logger.info(f"Data updated - ID: {id}, Name: {action.name}, Age: {action.age}")
            return redirect(url_for('table'))
        except:
            logger.error("Error updating data")
            return "There was an issue updating your data"
        else: 
            return render_template('edit.html', action=action)

if __name__ == '__main__':
    with app.app_context():
        logger.info("Creating database tables")
        db.create_all()  # Создаем таблицы
    app.run(debug=True, port=5000, threaded=True)  # Измените порт и добавьте параметр threaded