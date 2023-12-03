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

class Movie_actor_relation(db.Model): # 表名将会是 movie_actor_relation
    id = db.Column(db.Integer, primary_key=True) # 主键
    movie_id = db.Column(db.String(4)) # 电影id
    actor_id = db.Column(db.String(4)) # 电影上映日期
    type = db.Column(db.String(10)) # 主演/导演

class Move_box(db.Model): # 表名将会是 box
    movie_id = db.Column(db.Integer, primary_key=True) # 主键
    box = db.Column(db.Float) # 电影票房

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
        {'id': '1001', 'title': '战狼2', 'date': '2017/7/27', 'country': '中国', 'type': '战争', 'year': '2017'},
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
        actor = Actor(actor_id=a['actor_id'], name=a['name'], gender=a['gender'], acountry=a['country'])
        db.session.add(actor)

    db.session.commit()
    click.echo('Done.')

@app.cli.command()
def forge3():
    """Generate fake data."""
    db.create_all()
    # 全局的两个变量移动到这个函数内
    name = 'ShenglanQiang'
    relations = [
        {'id':'1','movie_id':'1001', 'actor_id':'2001','type':'主演'},
        {'id':'2','movie_id':'1001','actor_id':'2001','type':'导演'},
        {'id':'3','movie_id':'1002','actor_id':'2002','type':'导演'},
        {'id':'4','movie_id':'1003','actor_id':'2003','type':'主演'},
        {'id':'6','movie_id':'1003','actor_id':'2004','type':'导演'},
        {'id':'7','movie_id':'1004','actor_id':'2005','type':'导演'},
        {'id':'8','movie_id':'1004','actor_id':'2006','type':'主演'},
        {'id':'9','movie_id':'1004','actor_id':'2007','type':'主演'},
        {'id':'10','movie_id':'1005','actor_id':'2008','type':'导演'},
        {'id':'11','movie_id':'1005','actor_id':'2009','type':'主演'},
        {'id':'12','movie_id':'1005','actor_id':'2010','type':'主演'},
        {'id':'13','movie_id':'1006','actor_id':'2011','type':'导演'},
        {'id':'14','movie_id':'1006','actor_id':'2012','type':'主演'},
        {'id':'15','movie_id':'1006','actor_id':'2013','type':'主演'},
        {'id':'16','movie_id':'1007','actor_id':'2014','type':'导演'},
        {'id':'17','movie_id':'1007','actor_id':'2015','type':'主演'},
        {'id':'18','movie_id':'1008','actor_id':'2016','type':'导演'},
        {'id':'19','movie_id':'1008','actor_id':'2017','type':'主演'},
        {'id':'20', 'movie_id':'1009', 'actor_id':'2018', 'type':'导演'},
        {'id':'21', 'movie_id':'1009', 'actor_id':'2019', 'type':'主演'},
        {'id':'22', 'movie_id':'1009', 'actor_id':'2020', 'type':'主演'},
        {'id':'23', 'movie_id':'1010', 'actor_id':'2021', 'type':'导演'},
        {'id':'24', 'movie_id':'1010', 'actor_id':'2022', 'type':'主演'},
        {'id':'25', 'movie_id':'1011', 'actor_id':'2023', 'type':'导演'},
        {'id':'26', 'movie_id':'1011', 'actor_id':'2006', 'type':'主演'},
        {'id':'27', 'movie_id':'1011', 'actor_id':'2024', 'type':'主演'},
        {'id':'28', 'movie_id':'1012', 'actor_id':'2025', 'type':'导演'},
        {'id':'29', 'movie_id':'1012', 'actor_id':'2026', 'type':'主演'},
        {'id':'30', 'movie_id':'1012', 'actor_id':'2027', 'type':'主演'},
        {'id':'31', 'movie_id':'1012', 'actor_id':'2028', 'type':'主演'},
        {'id':'32', 'movie_id':'1013', 'actor_id':'2029', 'type':'导演'},
        {'id':'33', 'movie_id':'1013', 'actor_id':'2030', 'type':'主演'},
        {'id':'34', 'movie_id':'1013', 'actor_id':'2009', 'type':'主演'},
        {'id':'35', 'movie_id':'1013', 'actor_id':'2031', 'type':'主演'},
        {'id':'36', 'movie_id':'1015', 'actor_id':'2032', 'type':'导演'},
        {'id':'37', 'movie_id':'1015', 'actor_id':'2015', 'type':'导演'},
        {'id':'38', 'movie_id':'1015', 'actor_id':'2011', 'type':'导演'},
        {'id':'39', 'movie_id':'1015', 'actor_id':'2015', 'type':'主演'},
        {'id':'40', 'movie_id':'1015', 'actor_id':'2033', 'type':'主演'},
        {'id':'41', 'movie_id':'1015', 'actor_id':'2034', 'type':'主演'},
        {'id':'42', 'movie_id':'1016', 'actor_id':'2035', 'type':'导演'},
        {'id':'43', 'movie_id':'1016', 'actor_id':'2035', 'type':'主演'},
        {'id':'44', 'movie_id':'1016', 'actor_id':'2036', 'type':'主演'},
        {'id':'45', 'movie_id':'1016', 'actor_id':'2022', 'type':'主演'},
        {'id':'46', 'movie_id':'1017', 'actor_id':'2037', 'type':'导演'},
        {'id':'47', 'movie_id':'1017', 'actor_id':'2038', 'type':'导演'},
        {'id':'48', 'movie_id':'1017', 'actor_id':'2008', 'type':'导演'},
        {'id':'49', 'movie_id':'1017', 'actor_id':'2001', 'type':'主演'},
        {'id':'50', 'movie_id':'1017', 'actor_id':'2039', 'type':'主演'},
        {'id':'51', 'movie_id':'1018', 'actor_id':'2040', 'type':'导演'},
        {'id':'52', 'movie_id':'1018', 'actor_id':'2019', 'type':'主演'},
        {'id':'53', 'movie_id':'1018', 'actor_id':'2041', 'type':'主演'},
    ]

    user = User(name=name)
    db.session.add(user)
    for r in relations:
        movie_actor_relation = Movie_actor_relation(id=r['id'], movie_id=r['movie_id'], actor_id=r['actor_id'], type=r['type'])
        db.session.add(movie_actor_relation)

    db.session.commit()
    click.echo('Done.')

