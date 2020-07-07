from django.shortcuts import render, redirect
from housekeeping.globalFunc import js_ok, js_error

# Create your views here.
from user.models import User


def login(request):
    """
    请求方式：POST
    传递参数：username&password
    返回类型：字符串：ok|error
    """
    # 判断是否是post请求
    if request.POST:
        # 获取用户信息
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        # 查询对应用户信息
        user = User.objects.get(username=username)
        # 判断密码正确性
        if password == user.password:
            # 登录成功
            # 存入session
            request.session['username'] = username
            # 响应到客户端
            return js_ok('ok')

        else:
            # 这是账号密码不对的时候
            return js_error('100', 'error')


def logout(request):
    request.session.flush()

    return js_ok('ok')


def register(request):
    """
    请求方式：POST
    传递值：username&password
    """
    if request.POST:
        # 获取参数
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        real_name = request.request.POST.get('real_name', None)
        sex = request.request.POST.get('sex', None)
        phone = request.POST.get('phone', None)
        company = request.request.POST.get('company', None)

        # 判断用户是否存在
        user = User.objects.filter(username=username)

        if len(user) > 0:
            return js_error('100', 'error')

        # 这是用户名可以使用的时候
        # 添加数据
        user = User()

        user.username = username
        user.password = password
        user.salt = password[0:6]
        user.real_name = real_name
        user.sex = sex
        user.phone = phone
        user.company = company

        user.save()

        return js_ok('ok')


def completeUserInfo(request):
    context = dict()
    try:
        # 从session获取账号
        account = request.session['username']
        # 找到账号
        this_accounts = User.objects.get(username=account)
        context['account'] = account
        context['real_name'] = this_accounts.real_name
        context['phone'] = this_accounts.phone
        context['sex'] = this_accounts.sex
    except:
        context['account'] = None
    if request.POST:
        # 获取修改填入的数据
        sex = request.POST.get('sex')
        real_name = request.POST.get('real_name')
        phone = request.POST.get('phone')
        account = request.session['username']

        if sex == "" and real_name == "" and phone == "":  # 如果三项都没有进行修改
            return js_error(502, '请至少修改一项')
        else:  # 如果进行操作，一次判断哪一个发生了改变，再依次update
            if (real_name != ""):  # 昵称如果不为空，更新昵称
                User.objects.filter(username=account).update(real_name=real_name)
            if (sex != ""):  # 性别不为空，更新性别
                User.objects.filter(username=account).update(sex=sex)
            if (phone != "" and len(phone) == 11):  # 电话不为空，更新电话
                User.objects.filter(username=account).update(phone=phone)
            if (phone != "" and len(phone) != 11):
                return js_error(502, '电话号码位数不对')
            this_accounts = User.objects.get(username=account)
            context['account'] = this_accounts.username
            context['name'] = this_accounts.real_name
            context['phone'] = this_accounts.phone
            return js_ok('修改成功')
    else:
        return js_error(401, '修改失败')


def changePassword(request):
    context = dict()
    try:
        # 从session获取账号
        account = request.session['username']
        # 找到账号
        this_accounts = User.objects.get(username=account)
        context['account'] = account
        context['real_name'] = this_accounts.real_name
        context['phone'] = this_accounts.phone
        context['sex'] = this_accounts.sex
    except:
        context['account'] = None
    if request.POST:
        oldPwd = request.POST.get('oldPwd')
        newPwd = request.POST.get('newPwd')
        newPwd1 = request.POST.get('newPwd1')
        # 从session获取账号
        account = request.session['username']
        # 遍历找到账号
        for i in range(1, User.objects.count() + 1):
            this_accounts = User.objects.get(username=account)
            if account == this_accounts.username:
                break
        if this_accounts.a_pwd == oldPwd:
            if newPwd == newPwd1:
                if newPwd != this_accounts.password:
                    User.objects.filter(username=account).update(password=str(newPwd))
                    return js_ok('修改成功')
                else:
                    js_error(502, '不能与原密码一致')
            else:
                js_error(502, '两次密码不一致')
        else:
            js_error(401, '原密码不对')



def forgetPassword(request):
    """
    忘记密码
    请求方式：POST
    传递：phone
    此方法先不做处理，仅仅演示即可
    """
    return js_ok('已发送找回密码短信，请注意查收')


def showUserInfo(request, userId):
    """
    家政公司查看用户信息
    请求方式：GET
    返回手机、性别、姓氏等信息
    """
    result = User.objects.get(userId=userId)

    context = dict()
    context['data'] = result

    return js_ok(context)