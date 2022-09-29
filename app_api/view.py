from flask import render_template, request, flash, redirect, url_for
from mongoengine.queryset.visitor import Q
from mongoengine.errors import ValidationError

from app import app
from models import User
from forms import UserForm
from utils import PaginateQuerySet


@app.route('/')
def index():

    return render_template('index.html')


@app.route('/users')
def users_view():

    num_page = request.args.get('page')
    if num_page and num_page.isdigit():
        num_page = int(num_page)
    else:
        num_page = 1

    # ==search==
    q = request.args.get('q')
    if q:
        users_objects = User.objects(Q(username__icontains=q) | Q(first_name__icontains=q) | Q(user_city__icontains=q))
    else:
        users_objects = User.objects()
    
    if q and not users_objects:
        flash('No matches', 'error')
    elif q:
        flash(f'Found {users_objects.count()} matches', 'confirm')
    
    # ===pagination==
    per_page = 5
    users_objects = PaginateQuerySet(queryset=users_objects, per_page=per_page, num_page=num_page)

    print(users_objects.total_pages)
    return render_template('users.html', users=users_objects)


@app.route('/user/<id>', methods=['POST', 'GET'])
def user_detail(id):
    user_object = User.objects.get(telegram_id=id)

    return render_template('user_detail.html', user=user_object)


@app.route('/create_user', methods=['POST', 'GET'])
def create_user():
    form_object = UserForm()
    
    if form_object.validate_on_submit():
        telegram_id = request.form['telegram_id']
        username=request.form['username']
        first_name = request.form['first_name']
        phone_number = request.form['phone_number']
        email = request.form['email']
        user_city = request.form['user_city']
        is_blocked = True if request.form['is_blocked'] == 'True' else False

        try:
            user = User(
                telegram_id=telegram_id,
                username=username,
                first_name=first_name,
                phone_number=phone_number,
                email=email,
                user_city=user_city,
                is_blocked=is_blocked
            )
            user.save()
            flash(f'User {user.username} successful created', 'confirm')
        except Exception as e:
            flash('Something do wrong', 'error')
            print('Error here', e)

        return redirect(url_for('user_detail', id=user.telegram_id))
    
    return render_template('create_user.html', form=form_object)


@app.route('/edit_user/<id>', methods=['POST', 'GET'])
def edit_user(id):
    user_object = User.objects.get(telegram_id=id)

    if request.method == 'POST':
        try:
            user_form = UserForm(formdata=request.form, obj=user_object)

            user_form.is_blocked.data = True if user_form.is_blocked.data == 'True' else False

            user_form.populate_obj(user_object)
            user_object.save()        
            flash('User successful edit', 'confirm')
            return redirect(url_for('user_detail', id=user_object.telegram_id))
        except ValidationError:
            flash('User not edited: fillin useremail', 'error')
            return redirect(url_for('user_detail', id=user_object.telegram_id))

    form_object = UserForm(obj=user_object)
    return render_template('edit_user.html', user=user_object, form=form_object)


@app.route('/delete_user/<id>', methods=['GET', 'POST'])
def delete_user(id):
    user_object = User.objects.get(telegram_id=id)
    if request.method == 'POST':
        try:
            user_object.delete()
            flash(f'User {user_object.username} successful deleted', 'confirm')
            print('User deleted')
        except Exception as ex:
            flash('Something do wrong', 'error')
            print('Error here', ex)

        return redirect(url_for('users_view'))
    return render_template('user_delete.html', user=user_object)