import click
@app.cli.command()
def forge4():
    db.create_all()
    # 全局的两个变量移动到这个函数内
    name = 'ShenglanQiang'
    move_boxes = [
        {'movie_id': '1001', 'box': 56.84},
        {'movie_id': '1002', 'box': 50.15},
        {'movie_id': '1003', 'box': 46.86},
        {'movie_id': '1004', 'box': 42.5},
        {'movie_id': '1005', 'box': 36.5},
        {'movie_id': '1006', 'box': 33.97},
        {'movie_id': '1007', 'box': 31},
        {'movie_id': '1008', 'box': 29.12},
        {'movie_id': '1009', 'box': 26.7},
        {'movie_id': '1010', 'box': 25.47},
        {'movie_id': '1011', 'box': 23.9},
        {'movie_id': '1012', 'box': 22.37},
        {'movie_id': '1013', 'box': 30.10},
        {'movie_id': '1014', 'box': 16.02},
        {'movie_id': '1015', 'box': 28.29},
        {'movie_id': '1016', 'box': 54.13},
        {'movie_id': '1017', 'box': 53.48},
        {'movie_id': '1018', 'box': 13.92},
    ]

    user = User(name=name)
    db.session.add(user)
    for b in move_boxes:
        move_box = Move_box(movie_id=b['movie_id'], box=b['box'])
        db.session.add(move_box)

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

from sqlalchemy import join
@app.route('/search', methods=['GET'])
@login_required # 登录保护
def search():
    search_query = request.args.get('word')  # 获取搜索标题
    if search_query:
        movies = db.session.query(Movie.id, Movie.title, Movie.type, Movie.year, Move_box.movie_id, Move_box.box).join(Move_box, Movie.id == Move_box.movie_id).filter(Movie.title.contains(search_query)).all()  # 使用模糊匹配查询数据库
        return render_template('search.html', movies=movies, search_query=search_query)

@app.route('/actor_index/search2', methods=['GET'])
@login_required # 登录保护
def search2():
    search_query2 = request.args.get('word2') # 获取搜索人名
    if search_query2:
        actors = Actor.query.filter(Actor.name.contains(search_query2)).all() # 使用模糊匹配查询数据库
        return render_template('search2.html', actors=actors, search_query2=search_query2)

