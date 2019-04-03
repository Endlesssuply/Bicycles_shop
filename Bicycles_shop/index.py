from flask import Flask, session, redirect, render_template, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from models import UsersModel, BicyclesModel, DealersModel
from forms import LoginForm, RegisterForm, AddBicycleForm, SearchPriceForm, SearchDealerForm, AddDealerForm
from db import DB

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db = DB()
UsersModel(db.get_connection()).init_table()
BicyclesModel(db.get_connection()).init_table()
DealersModel(db.get_connection()).init_table()


@app.route('/')
@app.route('/index')
def index():
    """
    Главная страница
    :return:
    Основная страница сайта, либо редирект на авторизацю
    """
    # если пользователь не авторизован, кидаем его на страницу входа
    if 'username' not in session:
        return redirect('/login')
    # если админ, то его на свою страницу
    if session['username'] == 'admin':
        return render_template('index_admin.html', username=session['username'])
    # если обычный пользователь, то его на свою
    bicycles = BicyclesModel(db.get_connection()).get_all()
    return render_template('bicycle_user.html', username=session['username'], title='Просмотр базы', bicycles=bicycles)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Страница авторизации
    :return:
    переадресация на главную, либо вывод формы авторизации
    """
    form = LoginForm()
    if form.validate_on_submit():  # ввели логин и пароль
        user_name = form.username.data
        password = form.password.data
        user_model = UsersModel(db.get_connection())
        # проверяем наличие пользователя в БД и совпадение пароля
        if user_model.exists(user_name)[0] and check_password_hash(user_model.exists(user_name)[1], password):
            session['username'] = user_name  # запоминаем в сессии имя пользователя и кидаем на главную
            return redirect('/index')
        else:
            flash('Пользователь или пароль не верны')
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
def logout():
    """
    Выход из системы
    :return:
    """
    session.pop('username', 0)
    return redirect('/login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Форма регистрации
    """
    form = RegisterForm()
    if form.validate_on_submit():
        # создать пользователя
        users = UsersModel(db.get_connection())
        if form.user_name.data in [u[1] for u in users.get_all()]:
            flash('Такой пользователь уже существует')
        else:
            users.insert(user_name=form.user_name.data, email=form.email.data,
                         password_hash=generate_password_hash(form.password_hash.data))
            # редирект на главную страницу
            return redirect(url_for('index'))
    return render_template("register.html", title='Регистрация пользователя', form=form)


"""Работа с велосипедами"""


@app.route('/bicycle_admin', methods=['GET'])
def bicycle_admin():
    """
    Вывод всей информации об всех велосипедах
    :return:
    информация для авторизованного пользователя
    """
    # если пользователь не авторизован, кидаем его на страницу входа
    if 'username' not in session:
        return redirect('/login')
    # если админ, то его на свою страницу
    if session['username'] != 'admin':
        flash('Доступ запрещен')
        redirect('index')
    # если обычный пользователь, то его на свою
    bicycles = BicyclesModel(db.get_connection()).get_all()
    return render_template('bicycle_admin.html',
                           username=session['username'],
                           title='Просмотр велосипедов',
                           bicycles=bicycles)


@app.route('/add_bicycle', methods=['GET', 'POST'])
def add_bicycle():
    """
    Добавление велосипеда
    """
    # если пользователь не авторизован, кидаем его на страницу входа
    if 'username' not in session:
        return redirect('login')
    # если админ, то его на свою страницу
    if session['username'] != 'admin':
        return redirect('index')
    form = AddBicycleForm()
    available_dealers = [(i[0], i[1]) for i in DealersModel(db.get_connection()).get_all()]
    form.dealer_id.choices = available_dealers
    if form.validate_on_submit():
        # создать велосипед
        bicycle = BicyclesModel(db.get_connection())
        bicycle.insert(model=form.model.data,
                    price=form.price.data,
                    weight=form.weight.data,
                    electric=form.electric.data,
                    color=form.color.data,
                    dealer=form.dealer_id.data)
        # редирект на главную страницу
        return redirect(url_for('bicycle_admin'))
    return render_template("add_bicycle.html", title='Добавление велосипеда', form=form)


@app.route('/del_bicycle', methods=['GET', 'POST'])
def del_bicycle():
    """
    Удаление велосипеда
    """
    # если пользователь не авторизован, кидаем его на страницу входа
    if 'username' not in session:
        return redirect('login')
    # если админ, то его на свою страницу
    if session['username'] != 'admin':
        return redirect('index')
    available_dealers = [(i[0], i[1]) for i in DealersModel(db.get_connection()).get_all()]
    # удалить велосипед
    bicycle = BicyclesModel(db.get_connection())
    a = bicycle.get_id(form.price.data, form.weight.data, electric=form.electric.data, color=form.color.data)
    bicycle.delete(a)
    # редирект на главную страницу
    return redirect(url_for('bicycle_admin'))
        

