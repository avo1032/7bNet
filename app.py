from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'SPARTA'

from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient('mongodb+srv://test:sparta@cluster0.h3qxi.mongodb.net/Cluster0?retryWrites=true&w=majority',
                        tlsCAFile=ca)
db = client.dbsparta


@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"username": payload["id"]})
        return render_template('index.html', user_info=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))



@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


# @app.route('/user/<username>')
# def user(username):
#     # 각 사용자의 프로필과 글을 모아볼 수 있는 공간
#     token_receive = request.cookies.get('mytoken')
#     try:
#         payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
#         status = (username == payload["id"])  # 내 프로필이면 True, 다른 사람 프로필 페이지면 False
#
#         user_info = db.user.find_one({"username": username}, {"_id": False})
#         return render_template('user.html', user_info=user_info, status=status)
#     except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
#         return redirect(url_for("home"))
#

@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.user.find_one({'username': username_receive, 'password': pw_hash})

    if result is not None:
        payload = {
         'id': username_receive,
         'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        #token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    nickname_receive = request.form['nickname_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,                               # 아이디
        "password": password_hash,                                  # 비밀번호
        "nickname": nickname_receive,                               # 닉네임
        "profile_name": username_receive,                           # 프로필 이름 기본값은 아이디
        "profile_pic": "",                                          # 프로필 사진 파일 이름
        "profile_pic_real": "profile_pics/profile_placeholder.png", # 프로필 사진 기본 이미지
        "profile_info": ""                                          # 프로필 한 마디
    }
    db.user.insert_one(doc)
    return jsonify({'result': 'success'})


@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.user.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})


@app.route('/sign_up/check_dup_nick', methods=['POST'])
def check_dup_nick():
    nickname_receive = request.form['nickname_give']
    exists = bool(db.user.find_one({"nickname": nickname_receive}))
    return jsonify({'result': 'success', 'exists': exists})


@app.route('/update_profile', methods=['POST'])
def save_img():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # 프로필 업데이트
        return jsonify({"result": "success", 'msg': '프로필을 업데이트했습니다.'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@app.route('/posting', methods=['POST'])
def posting():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # 포스팅하기
        return jsonify({"result": "success", 'msg': '포스팅 성공'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@app.route("/get_posts", methods=['GET'])
def get_posts():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # 포스팅 목록 받아오기
        return jsonify({"result": "success", "msg": "포스팅을 가져왔습니다."})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@app.route('/update_like', methods=['POST'])
def update_like():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # 좋아요 수 변경
        return jsonify({"result": "success", 'msg': 'updated'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@app.route("/_get", methods=["GET"])
def movie_get():
    movie_list = list(db.movies.find({}, {'_id': False}))
    review_list = list(db.reviews.find({}, {'_id': False}))

    return jsonify({'movies':movie_list, 'reviews':review_list})


@app.route('/sign_up')
def aa():
    return render_template('sign_up.html')




# @app.route('/comment/<title>')
# def comment(title):
#     token_receive = request.cookies.get('mytoken')
#     payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
#     user_info = db.user.find_one({"username": payload["id"]})
#     # db에서 단어 찾아서 결과 보내기 (리뷰 페이지)
#     comment_list = list(db.reviews.find({'title': title}, {'_id': False}))
#     image = db.movies.find_one({'title': title})
#     # movie_list = list(db.movies.find({'title':title}, {'_id': False}))
#     # print(image)
#     return render_template("comment.html", title=title, image=image, user_info=user_info)

# @app.route('/comment/<title>')
# def comment(title):
#     # db에서 단어 찾아서 결과 보내기 (리뷰 페이지)
#     comment_list = list(db.reviews.find({'title': title}, {'_id': False}))
#     image = db.movies.find_one({'title': title})
#     return render_template("comment.html", title=title, image=image)


@app.route('/comment/<title>')
def comment(title):
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"username": payload["id"]})
        image = db.movies.find_one({'title': title})
        comment_list = list(db.reviews.find({'title': title}, {'_id': False}))
        return render_template('comment.html', title=title, user_info=user_info, image=image)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


# @app.route('/write/<title>')
# def comment_write(title):
#     # db에서 단어 찾아서 결과 보내기 (리뷰작성 페이지)
#     comment_list = list(db.reviews.find({}, {'_id': False}))
#     print(comment_list)
#     return render_template("comment_write.html", title=title, reviews=comment_list)


@app.route('/write/<title>')
def comment_write(title):
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"username": payload["id"]})
        comment_list = list(db.reviews.find({}, {'_id': False}))
        return render_template('comment_write.html', user_info=user_info, title=title, reviews=comment_list)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


@app.route("/write_post", methods=["POST"])
def comment_post():
    # 작성한 코멘트 DB에 저장하기
    # nickname_receive = request.form["nickname_give"]

    title_receive = request.form["title_give"]
    star_receive = request.form["star_give"]
    comment_receive = request.form["comment_give"]
    nick_receive = request.form["nick_give"]

    review_list = list(db.reviews.find({}, {'_id': False}))
    count = len(review_list) + 1

    doc = {
        'num': count,
        'nickname': nick_receive,
        'title': title_receive,
        'star': star_receive,
        'comment': comment_receive,
        'like_count': 0
    }

    db.reviews.insert_one(doc)
    db.reviews.delete_one({'comment': ""})

    return jsonify({'msg': '작성 완료!'})


@app.route("/comment_get", methods=["GET"])
def comment_get():
    comment_list = list(db.reviews.find({}, {'_id': False}))
    return jsonify({'comments': comment_list})





if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)