import re
import time
import requests
from config.config import config
from requests_toolbelt  import MultipartEncoder

# 全局请求
ss = requests.session()

domain = config['image_url']
payload = config['image_account']

# 登陆账号(获取用户信息)
def login():
    result = ss.post(domain)
    auth_token = re.findall('auth_token = "(.*?)"',result.text)[0]
    PHP_SESSID = re.findall('PHPSESSID=(.*?);',result.headers['set-cookie'])[0]
    payload["auth_token"] = auth_token
    result = ss.post(domain+"/login",data = payload,allow_redirects=False)
    KEEP_LOGIN = re.findall('KEEP_LOGIN=(.*?);',result.headers['set-cookie'])[0]
    ss.headers = {"cookie":f'PHPSESSID={PHP_SESSID}; KEEP_LOGIN={KEEP_LOGIN}'}
    result = ss.get(domain).text
    if "注销" in result:
        tips = re.findall('phone-hide">(.*?)</span>',result)[0]
        print(f"[路过图床-Login] 登陆成功:{tips}")
        return auth_token
    else:
        tips = re.findall('expirable("(.*?)"',result)[0]
        print(f"[路过图床-Login] 登陆失败:{tips}")
        return False

# 获取图床所有图片
def image_list():
    auth_token = login()
    result = ss.get(domain+f"/{payload['login-subject']}").text
    image_count = re.findall('image-count">(.*?)</b>',result)[0]
    image_list = re.findall('<img src="https://(.*?)" alt="(.*?).png"',result)
    image_lists = []
    for image_url,image_id in image_list:
        # print(f"[路过图床-IMG({image_id})] https://{image_url}")
        image_lists.append({"image_id":image_id,"image_url":"https://"+image_url})
    return {"code":200,"msg":"查询成功!","list":image_lists,"image_count":image_count}

# 图床上传图片接口
def image_upload(file):
    auth_token = login()
    t = str(int(time.time()*1000))
    file_payload = {"source": (f'{t}.png', file, 'image/png'),"type": "file","action": "upload","timestamp": t,"auth_token": auth_token,"nsfw": "0"}
    m = MultipartEncoder(fields=file_payload)
    ss.headers['Content-Type'] = m.content_type
    result = ss.post(domain+"/json", data=m).json()
    if result['status_code'] == 200:
        print(f"[路过图床-Upload] 上传成功: 图片地址({result['image']['url']})")
        return {"code":200,"msg":"上传成功!","image_url":result['image']['url']}
    else:
        print(f"[路过图床-Upload] 上传失败:{result['error']['message']}")
        return {"code":400,"msg":f"上传失败,{result['error']['message']}!"}

# 图床删除图片接口
def image_delete(image_id):
    auth_token = login()
    data = {"auth_token":auth_token,"action":"delete","single":"true","delete":"image","deleting[id]":image_id}
    # 发送POST请求
    result = ss.post(domain+"/json", data=data).json()
    if result['status_code'] == 200:
        print(f"[路过图床-Delete] 删除成功:{result['request']['deleting']['id']}")
        return {"code":200,"msg":"删除成功!","image_id":result['request']['deleting']['id']}
    else:
        print(f"[路过图床-Delete] 删除失败:{result['error']['message']}")
        return {"code":400,"msg":f"删除失败,{result['error']['message']}!"}