from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy # 导入扩展类
from flask_login import LoginManager
from flask_login import UserMixin
from flask_login import login_user
from flask_login import login_required, current_user

import os
import sys

WIN = sys.platform.startswith('win')
if WIN: # 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else: # 否则使用四个斜线
    prefix = 'sqlite:////'
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'  # 等同于 app.secret_key = 'dev'
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # 关闭对模型修改的监控
# 在扩展类实例化前加载配置
db = SQLAlchemy(app)

class Movie(db.Model): # 表名将会是 movie
    id = db.Column(db.Integer, primary_key=True) # 主键
    title = db.Column(db.String(60)) # 电影标题
    date = db.Column(db.String(10)) # 电影上映日期
    country = db.Column(db.String(20)) # 电影国家
    type = db.Column(db.String(4)) # 电影类型
    year = db.Column(db.String(4)) # 电影时间

class Actor(db.Model): # 表名将会是 actor
    actor_id = db.Column(db.Integer, primary_key=True) # 主键
    name = db.Column(db.String(20)) # 演员名字
    gender = db.Column(db.String(2)) # 演员性别
    country = db.Column(db.String(20)) # 演员国家

import click

@app.cli.command() # 注册为命令
@click.option('--drop', is_flag=True, help='Create after drop.')
# 设置选项
def initdb(drop):
    """Initialize the database."""
    if drop: # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.') # 输出提示信息

