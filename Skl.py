import requests
import re
import uuid
import time


class Skl(object):
    def check_num(self, message, uid, gid):
        if re.match(r'^[0-9]{4}$', message):
            self.code = message
            return 1
        return 0

    def spider(self):
        response = requests.get(
            'https://cas.hdu.edu.cn/cas/login?state=IFgP7G0QAG0UFHop0M4&service=https%3A%2F%2Fskl.hdu.edu.cn%2Fapi%2Fcas%2Flogin%3Fstate%3DIFgP7G0QAG0UFHop0M4%26index%3D')
        response.enconding = 'utf-8'
        setcookie = response.headers['Set-Cookie']
        p = r'JSESSIONID=([0-9A-Za-z]{1,})'
        cookie = re.search(p, setcookie).group(1)
        p = r'<input type="hidden" id="lt" name="lt" value="(LT-\d{1,}-[0-9A-Za-z]{1,}-cas)" />'
        lt = re.search(p, response.text).group(1)
        p = r'<input type="hidden" name="execution" value="([0-9A-Za-z]{1,})" />'
        execu = re.search(p, response.text).group(1)

        return lt, execu, cookie

    def to_node(self, lt, upwd):
        response = requests.get(
            'http://127.0.0.1:2022/?lt={0}&upwd={1}'.format(lt, upwd)).text
        return response

    def checkin(self, rsa, lt, execu, cookie_1, user, code,passwd):
        url_1 = 'https://cas.hdu.edu.cn/cas/login?state=IFgP7G0QAG0UFHop0M4&service=https%3A%2F%2Fskl.hdu.edu.cn%2Fapi%2Fcas%2Flogin%3Fstate%3DIFgP7G0QAG0UFHop0M4%26index%3D'
        data_1 = {
            'rsa': rsa,
            'ul': len(user),
            'pl': len(passwd),
            'lt': lt,
            'execution': execu,
            '_eventId': 'submit'}

        head_1 = {
            'Host': 'cas.hdu.edu.cn',
            'Origin': 'https://cas.hdu.edu.cn',
            'Upgrade-Insecure-Requests': '1',
            'Cookie': 'hdu_cas_un={0}; JSESSIONID={1}; Language=zh_CN'.format(user, cookie_1),
            'Accept-Encoding': 'gzip, deflate',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
            'Referer': 'https://cas.hdu.edu.cn/cas/login?state=IFgP7G0QAG0UFHop0M4&service=https%3A%2F%2Fskl.hdu.edu.cn%2Fapi%2Fcas%2Flogin%3Fstate%3DIFgP7G0QAG0UFHop0M4%26index%3D'}

        res = requests.post(url_1, data=data_1,
                            headers=head_1, allow_redirects=False)
        url_2 = res.headers['Location']
        p = r'CASTGC=([^;]+)'
        cookie_3 = re.search(p, res.headers['Set-Cookie']).group(1)

        head_2 = {
            'Host': 'skl.hdu.edu.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
            'Upgrade-Insecure-Requests': '1',
            'Referer': 'https://cas.hdu.edu.cn/',
            'Accept-Language': 'zh-CN,zh;q=0.9'}

        url_3 = requests.get(url_2, headers=head_2,
                             allow_redirects=False).headers['Location']

        head_3 = {
            'Host': 'cas.hdu.edu.cn',
            'Upgrade-Insecure-Requests': '1',
            'Cookie': 'CASTGC={0};JSESSIONID={1}; Language=zh_CN'.format(cookie_3, cookie_1),
            'Accept-Encoding': 'gzip, deflate',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
            'Referer': 'https://cas.hdu.edu.cn/'}
        url_4 = requests.get(url_3, headers=head_3,
                             allow_redirects=False).headers['Location']

        head_4 = {
            'Host': 'skl.hdu.edu.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
            'Upgrade-Insecure-Requests': '1',
            'Referer': 'https://cas.hdu.edu.cn/',
            'Accept-Language': 'zh-CN,zh;q=0.9'}
        token = requests.get(url_4, headers=head_4,
                             allow_redirects=False).headers['X-Auth-Token']

        t = int(time.time()*1000)
        url_5 = 'https://skl.hdu.edu.cn/api/checkIn/code-check-in?userid={0}&code={1}&latitude=30.31958&longitude=120.3391&t={2}'.format(
            user, code, t)
        id = str(uuid.uuid1())
        head_5 = {
            'Host': 'skl.hdu.edu.cn',
            'X-Auth-Token': token,
            'Skl-Ticket': id,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
            'Origin': 'https://skl.hduhelp.com',
            'Referer': 'https://cas.hdu.edu.cn/',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Accept-Encoding': 'gzip, deflate'}
        res = requests.get(url_5, headers=head_5).text
        p = '\"msg\":\"(.+)\"'
        msg = re.search(p, res).group(1)
        return(msg)

    def autocheck(self, message, user, passwd, group):
        secret = []
        secret = self.spider()
        lt = secret[0]
        execu = secret[1]
        cookie = secret[2]
        rsa = self.to_node(lt, user+passwd)
        result = 'hdu账号为'+user+'的返回消息:' + \
            self.checkin(rsa, lt, execu, cookie, user, message,passwd)
        requests.get(
            url='http://127.0.0.1:5700/send_group_msg?group_id={0}&message={1}'.format(group, result))
