from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager): #自定义Manager管理器
    def _create_user(self,PersonNo,password,PersonEmail,PersonLastName,PersonFirstName,PersonGender,PersonAge,PersonPhone,PersonJob,PersonDirectSuperior,**kwargs):
        if not PersonNo:
            raise ValueError("请传入学号！")
        if not password:
            raise ValueError("请传入密码！")
        if not PersonEmail:
            raise ValueError("请传入邮箱地址！")
        if not PersonLastName:
            raise ValueError("请传入姓名！")
        if not PersonFirstName:
            raise ValueError("请传入姓名！")
        if not PersonGender:
            raise ValueError("请传入性别！")
        if not PersonAge:
            raise ValueError("请传入年龄！")
        if not PersonPhone:
            raise ValueError("请传入电话！")
        if not PersonJob:
            raise ValueError("请传入身份！")
        if not PersonDirectSuperior:
            raise ValueError("请传入直接上级！")
        user = self.model(PersonNo=PersonNo,PersonEmail=PersonEmail,PersonLastName=PersonLastName,PersonFirstName=PersonFirstName,PersonGender=PersonGender,PersonAge=PersonAge,PersonPhone=PersonPhone,PersonJob=PersonJob,PersonDirectSuperior=PersonDirectSuperior,**kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self,PersonNo,password,PersonEmail,PersonLastName,PersonFirstName,PersonGender,PersonAge,PersonPhone,PersonJob,PersonDirectSuperior,**kwargs): # 创建普通用户
        kwargs['is_superuser'] = False
        return self._create_user(PersonNo,password,PersonEmail,PersonLastName,PersonFirstName,PersonGender,PersonAge,PersonPhone,PersonJob,PersonDirectSuperior,**kwargs)

    def create_superuser(self,PersonNo,password,PersonEmail,PersonLastName,PersonFirstName,PersonGender,PersonAge,PersonPhone,PersonJob,PersonDirectSuperior,**kwargs): # 创建超级用户
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        return self._create_user(PersonNo,password,PersonEmail,PersonLastName,PersonFirstName,PersonGender,PersonAge,PersonPhone,PersonJob,PersonDirectSuperior,**kwargs)