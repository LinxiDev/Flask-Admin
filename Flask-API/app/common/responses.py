# 第三方库导入
# 用于返回JSON格式响应
from flask import jsonify

# 成功响应
def success(data=None, msg='操作成功'):
    return jsonify({'success': True,'msg': msg,'data': data}), 200
    
# 失败响应
def fail(code=400, msg='操作失败'):
    return jsonify({'success': False,'msg': msg}), code
# 分页响应
def page(rows,currentPage = 1,pageSize = 10, msg='操作成功'):
    total = len(rows)
    return jsonify({'success': True,'msg': msg,'data': {'total': total,'list': rows,'currentPage':currentPage,'pageSize':pageSize,}}), 200