@app.route('/bicycle/<int:bicycle_id>', methods=['GET'])
def bicycle(bicycle_id):
    """
    Вывод всей информации об велосипеде
    :return:
    информация для авторизованного пользователя
    """
    # если пользователь не авторизован, кидаем его на страницу входа
    if 'username' not in session:
        return redirect('/login')
    # если не админ, то его на главную страницу
    '''if session['username'] != 'admin':
        return redirect(url_for('index'))'''
    # иначе выдаем информацию
    bicycle = BicyclesModel(db.get_connection()).get(bicycle_id)
    dealer = DealersModel(db.get_connection()).get(bicycle[6])
    return render_template('bicycle_info.html',
                           username=session['username'],
                           title='Просмотр велосипеда',
                           bicycle=bicycle,
                           dealer=dealer[1])


@app.route('/search_price', methods=['GET', 'POST'])
def search_price():
    """
    Запрос велосипедов, удовлетворяющих определенной цене
    """
    form = SearchPriceForm()
    if form.validate_on_submit():
        # получить все машины по определенной цене
        bicycles = BicyclesModel(db.get_connection()).get_by_price(form.start_price.data, form.end_price.data)
        # редирект на страницу с результатами
        return render_template('bicycle_user.html', username=session['username'], title='Просмотр базы', bicycles=bicycles)
    return render_template("search_price.html", title='Подбор по цене', form=form)


@app.route('/search_dealer', methods=['GET', 'POST'])
def search_dealer():
    """
    Запрос велосипедов, продающихся в определенном дилерском центре
    """
    form = SearchDealerForm()
    available_dealers = [(i[0], i[1]) for i in DealersModel(db.get_connection()).get_all()]
    form.dealer_id.choices = available_dealers
    if form.validate_on_submit():
        #
        bicycles = BicyclesModel(db.get_connection()).get_by_dealer(form.dealer_id.data)
        # редирект на главную страницу
        return render_template('bicycle_user.html', username=session['username'], title='Просмотр базы', bicycles=bicycles)
    return render_template("search_dealer.html", title='Подбор по цене', form=form)


'''Работа с дилерским центром'''


@app.route('/dealer_admin', methods=['GET'])
def dealer_admin():
    """
    Вывод всей информации об всех дилерских центрах
    :return:
    информация для авторизованного пользователя
    """
    # если пользователь не авторизован, кидаем его на страницу входа
    if 'username' not in session:
        return redirect('/login')
    # если админ, то его на свою страницу
    if session['username'] != 'admin':
        flash('Доступ запрещен')
        redirect('index')
    # иначе это админ
    dealers = DealersModel(db.get_connection()).get_all()
    return render_template('dealer_admin.html',
                           username=session['username'],
                           title='Просмотр Дилерских центров',
                           dealers=dealers)


@app.route('/dealer/<int:dealer_id>', methods=['GET'])
def dealer(dealer_id):
    """
    Вывод всей информации о дилерском центре
    :return:
    информация для авторизованного пользователя
    """
    # если пользователь не авторизован, кидаем его на страницу входа
    if 'username' not in session:
        return redirect('/login')
    # если не админ, то его на главную страницу
    if session['username'] != 'admin':
        return redirect(url_for('index'))
    # иначе выдаем информацию
    dealer = DealersModel(db.get_connection()).get(dealer_id)
    return render_template('dealer_info.html',
                           username=session['username'],
                           title='Просмотр информации о дилерском центре',
                           dealer=dealer)


@app.route('/add_dealer', methods=['GET', 'POST'])
def add_dealer():
    """
    Добавление дилерского центра и вывод на экран информации о нем
    """
    # если пользователь не авторизован, кидаем его на страницу входа
    if 'username' not in session:
        return redirect('/login')
    # если админ, то его на свою страницу
    if session['username'] == 'admin':
        form = AddDealerForm()
        if form.validate_on_submit():
            # создать дилера
            dealers = DealersModel(db.get_connection())
            dealers.insert(name=form.name.data, address=form.address.data)
            # редирект на главную страницу
            return redirect(url_for('index'))
        return render_template("add_dealer.html", title='Добавление дилерского центра', form=form)
#http://127.0.0.1:8080/

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
