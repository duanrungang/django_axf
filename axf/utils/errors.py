OK = 200
SUCCESS = {'code': 200, 'msg': '请求成功'}

ERR_MSG_INVALID = {'code': 400, 'msg': '请求失败'}

# 用户模块
USER_REGISTER_NAME_EXISTS = {'code': 1001, 'msg': '注册账号已存在，请更换账号'}
USER_REGISTER_PASSWORD_INVALID = {'code': 1002, 'msg': '注册密码和确认密码不一致'}
USER_REGISTER_EMAIL_INVALID = {'code': 1003, 'msg': '邮箱已存在，请更换邮箱'}
USER_REGISTER_PARAMS_INVALID = {'code': 1004, 'msg': '请求参数校验失败'}