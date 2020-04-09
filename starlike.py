from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbsparta

# API 역할을 하는 부분
@app.route('/api/list', methods=['GET'])
def star_list():
    # 1. mystar 목록 전체를 검색합니다. ID는 제외하고 like 가 많은 순으로 정렬합니다.
    stars = list(db.mystar.find({},{'_id':False}).sort('like',-1))
    # 2. 성공하면 success 메시지와 함께 stars 목록을 클라이언트에 전달합니다.
    return jsonify({'result': 'success','stars_list':stars})

@app.route('/api/like', methods=['POST'])
def star_like():
    # 1. 클라이언트가 전달한 name_give를 name_receive 변수에 넣습니다.
    name_receive = request.form['name_give']
    star = db.mystar.find_one({'name': name_receive})
    new_like = star['like'] + 1
    db.mystar.update_one({'name': name_receive}, {'$set': {'like': new_like}})
    return jsonify({'result': 'success'})