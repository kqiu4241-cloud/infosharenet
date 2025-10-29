from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import unquote, quote
from flask_migrate import Migrate
import os
from sqlalchemy import func
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash #哈希函数
# ====================== 初始化 Flask 应用 ======================
app = Flask(__name__)
CORS(app)

# ====================== 数据库配置 ======================
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://infouser:123456@localhost/infoshare'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# ====================== JWT 配置 ======================
app.config['JWT_SECRET_KEY'] = 'your-secret-key'
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_HEADER_NAME'] = 'Authorization'
app.config['JWT_HEADER_TYPE'] = 'Bearer'

jwt = JWTManager(app)

# ====================== 模型定义 ======================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(512))
    avatar = db.Column(db.String(255), default='https://cdn-icons-png.flaticon.com/512/3135/3135715.png')  # 默认头像链接
class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255))
    major = db.Column(db.String(64))
    category = db.Column(db.String(64))
    uploader = db.Column(db.String(64))
    filepath = db.Column(db.String(255))

# ====================== 文件存储配置 ======================
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ====================== 初始化数据库 ======================
with app.app_context():
    db.create_all()

@app.route('/auth/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    # 参数检查
    if not username or not password:
        return jsonify({'error': '用户名和密码不能为空'}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'User already exists'}), 400
    # ✅ 密码加密（默认使用 pbkdf2:sha256）
    hashed_password = generate_password_hash(password)
    # 默认头像
    default_avatar = 'https://cdn-icons-png.flaticon.com/512/3135/3135715.png'
    # 存入数据库
    new_user = User(username=username, password=hashed_password,avatar=default_avatar)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Registered successfully'})

# ====================== 用户接口 ======================
@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    # 验证用户存在 + 密码匹配
    if user and check_password_hash(user.password, password):
        token = create_access_token(identity=username)
        return jsonify({
        'token': token, 
        'message': '登录成功',
        'username': user.username,
        'avatar': user.avatar
        })
    else:
        return jsonify({'message': '用户名或密码错误'}), 401

@app.route('/auth/user', methods=['GET'])
@jwt_required()  # 需要用户登录
def get_user_info():
    current_user = get_jwt_identity()  # 获取当前用户的用户名
    user = User.query.filter_by(username=current_user).first()

    if user:
        # 返回用户信息（例如：头像、用户名等）
        return jsonify({
            'username': user.username,
            'avatar': user.avatar  # 如果你添加了头像字段
        })
    else:
        return jsonify({'message': '用户不存在'}), 404

# ====================== 文件接口 ======================
@app.route('/upload', methods=['POST'])
@jwt_required()
def upload_file_main():
    current_user = get_jwt_identity()
    uploader = current_user

    if 'file' not in request.files:
        return jsonify({'message': '没有上传文件'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': '未选择文件'}), 400

    major = request.form.get('major')
    category = request.form.get('category')

    save_dir = os.path.join(UPLOAD_FOLDER, major, category)
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, file.filename)

    existing = File.query.filter_by(filename=file.filename, major=major, category=category).first()
    if existing:
        return jsonify({'error': '文件已存在，请勿重复上传'}), 400

    file.save(save_path)

    new_file = File(
        filename=file.filename,
        major=major,
        category=category,
        uploader=uploader,
        filepath=save_path
    )
    db.session.add(new_file)
    db.session.commit()

    return jsonify({
        'message': f'文件上传成功 by {uploader}',
        'filename': file.filename
    })


@app.route('/files/<major>', methods=['GET'])
def get_files_by_major(major):
    result = {'basic': [], 'research': [], 'job': []}
    files = File.query.filter_by(major=major).all()
    removed = []

    for f in files:
        if not os.path.exists(f.filepath):
            removed.append(f)
            continue

        url = f'http://192.168.187.135:5000/download/{quote(f.major)}/{quote(f.category)}/{quote(f.filename)}'
        if f.category in result:
            result[f.category].append({
                'id': f.id,
                'name': f.filename,
                'url': url
            })

    if removed:
        for r in removed:
            db.session.delete(r)
        db.session.commit()
        print(f"已清理 {len(removed)} 条无效文件记录")

    return jsonify(result)


@app.route('/download/<path:filepath>', methods=['GET'])
def download_file(filepath):
    decoded_path = unquote(filepath)
    abs_path = os.path.join(UPLOAD_FOLDER, decoded_path)

    if not os.path.exists(abs_path):
        return jsonify({'error': f'File not found: {abs_path}'}), 404

    return send_file(
        abs_path,
        as_attachment=True,
        download_name=os.path.basename(abs_path),
        mimetype='application/octet-stream'
    )


@app.route('/files/delete/<int:file_id>', methods=['DELETE'])
@jwt_required()
def delete_file(file_id):
    current_user = get_jwt_identity()
    file = File.query.get(file_id)

    if not file:
        return jsonify({'error': 'File not found'}), 404

    if file.uploader != current_user:
        return jsonify({'error': 'You do not have permission to delete this file'}), 403

    if os.path.exists(file.filepath):
        os.remove(file.filepath)

    db.session.delete(file)
    db.session.commit()

    return jsonify({'message': 'File deleted successfully'})


@app.route('/files/search', methods=['GET'])
def search_files():
    """
    GET /files/search?keyword=xxx[&category=basic|research|job][&major=信息工程]
    返回：一个数组，每个元素 { name, major, category, url }
    """
    keyword = request.args.get('keyword', '').strip()
    category = request.args.get('category', '').strip()
    major = request.args.get('major', '').strip()

    if not keyword:
        return jsonify({'error': 'Missing keyword'}), 400

    query = File.query.filter(func.lower(File.filename).like(f"%{keyword.lower()}%"))
    if category:
        query = query.filter_by(category=category)
    if major:
        query = query.filter_by(major=major)

    results = query.all()
    found_files = []
    removed = []

    for f in results:
        if not os.path.exists(f.filepath):
            removed.append(f)
            continue

        major_q = quote(f.major, safe='')
        category_q = quote(f.category, safe='')
        filename_q = quote(f.filename, safe='')

        found_files.append({
            'id': f.id,
            'name': f.filename,
            'major': f.major,
            'category': f.category,
            'url': f'http://192.168.187.135:5000/download/{f.major}/{f.category}/{f.filename}'
        })

    if removed:
        for r in removed:
            db.session.delete(r)
        db.session.commit()

    return jsonify(found_files)


# ====================== 启动应用 ======================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