@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()
    # 全局的两个变量移动到这个函数内
    name = 'ShenglanQiang'
    movies = [
        {'id': '1001', 'title': '战狼2', 'date': '2017/7/27', 'country': '中国', 'type': '战争', 'year': '1988'},
        {'id': '1002', 'title': '哪吒之魔童降世', 'date': '2019/7/26', 'country': '中国', 'type': '动画', 'year': '2019'},
        {'id': '1003', 'title': '流浪地球', 'date': '2019/2/5', 'country': '中国', 'type': '科幻', 'year': '2019'},
        {'id': '1004', 'title': '复仇者联盟4', 'date': '2019/4/24', 'country': '美国', 'type': '科幻', 'year': '2019'},
        {'id': '1005', 'title': '红海行动', 'date': '2018/2/16', 'country': '中国', 'type': '战争', 'year': '2018'},
        {'id': '1006', 'title': '唐人街探案2', 'date': '2018/2/16', 'country': '中国', 'type': '喜剧', 'year': '2018'},
        {'id': '1007', 'title': '我不是药神', 'date': '2018/7/5', 'country': '中国', 'type': '喜剧', 'year': '2018'},
        {'id': '1008', 'title': '中国机长', 'date': '2019/9/30', 'country': '中国', 'type': '剧情', 'year': '2019'},
        {'id': '1009', 'title': '速度与激情8', 'date': '2017/4/14', 'country': '美国', 'type': '动作', 'year': '2017'},
        {'id': '1010', 'title': '西虹市首富', 'date': '2018/7/27', 'country': '中国', 'type': '喜剧', 'year': '2018'},
        {'id': '1011', 'title': '复仇者联盟3', 'date': '2018/5/11', 'country': '美国', 'type': '科幻', 'year': '2018'},
        {'id': '1012', 'title': '捉妖记2', 'date': '2018/2/16', 'country': '中国', 'type': '喜剧', 'year': '2018'},
        {'id': '1013', 'title': '八佰', 'date': '2020/08/21', 'country': '中国', 'type': '战争', 'year': '2020'},
        {'id': '1014', 'title': '姜子牙', 'date': '2020/10/01', 'country': '中国', 'type': '动画', 'year': '2020'},
        {'id': '1015', 'title': '我和我的家乡', 'date': '2020/10/01', 'country': '中国', 'type': '剧情', 'year': '2020'},
        {'id': '1016', 'title': '你好，李焕英', 'date': '2021/02/12', 'country': '中国', 'type': '喜剧', 'year': '2021'},
        {'id': '1017', 'title': '长津湖', 'date': '2021/09/30', 'country': '中国', 'type': '战争', 'year': '2021'},
        {'id': '1018', 'title': '速度与激情9', 'date': '2021/05/21', 'country': '中国', 'type': '动作', 'year': '2021'},
    ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(id=m['id'], title=m['title'], date=m['date'], country=m['country'], type=m['type'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')

import click
@app.cli.command()
def forge2():
    db.create_all()
    # 全局的两个变量移动到这个函数内
    name = 'ShenglanQiang'
    actors = [
        {'actor_id': '2001', 'name': '吴京', 'gender': '男', 'country': '中国'},
        {'actor_id': '2002', 'name': '饺子', 'gender': '男', 'country': '中国'},
        {'actor_id': '2003', 'name': '屈楚萧', 'gender': '男', 'country': '中国'},
        {'actor_id': '2004', 'name': '郭帆', 'gender': '男', 'country': '中国'},
        {'actor_id': '2005', 'name': '乔罗素', 'gender': '男', 'country': '美国'},
        {'actor_id': '2006', 'name': '小罗伯特·唐尼', 'gender': '男', 'country': '美国'},
        {'actor_id': '2007', 'name': '克里斯·埃文斯', 'gender': '男', 'country': '美国'},
        {'actor_id': '2008', 'name': '林超贤', 'gender': '男', 'country': '中国'},
        {'actor_id': '2009', 'name': '张译', 'gender': '男', 'country': '中国'},
        {'actor_id': '2010', 'name': '黄景瑜', 'gender': '男', 'country': '中国'},
        {'actor_id': '2011', 'name': '陈思诚', 'gender': '男', 'country': '中国'},
        {'actor_id': '2012', 'name': '王宝强', 'gender': '男', 'country': '中国'},
        {'actor_id': '2013', 'name': '刘昊然', 'gender': '男', 'country': '中国'},
        {'actor_id': '2014', 'name': '文牧野', 'gender': '男', 'country': '中国'},
        {'actor_id': '2015', 'name': '徐峥', 'gender': '男', 'country': '中国'},
        {'actor_id': '2016', 'name': '刘伟强', 'gender': '男', 'country': '中国'},
        {'actor_id': '2017', 'name': '张涵予', 'gender': '男', 'country': '中国'},
        {'actor_id': '2018', 'name': 'F·加里·格雷', 'gender': '男', 'country': '美国'},
        {'actor_id': '2019', 'name': '范·迪赛尔', 'gender': '男', 'country': '美国'},
        {'actor_id': '2020', 'name': '杰森·斯坦森', 'gender': '男', 'country': '美国'},
        {'actor_id': '2021', 'name': '闫非', 'gender': '男', 'country': '中国'},
        {'actor_id': '2022', 'name': '沈腾', 'gender': '男', 'country': '中国'},
        {'actor_id': '2023', 'name': '安东尼·罗素', 'gender': '男', 'country': '美国'},
        {'actor_id': '2024', 'name': '克里斯海姆斯沃斯', 'gender': '男', 'country': '美国'},
        {'actor_id': '2025', 'name': '许诚毅', 'gender': '男', 'country': '中国'},
        {'actor_id': '2026', 'name': '梁朝伟', 'gender': '男', 'country': '中国'},
        {'actor_id': '2027', 'name': '白百何', 'gender': '女', 'country': '中国'},
        {'actor_id': '2028', 'name': '井柏然', 'gender': '男', 'country': '中国'},
        {'actor_id': '2029', 'name': '管虎', 'gender': '男', 'country': '中国'},
        {'actor_id': '2030', 'name': '王千源', 'gender': '男', 'country': '中国'},
        {'actor_id': '2031', 'name': '姜武', 'gender': '男', 'country': '中国'},
        {'actor_id': '2032', 'name': '宁浩', 'gender': '男', 'country': '中国'},
        {'actor_id': '2033', 'name': '葛优', 'gender': '男', 'country': '中国'},
        {'actor_id': '2034', 'name': '范伟', 'gender': '男', 'country': '中国'},
        {'actor_id': '2035', 'name': '贾玲', 'gender': '女', 'country': '中国'},
        {'actor_id': '2036', 'name': '张小斐', 'gender': '女', 'country': '中国'},
        {'actor_id': '2037', 'name': '陈凯歌', 'gender': '男', 'country': '中国'},
        {'actor_id': '2038', 'name': '徐克', 'gender': '男', 'country': '中国'},
        {'actor_id': '2039', 'name': '易烊千玺', 'gender': '男', 'country': '中国'},
        {'actor_id': '2040', 'name': '徐诣彬', 'gender': '男', 'country': '中国'},
        {'actor_id': '2041', 'name': '米歇尔·罗德里格兹', 'gender': '女', 'country': '美国'},
    ]

    user = User(name=name)
    db.session.add(user)
    for a in actors:
        actor = Actor(actor_id=a['actor_id'], name=a['name'], gender=a['gender'], country=a['country'])
        db.session.add(actor)

    db.session.commit()
    click.echo('Done.')

@app.context_processor
def inject_user(): # 函数名可以随意修改
    user = User.query.first()
    return dict(user=user) # 需要返回字典，等同于return {'user': user}

@app.errorhandler(404) # 传入要处理的错误代码
def page_not_found(e): # 接受异常对象作为参数
    return render_template('404.html'), 404 # 返回模板和状态码

from flask import request, url_for, redirect, flash
# ...
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST': # 判断是否是 POST 请求
        if not current_user.is_authenticated:  # 如果当前用户未认证
            return redirect(url_for('index'))  # 重定向到主页
        # 获取表单数据
        id = request.form.get('id')
        title = request.form.get('title') # 传入表单对应输入字段的name 值
        date = request.form.get('date')
        country = request.form.get('country')
        type = request.form.get('type')
        year = request.form.get('year')
        # 验证数据
        if not title or not year or not date or not type or not country or len(year) > 4 or len(title) > 60 or len(date) > 10 or len(type) > 4 or len(country) > 20:
            flash('Invalid input.') # 显示错误提示
            return redirect(url_for('index')) # 重定向回主页
        # 保存表单数据到数据库
        movie = Movie(id=id, title=title, date=date, country=country, type=type, year=year) # 创建记录
        db.session.add(movie) # 添加到数据库会话
        db.session.commit() # 提交数据库会话
        flash('Item created.') # 显示成功创建的提示
        return redirect(url_for('index')) # 重定向回主页

    user = User.query.first()
    movies = Movie.query.all()
    return render_template('index.html', user=user, movies=movies)

@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])

@login_required
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if request.method == 'POST': # 处理编辑表单的提交请求
        id = request.form['id']
        title = request.form['title']  # 传入表单对应输入字段的name 值
        date = request.form['date']
        country = request.form['country']
        type = request.form['type']
        year = request.form['year']
        if not title or not year or not date or not type or not country or len(year) > 4 or len(title) > 60 or len(date) > 10 or len(type) > 4 or len(country) > 20:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))
