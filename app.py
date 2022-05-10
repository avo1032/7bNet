from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient('mongodb+srv://test:sparta@cluster0.h3qxi.mongodb.net/Cluster0?retryWrites=true&w=majority',
                     tlsCAFile=ca)
db = client.dbsparta

@app.route('/comment')
def home():
    return render_template('comment.html')

@app.route('/comment/write')
def comment():
    return render_template('comment_write.html')

# @app.route('/')
# def main():
#     # DB에서 저장된 단어 찾아서 HTML에 나타내기
#     msg = request.args.get("msg")
#     words = list(db.title.find({}, {"_id":False}))
#     return render_template("index.html", words = words, msg=msg)

@app.route("/comment/write", methods=["POST"])
def comment_post():
    # 작성한 코멘트 DB에 저장하기
    # nickname_receive = request.form["nickname_give"]
    # title_receive = request.form["title_give"]
    star_receive = request.form["star_give"]
    comment_receive = request.form["comment_give"]

    review_list = list(db.reviews.find({}, {'_id': False}))
    count = len(review_list) + 1

    doc = {
        'num' : count,
        'nickname' : "",
        'title' : "",
        'star' : star_receive,
        'comment' : comment_receive,
        'like_count' : 0
    }

    db.reviews.insert_one(doc)

    return jsonify({'msg': '작성 완료!'})


@app.route("/comment", methods=["GET"])
def comment_get():
    comment_list = list(db.reviews.find({}, {'_id': False}))
    return jsonify({'comments': comment_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)