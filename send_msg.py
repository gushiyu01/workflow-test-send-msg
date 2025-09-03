import requests
import json
# 微信企业号消息推送
# 企业ID
corp_id = 'wwf6aea27e2d98b2d0'
# 创建应用的secret
corp_secret = 'ujWgFTJoozit4uPZdLGrmWZgzrxGG7rJOkNY-bTXzHE'
# 创建应用的id
agent_id = '1000002'
# 获取access_token的url
token_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
# 发送消息的url
send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send'


def send_wx_msg(to_user, content):
    res = requests.get(token_url + "?corpid=" + corp_id + "&corpsecret=" + corp_secret)

    json_loads = json.loads(res.text)
    token = json_loads.get('access_token')

    params = {
        'touser': to_user,
        'msgtype': 'text',
        'agentid': agent_id,
        'text': {
            'content': content
        }
    }

    post = requests.post(url=send_url + "?access_token=" + token, json=params).text
    return post


print(send_wx_msg('GuShiYu', '去抢茅台啊，都是钱，签到！'))
print(send_wx_msg('TianTian', '田大妞，抢茅台了'))
print(send_wx_msg('HuaHua', '田二妞，抢茅台了'))