# 重定向回对应的编辑页面
        movie.id = id  # 更新id
        movie.title = title # 更新标题
        movie.date = date # 更新日期
        movie.country = country  # 更新国家
        movie.type = type  # 更新类型
        movie.year = year # 更新年份
        db.session.commit() # 提交数据库会话
        flash('Item updated.')
        return redirect(url_for('index')) # 重定向回主页

    return render_template('edit.html', movie=movie) # 传入被编辑的电影记录

from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20)) # 用户名
    password_hash = db.Column(db.String(128)) # 密码散列值

    def set_password(self, password): # 用来设置密码的方法，接受密码作为参数
        self.password_hash = generate_password_hash(password) # 将生成的密码保持到对应字段

    def validate_password(self, password): # 用于验证密码的方法，接受密码作为参数
        return check_password_hash(self.password_hash, password)
    # 返回布尔值

@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, help='The password used to login.')
def admin(username, password):
    """Create user."""
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password) # 设置密码
    else:
        click.echo('Creating user...')
        user = User(username=username, name='ShenglanQiang')
        user.set_password(password) # 设置密码
        db.session.add(user)

    db.session.commit() # 提交数据库会话
    click.echo('Done.')

login_manager = LoginManager(app) # 实例化扩展类
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id): # 创建用户加载回调函数，接受用户 ID 作为参数
    user = User.query.get(int(user_id)) # 用 ID 作为 User 模型的主键查询对应的用户
    return user # 返回用户对象

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        user = User.query.first()
        # 验证用户名和密码是否一致
        if username == user.username and user.validate_password(password):
            login_user(user) # 登入用户
            flash('Login success.')
            return redirect(url_for('index')) # 重定向到主页

        flash('Invalid username or password.') # 如果验证失败，显示错误消息
        return redirect(url_for('login')) # 重定向回登录页面

    return render_template('login.html')

