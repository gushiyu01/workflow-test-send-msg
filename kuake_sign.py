from datetime import datetime
import httpx
import json
import os


# 微信企业号消息推送
# 企业ID
# 创建应用的secret
# 创建应用的id

# corp_id = 'wwf6aea27e2d98b2d0'
# corp_secret = 'ujWgFTJoozit4uPZdLGrmWZgzrxGG7rJOkNY-bTXzHE'
# agent_id = '1000002'
    
corp_id = os.getenv("AGENT_ID")
corp_secret = os.getenv("SECRET")
agent_id = os.getenv("ID")
print(11111)
print(corp_id)
print(corp_secret)
print(agent_id)



# 获取access_token的url
token_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
# 发送消息的url
send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send'

steps = [
    {
"kps":"AAT4Mh%2BRrlWjv%2F93cjne%2FRhUo55JXDqlFITJk13SJzKoGgE9xF%2Fm4xhsd0q1UN51qeRj7Y5IEn0vPD2TLcOM3dXrbvhq1WMY7CyrCNM32tOgyA%3D%3D",
"sign":"AAQKX2OQwZJ%2Bfp7%2BRGFwFfoR2MRictrBs9GQTgDInprQ8anr6kuGCr0yMPVm3sKVbRs%3D",
"vcode":"1756777261986",
"tel":"13523511140"
},
{
"kps":"AARHgzNN8nLz%2FldvKznL862irujZ0NUR3D89yM7%2F%2FWJmhu1ErS8TKDJJrhU9y%2B5n7OWTHs5%2F%2By%2BehmdOmV0RhqKRpD4NmfteNtJdEUDOFiDqgNX9QwuWvfB24JY%2BlxNCxn8%3D",
"sign":"AARCRuziwgYxYKG%2F88ErLD04BtVhHtMygMZDavvuqCUtBSGIGSCV5CAbq2axUuj3JFU%3D",
"vcode":"1755250298810",
"tel":"19603717135"
}
]

# 夸克 13523511140
# kps = 'AAT4Mh%2BRrlWjv%2F93cjne%2FRhUo55JXDqlFITJk13SJzKoGgE9xF%2Fm4xhsd0q1UN51qeRj7Y5IEn0vPD2TLcOM3dXrbvhq1WMY7CyrCNM32tOgyA%3D%3D'
# sign = 'AAQKX2OQwZJ%2Bfp7%2BRGFwFfoR2MRictrBs9GQTgDInprQ8anr6kuGCr0yMPVm3sKVbRs%3D'
# vcode = '1756777261986'
# 19603717135
# kps = 'AARHgzNN8nLz%2FldvKznL862irujZ0NUR3D89yM7%2F%2FWJmhu1ErS8TKDJJrhU9y%2B5n7OWTHs5%2F%2By%2BehmdOmV0RhqKRpD4NmfteNtJdEUDOFiDqgNX9QwuWvfB24JY%2BlxNCxn8%3D'
# sign = 'AARCRuziwgYxYKG%2F88ErLD04BtVhHtMygMZDavvuqCUtBSGIGSCV5CAbq2axUuj3JFU%3D'
# vcode = '1755250298810'


def send_wx_msg(to_user, content):
    """
    发送微信消息
    :param to_user: 接收消息的微信id
    :param content: 消息内容
    :return: None
    """
    print(token_url + "?corpid=" + corp_id + "&corpsecret=" + corp_secret)
    res = httpx.get(token_url + "?corpid=" + corp_id + "&corpsecret=" + corp_secret)
    print(res.text)
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

    post = httpx.post(url=send_url + "?access_token=" + token, json=params).text
    return post


def query_balance():
    """
    查询抽奖余额
    """
    url = "https://coral2.quark.cn/currency/v1/queryBalance"
    querystring = {
        "moduleCode": "1f3563d38896438db994f118d4ff53cb",
        "kps": kps,
    }
    response = httpx.get(url=url, params=querystring)
    response.raise_for_status()
    print(response.json())


def human_unit(bytes_: int) -> str:
    """
    人类可读单位
    :param bytes_: 字节数
    :return: 返回 MB GB TB
    """
    units = ("MB", "GB", "TB", "PB")
    bytes_ = bytes_ / 1024 / 1024
    i = 0
    while bytes_ >= 1024:
        bytes_ /= 1024
        i += 1
    return f"{bytes_:.2f} {units[i]}"


def user_info(kps, sign, vcode):
    """
    获取用户信息
    :return: None
    """
    now = datetime.now()
    timestamp = now.timestamp()
    url = "https://drive-m.quark.cn/1/clouddrive/capacity/growth/info"
    querystring = {
        "pr": "ucpro",
        "fr": "android",
        "kps": kps,
        "sign": sign,
        "vcode": vcode,
    }
    response = httpx.get(url=url, params=querystring)
    response.raise_for_status()
    content = response.json()
    if content["code"] != 0:
        print(content["message"])
    else:
        data = content["data"]
        super_vip_exp_at = "未知"
        if not data.get('super_vip_exp_at', None) is None:
            super_vip_exp_at = datetime.fromtimestamp(
                data["super_vip_exp_at"] / 1000
            ).strftime("%Y-%m-%d %H:%M:%S")
        cap_sign = data["cap_sign"]
        notify_message = ""
        if cap_sign["sign_daily"]:
            notify_message += (f"今日已签到，获得容量: {human_unit(cap_sign['sign_daily_reward'])},"
                               f" 签到进度: {cap_sign['sign_progress']}\n")
        notify_message += (f"会员类型：{data['member_type']}, 过期时间：{super_vip_exp_at}, 总计容量："
                           f"{human_unit(data['total_capacity'])}, 使用容量：{human_unit(data['use_capacity'])}, "
                           f"使用百分比：{data['use_capacity'] / data['total_capacity'] * 100:.2f}%")
        msg = notify_message
    return msg

def checkin(kps, sign, vcode):
    """
    签到
    :return: None
    """
    now = datetime.now()
    timestamp = now.timestamp()
    url = "https://drive-m.quark.cn/1/clouddrive/capacity/growth/sign"
    querystring = {
        "pr": "ucpro",
        "fr": "android",
        "kps": kps,
        "sign": sign,
        "vcode": vcode,
    }
    # add headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; U; Android 10; zh-Hans-CN; FRL-AN00a Build/HUAWEIFRL-AN00a) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/123.0.6312.80 Quark/7.14.5.880 Mobile Safari/537.36",
        "sec-ch-ua-platform": "Android",
        "Accept": "*/*",
        "Origin": "https://b.quark.cn",
        "X-Requested-With": "com.quark.browser",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://b.quark.cn/",
        "Accept-Encoding": "gzip, deflate, br",
    }
    response = httpx.post(url=url, json={"sign_cyclic": True}, params=querystring, headers=headers)
    if response.status_code == 200:
        if response.json()["code"] != 0:
            print(response.json()["message"])
        else:
            msg = f"签到成功，获得容量: " + human_unit(response.json()['data']['sign_daily_reward'])
            
    else:
        msg = f"已经签到，请勿重复签到"

    return msg

if __name__ == "__main__":
    print(corp_id)
    print(corp_secret)
    print(agent_id)
    # 遍历 steps 进行多账号签到
    for step in steps:
        kps = step['kps']
        sign = step['sign']
        vcode = step['vcode']
	
        m0 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg = f"签到时间：{m0}\n"
        m1 = checkin(kps, sign, vcode)
        m2 = user_info(kps, sign, vcode)
        send_wx_msg("GuShiYu", msg + m1 + "\n" + m2)
        print(step['tel'] + "签到完成")
