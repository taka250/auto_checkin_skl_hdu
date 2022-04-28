from flask import Flask, request
import Skl
import account


app = Flask(__name__)


@app.route('/', methods=["POST"])
def post_data():
    if request.get_json().get('message_type') == 'group' and request.get_json().get('group_id') == int(account.group):
        print(account.group)
        gid = request.get_json().get('group_id')
        uid = request.get_json().get('sender').get('user_id')
        message = request.get_json().get('raw_message')
        skl = Skl.Skl()
        if skl.check_num(message, uid, gid):
            skl.autocheck(message, account.user_1,
                          account.passwd_1, account.group)
            skl.autocheck(message, account.user_2,
                          account.passwd_2, account.group)
    return 'ok'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8001)