from flask_login import login_required, logout_user
@app.route('/logout')
@login_required # 用于视图保护，后面会详细介绍
def logout():
    logout_user() # 登出用户
    flash('Goodbye.')
    return redirect(url_for('index')) # 重定向回首页

@app.route('/movie/delete/<int:movie_id>', methods=['POST'])
@login_required # 登录保护
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Item deleted.')
    return redirect(url_for('index'))

from flask_login import login_required, current_user
# ...
@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))
        current_user.name = name
        # current_user 会返回当前登录用户的数据库记录对象
        # 等同于下面的用法
        # user = User.query.first()
        # user.name = name
        db.session.commit()
        flash('Settings updated.')
        return redirect(url_for('index'))

    return render_template('settings.html')

@app.route('/actor_index', methods=['GET', 'POST'])
@login_required
def actor_index():
    if request.method == 'POST': # 判断是否是 POST 请求
        if not current_user.is_authenticated:  # 如果当前用户未认证
            return redirect(url_for('actor_index'))  # 重定向到主页
        # 获取表单数据
        actor_id = request.form.get('actor_id')
        name = request.form.get('name') # 传入表单对应输入字段的name 值
        gender = request.form.get('gender')
        country = request.form.get('country')
        # 验证数据
        if not name or not gender or not country or len(name) > 20 or len(gender) > 2 or len(country) > 20:
            flash('Invalid input.') # 显示错误提示
            return redirect(url_for('actor_index')) # 重定向回主页
        # 保存表单数据到数据库
        actor = Actor(actor_id=actor_id, name=name, gender=gender, country=country) # 创建记录
        db.session.add(actor) # 添加到数据库会话
        db.session.commit() # 提交数据库会话
        flash('Item created.') # 显示成功创建的提示
        return redirect(url_for('actor_index')) # 重定向回主页

    user = User.query.first()
    actors = Actor.query.all()
    return render_template('actor_index.html', user=user, actors=actors)

@app.route('/actor_index/actor/edit2/<int:actor_id>', methods=['GET', 'POST'])
@login_required
def edit2(actor_id):
    actor = Actor.query.get_or_404(actor_id)
    if request.method == 'POST': # 处理编辑表单的提交请求
        actor_id = request.form['actor_id']
        name = request.form['name']  # 传入表单对应输入字段的name 值
        gender = request.form['gender']
        country = request.form['country']
        if not name or not gender or not country or len(name) > 20 or len(gender) > 2 or len(country) > 20:
            flash('Invalid input.')
            return redirect(url_for('edit2', actor_id=actor_id))
# 重定向回对应的编辑页面
        actor.actor_id = actor_id  # 更新id
        actor.name = name # 更新名字
        actor.gender = gender # 更新性别
        actor.country = country  # 更新国家
        db.session.commit() # 提交数据库会话
        flash('Item updated.')
        return redirect(url_for('actor_index')) # 重定向回主页

    return render_template('edit2.html', actor=actor) # 传入被编辑的电影记录

@app.route('/actor_index/actor/delete2/<int:actor_id>', methods=['POST'])
@login_required # 登录保护
def delete2(actor_id):
    actor = Actor.query.get_or_404(actor_id)
    db.session.delete(actor)
    db.session.commit()
    flash('Item deleted.')
    return redirect(url_for('actor_index'))
