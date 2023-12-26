from flask import Blueprint, redirect, url_for, render_template, request, session, current_app, flash
from db import db
from db.models import users, products, cart_items
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.utils import secure_filename


rgz = Blueprint('rgz', __name__)


@rgz.route('/')
@rgz.route('/index')
def start():
    return redirect('/rgz/', code=302)


@rgz.route('/rgz/login', methods=['GET', 'POST'])
def login():
    errors = []
    if request.method == 'GET':
        return render_template('login.html')

    username_form = request.form.get('username')
    password_form = request.form.get('password')

    my_user = users.query.filter_by(username=username_form).first()

    if my_user is not None:
        if check_password_hash(my_user.password, password_form):
            login_user(my_user, remember = False)
            return redirect('/rgz/')
        else: 
            errors.append("Неправильный пароль")
            return render_template('login.html', errors=errors)
        
    if not (username_form or password_form):
        errors.append("Пожалуйста заполните все поля")
        return render_template("login.html", errors=errors)
    if username_form == '':
        errors.append("Пожалуйста заполните все поля")
        print(errors)
        return render_template('login.html', errors=errors)
    if password_form == '':
        errors.append("Пожалуйста заполните все поля")
        print(errors)
        return render_template('login.html', errors=errors)
    else: 
        errors.append('Пользователя не существует')
        return render_template('login.html', errors=errors)
    
@rgz.route('/rgz/register', methods=["GET", "POST"])
def registerPage():
    errors = []

    if request.method == "GET":
        return render_template('register.html', errors=errors)
     
    username_form = request.form.get("username")
    password_form = request.form.get("password")

    
    hashPassword = generate_password_hash(password_form, method='pbkdf2')

    isUserExist = users.query.filter_by(username=username_form).first()
    if isUserExist is not None:
        errors.append("Пользователь уже существует")
        return render_template('register.html', errors=errors)
    
    if username_form is None or password_form is None or username_form.strip() == '' or password_form.strip() == '':
        errors.append("Пожалуйста, заполните все поля")
        print(errors)
        return render_template('register.html', errors=errors)
    if len(password_form) < 5:
            errors.append("Пароль должен содержать не менее 5 символов")
            print(errors)
            return render_template('register.html', errors=errors)

    newUser = users(username=username_form, password=hashPassword)

    db.session.add(newUser)
    db.session.commit()

    return redirect('/rgz/')

@rgz.route('/rgz/')
def main():
    articles = products.query.all()
    return render_template('rgz.html', articles=articles)


@rgz.route('/rgz/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    quantity = int(request.form.get('quantity', 1))
    
    # Создаем запись в корзине
    cart_item = cart_items(user_id=current_user.id, product_id=product_id, quantity=quantity)
    db.session.add(cart_item)
    db.session.commit()
    
    return redirect('/rgz/')

@rgz.route('/rgz/cart')
@login_required
def cart():
    cart_itemss = cart_items.query.filter_by(user_id=current_user.id).all()
    total_cost = sum(item.product.cost * item.quantity for item in cart_itemss)
    return render_template('cart.html', cart_itemss=cart_itemss, total_cost=total_cost)

@rgz.route('/rgz/remove_from_cart/<int:item_id>', methods=['POST'])
@login_required
def remove_from_cart(item_id):
    cart_item = cart_items.query.get_or_404(item_id)
    
    if cart_item.user_id != current_user.id:
        return redirect('/rgz/cart')
    
    db.session.delete(cart_item)
    db.session.commit()
    
    return redirect('/rgz/cart')

@rgz.route('/rgz/checkout', methods=['POST'])
@login_required
def checkout():
    cart_itemss = cart_items.query.filter_by(user_id=current_user.id).all()
    
    for item in cart_itemss:
        db.session.delete(item)
    
    
    db.session.commit()  
    
    return redirect('/rgz/cart')

@rgz.route('/rgz/logout')
@login_required
def logout():
    session.clear()
    return redirect('/rgz/')