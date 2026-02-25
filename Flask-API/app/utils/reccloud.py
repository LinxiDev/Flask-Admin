# 录咖WEB-UI  https://reccloud.cn/speech-to-text-online
# 录咖WEB-UI  https://reccloud.cn/text-to-speech-online
import json
import time
import hmac
import base64
import hashlib
import requests
from datetime import datetime

# 全局请求
ss = requests.session()

# 拼接Authorization认证字段
def authorization(s, f, d):
    return "OSS " + s + ":" + compute_signature(f, d)

# 签名算法Sign
def compute_signature(f, d):
    hmac_sha1 = hmac.new(f.encode('utf-8'), d.encode('utf-8'), hashlib.sha1)
    return base64.b64encode(hmac_sha1.digest()).decode('utf-8')

# 将当前时间格式化为指定格式
def get_date():
    current_time = datetime.utcnow()
    date = current_time.strftime("%a, %d %b %Y %H:%M:%S GMT")
    return date

# 组装请求头
def get_headers(sign,date,token,path):
    headers = {
        'Origin': 'https://reccloud.cn',
        'Referer': 'https://reccloud.cn/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        'authorization': sign,
        'x-oss-callback': 'eyJjYWxsYmFja1VybCI6Imh0dHBzOi8vYXcuYW9zY2RuLmNvbS90ZWNoL2NhbGxiYWNrcy9hbGl5dW4vb3NzIiwiY2FsbGJhY2tCb2R5IjoiYnVja2V0PSR7YnVja2V0fSZvYmplY3Q9JHtvYmplY3R9JnNpemU9JHtzaXplfSZtaW1lVHlwZT0ke21pbWVUeXBlfSZpbWFnZUluZm8uaGVpZ2h0PSR7aW1hZ2VJbmZvLmhlaWdodH0maW1hZ2VJbmZvLndpZHRoPSR7aW1hZ2VJbmZvLndpZHRofSZpbWFnZUluZm8uZm9ybWF0PSR7aW1hZ2VJbmZvLmZvcm1hdH0meDpmaWxlbmFtZT1hdWRpby5hYWMifQ==',
        'x-oss-date': date,
        'x-oss-security-token': token,
        'x-oss-user-agent': 'aliyun-sdk-js/6.9.0 Chrome 102.0.0.0 on Windows 10 64-bit',
    }
    d = f"""PUT\n\n\n{date}\nx-oss-callback:{headers['x-oss-callback']}\nx-oss-date:{date}\nx-oss-security-token:{token}\nx-oss-user-agent:{headers['x-oss-user-agent']}\n{path}"""
    return headers,d

# 获取上传文件权限的任务ID-预上传
def get_taskid(file_path):
    url = "https://aw.aoscdn.com/tech/authorizations/oss"
    data = {
        "task_type": "201",
        "filenames[]": file_path
    }
    result = ss.post(url, data=data).json()
    bucket = result['data']['bucket']
    endpoint = result['data']['endpoint']
    objects = result['data']['objects'][file_path]
    taskurl = f"https://{bucket}.{endpoint}/{objects}"
    token = result['data']['credential']['security_token']
    id = result['data']['credential']['access_key_id']
    secret = result['data']['credential']['access_key_secret']
    path = f"/wxtechsz/{objects}"
    return taskurl,path,id,secret,token

# 上传文件
def upload(file_path,file):
    taskurl,path,id,secret,token = get_taskid(file_path)
    date = get_date()
    headers,d = get_headers(None,date,token,path)
    sign = authorization(id, secret, d)
    headers,d = get_headers(sign,date,token,path)
    # 以二进制模式打开文件并读取内容
    # with open(file_path, 'rb') as file:
    #     data = file
    data = file
    result = ss.put(taskurl,headers=headers, data=data).json()
    ossurl = result['data']['uri']
    resource_id = result['data']['resource_id']
    return ossurl

# 语音识别程序
def API(file_path,ossurl):
    headers = {"X-API-KEY":"wxpgzsnks6hfzxmf3"}
    data = {"content_type": "0","filename": file_path,"language": "","return_type": "1","type": "4","url": ossurl,}
    result = ss.post("https://aw.aoscdn.com/app/reccloud/v2/open/ai/recognition",headers=headers,data=data).json()
    taskid = result['data']
    while True:
        result = ss.get(f" https://aw.aoscdn.com/app/reccloud/v2/open/ai/recognition/{taskid}",headers=headers).json()
        if result['data']['state'] == 1 :
            result = result['data']['result']
            testlist = []
            for t in result:
                testlist.append(t['text'].replace(".","").replace(",",""))
            print(f"[语音识别] 识别成功:{testlist}")
            return {"code":200,"msg":"识别成功!","text":testlist}
        elif result['data']['state'] in [0,4]:
            print(f"[语音识别] 正在识别...",end='\r')
        else:
            print(f"[语音识别] 识别异常:{result}")
            return {"code":400,"msg":"识别异常!","text":None}

# ASR 语音识别接口(file 二进制文件数据)
def ASR(file,file_path="audio.aac"):
    ossurl = upload(file_path,file)
    return API(file_path,ossurl)


# TTS 语音合成接口(text 需要合成的文字)
def TTS(text,language="zh-CN"):
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    voives = ss.get("https://aw.aoscdn.com/app/reccloud/v2/open/ai/speech/language?gender=male").json()['data']['items']
    for v in voives:
        if v['language'] == language:
            voive = v['voice']
            break
    else:
        return {"code":400,"msg":"不支持语种或语种错误!"}
    data = {"language":"","title":f"reccloud-{formatted_time}","voice":voive,"text":text,"format":"mp3"}
    task_id = ss.post("https://aw.aoscdn.com/app/reccloud/v2/open/ai/speech",data=data).json()['data']['task_id']
    while True:
        result = ss.get(f"https://aw.aoscdn.com/app/reccloud/v2/open/ai/speech/{task_id}").json()
        if result['data']['state'] == 1:
            print("[语音合成] 转换成功: ",result['data']['file'])
            return {"code":200,"msg":"转换成功!","audio":result['data']['file']}
        elif result['data']['state'] in [0,2,4]:
            print("[语音合成] 正在合成...",end='\r')
        else:
            print("[语音合成] 转换失败,请重新尝试!",{result})
            return {"code":400,"msg":"转换失败,请重新尝试!"}
        
# OCR 文字识别接口(file 二进制文件数据)
def OCR(file):
    headers = {'Origin': 'https://cn.iloveocr.com','Referer': 'https://cn.iloveocr.com/','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
    info = ss.post("https://ocr.convertserver.com/php/ocrupload.php", headers=headers, files={'files': ('logo.png',file, 'image/png')}).json()
    if info['isSuccess']:
        for info in info['files']:
            params = {"jsoncallback2691": "","mstr": "","oldfile": info['name'],"ocrformat": "txt","lang[]": "eng","lang[]": "chi_sim","_": int(time.time()*1000)}
            text = ss.post("https://ocr.convertserver.com/php/apiocr.php", headers=headers, params=params).text
            if text:
                return {"code":200,"msg":"识别成功!","text":json.loads(text[1:-1])['text']}
            else:
                return {"code":400,"msg":"识别失败!","text":None}
    else:
        return {"code":400,"msg":"上传失败!","text":None}
    
