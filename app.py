from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import unquote
import os, json

app = Flask(__name__)
CORS(app)

# ====================== 数据库配置 ======================
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://infouser:123456@localhost/infoshare'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ====================== 模型定义 ======================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(128))

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

# ====================== 用户接口 ======================
@app.route('/auth/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and user.password == data['password']:
        return jsonify({'token': 'mock-token', 'username': user.username})
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/auth/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'User already exists'}), 400
    new_user = User(username=data['username'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Registered successfully'})

# ====================== 文件接口 ======================

# 上传文件接口
@app.route('/upload', methods=['POST'])
def upload_file_main():
    if 'file' not in request.files:
        return jsonify({'error': 'No file found'}), 400

    file = request.files['file']
    major = request.form.get('major')
    category = request.form.get('category')
    uploader = request.form.get('uploader', 'Anonymous')

    save_dir = os.path.join(UPLOAD_FOLDER, major, category)
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, file.filename)

    # ✅ 检查数据库中是否已存在该文件记录
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

    return jsonify({'message': 'File uploaded successfully', 'filename': file.filename})


# 获取某专业下所有文件分类
@app.route('/files/<major>', methods=['GET'])
def get_files_by_major(major):
    result = {'basic': [], 'research': [], 'job': []}

    files = File.query.filter_by(major=major).all()
    removed = []  # 用于记录删除的无效记录

    for f in files:
        if not os.path.exists(f.filepath):
            removed.append(f)
            continue  # 跳过已丢失的文件

        url = f'/download/{f.major}/{f.category}/{f.filename}'
        if f.category in result:
            result[f.category].append({
                'name': f.filename,
                'url': url
            })

    # ✅ 清理数据库中已不存在的文件记录
    if removed:
        for r in removed:
            db.session.delete(r)
        db.session.commit()
        print(f"已清理 {len(removed)} 条无效文件记录")

    return jsonify(result)


# 下载文件接口（支持中文文件名）
@app.route('/download/<path:filepath>', methods=['GET'])
def download_file(filepath):
    decoded_path = unquote(filepath)
    abs_path = os.path.join(UPLOAD_FOLDER, decoded_path)

    if not os.path.exists(abs_path):
        return jsonify({'error': f'File not found: {abs_path}'}), 404

    return send_file(abs_path, as_attachment=True)


# ====================== 启动应用 ======================
if __name__ == '__main__':
    # 用 0.0.0.0 让局域网可访问
    app.run(host='0.0.0.0', port=5000, debug=True)