from sqlalchemy import func
import matplotlib.pyplot as plt
@app.route('/analysis', methods=['GET'])
@login_required # 登录保护
def analysis():
    ana1s = db.session.query(Movie.type, func.round(func.avg(Move_box.box),).label('avg')).join(Move_box, Movie.id == Move_box.movie_id).group_by(Movie.type).all()
    ana2s = db.session.query(Movie.country, func.round(func.avg(Move_box.box), ).label('avg1')).join(Move_box, Movie.id == Move_box.movie_id).group_by(Movie.country).all()
    ana3s = db.session.query(Movie.year, func.round(func.avg(Move_box.box), ).label('avg2')).join(Move_box, Movie.id == Move_box.movie_id).group_by(Movie.year).all()

    # 从 ana1s 中提取类型和平均票房数据
    types = [item[0] for item in ana1s]
    avg_box = [item[1] for item in ana1s]

    # 绘制柱形图
    plt.bar(types, avg_box, color='#8CC629')
    plt.xlabel('Type')
    plt.ylabel('Box Office (Average)')
    plt.title('Average Box Office by Type')
    plt.xticks(rotation=45)

    plt.rcParams['font.sans-serif'] = ['SimHei','Songti SC','STFangsong'] # 正常显示中文
    plt.rcParams['axes.unicode_minus'] = False # 正常显示负号
    # 保存图像文件
    plt.savefig('static/images/type_output.png')
    #清除图形
    plt.clf()
    plt.close('all')

    # 从 ana2s 中提取类型和平均票房数据
    countries = [item[0] for item in ana2s]
    avg_box2 = [item[1] for item in ana2s]

    # 绘制柱形图
    plt.bar(countries, avg_box2, color='#8CC629')
    plt.xlabel('Country')
    plt.ylabel('Box Office (Average)')
    plt.title('Average Box Office by Country')
    plt.xticks(rotation=45)

    plt.rcParams['font.sans-serif'] = ['SimHei', 'Songti SC', 'STFangsong']  # 正常显示中文
    plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号
    # 保存图像文件
    plt.savefig('static/images/country_output.png')
    # 清除图形
    plt.clf()
    plt.close('all')

    # 从 ana3s 中提取类型和平均票房数据
    years = [item[0] for item in ana3s]
    avg_box3 = [item[1] for item in ana3s]

    # 绘制柱形图
    plt.plot(years, avg_box3, color='#8CC629')
    plt.xlabel('Year')
    plt.ylabel('Box Office (Average)')
    plt.title('Average Box Office by Year')
    plt.xticks(rotation=45)

    plt.rcParams['font.sans-serif'] = ['SimHei', 'Songti SC', 'STFangsong']  # 正常显示中文
    plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号
    # 保存图像文件
    plt.savefig('static/images/year_output.png')
    # 清除图形
    plt.clf()
    plt.close('all')

    return render_template('analysis.html', ana1s = ana1s, ana2s = ana2s, ana3s = ana3s)

import lightgbm as lgb
import numpy as np
# 加载保存的模型
model1 = lgb.Booster(model_file='C:/Users/Qiang/watchlist/model1.txt')

@app.route('/predict', methods=['GET'])
@login_required
def predict():
    return render_template('predict.html')

@login_required
@app.route('/result', methods=['GET'])
def result():
        # 获取表单数据
        runtime = request.args.get('runtime')
        num_genres = request.args.get('num_genres')
        genre_Drama = request.args.get('genre_Drama')
        genre_Comedy = request.args.get('genre_Comedy')
        genre_Thriller = request.args.get('genre_Thriller')
        genre_Action = request.args.get('genre_Action')
        genre_Romance = request.args.get('genre_Romance')
        genre_Crime = request.args.get('genre_Crime')
        genre_Adventure = request.args.get('genre_Adventure')
        genre_Horror = request.args.get('genre_Horror')
        genre_Science_Fiction = request.args.get('genre_Science_Fiction')
        num_languages = request.args.get('num_languages')
        language_English = request.args.get('language_English')
        language_French = request.args.get('language_French')
        gender0 = request.args.get('gender0')
        gender1 = request.args.get('gender1')
        log_budget = request.args.get('log_budget')
        homepage = request.args.get('homepage')
        release_date_year = request.args.get('release_date_year')
        quarter = request.args.get('quarter')
        words_title = request.args.get('words_title')

        # 将表单数据转换为一维数组
        input_data = np.array([
            runtime, num_genres, genre_Drama, genre_Comedy, genre_Thriller,
            genre_Action, genre_Romance, genre_Crime, genre_Adventure, genre_Horror,
            genre_Science_Fiction, num_languages, language_English, language_French,
            gender0, gender1, log_budget, homepage, release_date_year, quarter, words_title
        ])
        # 将一维数组转换为二维数组（-1 表示自动推断数组长度）
        input_array = input_data.reshape(-1, 21)
        # 使用模型进行预测
        predictions = model1.predict(input_array)
        # 将预测结果传递给模板，用于在网页上显示
        return render_template('result.html', predictions=predictions)