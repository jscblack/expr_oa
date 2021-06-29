from rest_framework import serializers
from oa.models import *
from jsonschema  import  ValidationError, validate
import phonenumbers
class CustomUserAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUsers
        fields = [
            "PersonNo",
            "PersonLastName",
            "PersonFirstName",
        ]

class CustomUserDetailSerializerForGet(serializers.ModelSerializer):
    class Meta:
        model = CustomUsers
        exclude=[
            "password",
            "groups",
            "user_permissions",
        ]

class CustomUserDetailSerializerForPutForSelf(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUsers
        fields=[
            "password",
            "password_confirm",
            'PersonEmail',
            'PersonLastName',
            'PersonFirstName',
            'PersonGender',
            'PersonAge',
            'PersonPhone',
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

        def validate_PersonAge(self, value):
            if value<=0 or value>=200:
                raise serializers.ValidationError("年龄不合法")
            return value

        def validate_PersonPhone(self, value):
            try:
                z=phonenumbers.parse("+86"+value, None)
                if phonenumbers.is_valid_number(z):
                    return value
                else:
                    raise serializers.ValidationError("手机号不合法")
            except Exception as e:
                raise serializers.ValidationError("手机号不合法")
        def validate(self, attrs):
        # 传进来什么参数，就返回什么参数，一般情况下用attrs
            if attrs['password'] != attrs['password_confirm']:
                raise serializers.ValidationError("密码不一致")
            return attrs

        def update(self,instance,validated_data):
            serializers.valid()
            validated_data.pop('password_confirm',None)
            # user=CustomUsers.objects.get(pk=self.context['kwargs']['pk'])
            # user.set_password(validated_data.get('password',None))
            instance.set_password(validated_data.get('password',None))
            instance.PersonEmail=validated_data.get('PersonEmail',None)
            instance.PersonLastName=validated_data.get('PersonLastName',None)
            instance.PersonFirstName=validated_data.get('PersonFirstName',None)
            instance.PersonGender=validated_data.get('PersonGender',None)
            instance.PersonAge=validated_data.get('PersonAge',None)
            instance.PersonPhone=validated_data.get('PersonPhone',None)
            instance.save()
            return instance

class CustomUserDetailSerializerForPutForAdmin(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUsers
        fields=[
            "password",
            "password_confirm",
            'PersonEmail',
            'PersonLastName',
            'PersonFirstName',
            'PersonGender',
            'PersonAge',
            'PersonPhone',
            'PersonJob',
            'PersonDirectSuperior',
            'is_superuser',
            'is_staff',
            'is_active'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def validate_PersonAge(self, value):
        print("validate_PersonAge")
        if value<=0 or value>=200:
            raise serializers.ValidationError("年龄不合法")
        return value
    def validate_PersonPhone(self, value):
        try:
            z=phonenumbers.parse("+86"+value, None)
            if phonenumbers.is_valid_number(z):
                return value
            else:
                raise serializers.ValidationError("手机号不合法")
        except Exception as e:
            raise serializers.ValidationError("手机号不合法")

    def validate(self, attrs):
        print("validate")
        # 传进来什么参数，就返回什么参数，一般情况下用attrs
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("密码不一致")
        return attrs

    def update(self,instance,validated_data):
        print("updateupdate")
        validated_data.pop('password_confirm',None)
        # print(instace)
        instance.set_password(validated_data.get('password',None))
        instance.PersonEmail=validated_data.get('PersonEmail',None)
        instance.PersonLastName=validated_data.get('PersonLastName',None)
        instance.PersonFirstName=validated_data.get('PersonFirstName',None)
        instance.PersonGender=validated_data.get('PersonGender',None)
        instance.PersonAge=validated_data.get('PersonAge',None)
        instance.PersonPhone=validated_data.get('PersonPhone',None)
        instance.PersonJob=validated_data.get('PersonJob',None)
        instance.PersonDirectSuperior=validated_data.get('PersonDirectSuperior',None)
        instance.is_superuser=validated_data.get('is_superuser',None)
        instance.is_staff=validated_data.get('is_staff',None)
        instance.is_active=validated_data.get('is_active',None)
        instance.save()
        return instance

class CustomUserAddSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUsers
        fields = [
            "PersonNo",
            "password",
            "password_confirm",
            'PersonEmail',
            'PersonLastName',
            'PersonFirstName',
            'PersonGender',
            'PersonAge',
            'PersonPhone',
            'PersonJob',
            'PersonDirectSuperior',
            'is_superuser',
            'is_staff',
            'is_active'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

        
    def validate_PersonAge(self, value):
        if value<=0 or value>=200:
            raise serializers.ValidationError("年龄不合法")
        return value
    def validate_PersonPhone(self, value):
        try:
            z=phonenumbers.parse("+86"+value, None)
            if phonenumbers.is_valid_number(z):
                return value
            else:
                raise serializers.ValidationError("手机号不合法")
        except Exception as e:
            raise serializers.ValidationError("手机号不合法")
    def validate(self, attrs):
    # 传进来什么参数，就返回什么参数，一般情况下用attrs
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("密码不一致")
        return attrs

    def create(self,validated_data):
        validated_data.pop('password_confirm',None)
        print(validated_data)
        user = CustomUsers.objects.create_user(**validated_data)
        return user
    
class CreateProcessSerializer(serializers.ModelSerializer):
    CreateProcessSteps = serializers.JSONField(write_only=True)
    #CreateProcessSteps = serializers.CharField(max_length=2048)
    class Meta:
        model = ProcessRaiseEvent
        fields = [
            'ProcessRaiseTitle',
            'ProcessRaiseInfo',
            'CreateProcessSteps'
        ]
        extra_kwargs = {
            'CreateProcessSteps': {'write_only':True, 'required': True}
        }

    def validate_ProcessRaiseInfo(self, value):
        schema  =  {
            "type":"object",
            "properties":{
                "reqInfo" : {"type" :"string"}
            },
            "required" : ["reqInfo"]
        }
        try:
            validate(value, schema)
        except ValidationError as e:
            raise serializers.ValidationError("请求参数不合法")
        else:
            return value


    def validate_CreateProcessSteps(self, value):
        schema  =  {
            "type":"object",
            "properties":{
                "reqRev" : {
                    "type" :"array",
                    "items" : {
                        "type": "integer"
                    },
                    "minItems": 1,
                    "uniqueItems": True
                },
            },
            "required" : ["reqRev"]
        }
        try:
            validate(value, schema)
            ProcessSteps=value['reqRev']
            print(ProcessSteps)
            if self.context['request'].user.PersonNo in ProcessSteps:
                raise serializers.ValidationError("流转目标不可以为自己")
            res=CustomUsers.objects.filter(PersonNo__in=ProcessSteps)
            res_count=len(res)
            print(res_count)
            print(len(ProcessSteps))
            if res_count!=len(ProcessSteps):
                raise serializers.ValidationError("流转目标必须为已存在的用户")
        except ValidationError as e:
            raise serializers.ValidationError("请求参数不合法")
        else:
            return value

    def create(self,validated_data):
        ProcessSteps=validated_data.pop('CreateProcessSteps',None)
        #handle
        ProcessSteps=ProcessSteps['reqRev']#array
        print(ProcessSteps)
        processRaiseEvent = ProcessRaiseEvent.objects.create(
            ProcessRaiser=self.context['request'].user,
            **validated_data
            )
        for i in range(len(ProcessSteps)):
            #当前级处理者为ProcessSteps[i] 当前级为i
            ProcessHandleEvent.objects.create(
                ProcessOriginalEvent=processRaiseEvent,
                ProcessHandleLevel=(i+1),
                ProcessHandleStatus=(2 if i == 0 else 1),
                ProcessHandler=CustomUsers.objects.filter(PersonNo=ProcessSteps[i])[0]
            )
        return processRaiseEvent

class ListProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessRaiseEvent
        fields = [
            'id',
            'ProcessRaiser',
            'ProcessRaiseTime',
            'ProcessRaiseInfo',
            'ProcessRaiseStatus',
        ]

class ProcessDetailSerializerOfProcessRaiseEvent(serializers.ModelSerializer):
    class Meta:
        model = ProcessRaiseEvent
        fields = [
            'id',
            'ProcessRaiseTitle',
            'ProcessRaiser',
            'ProcessRaiseTime',
            'ProcessRaiseInfo',
            'ProcessRaiseStatus',
        ]

class ProcessDetailSerializerOfProcessHandleEvent(serializers.ModelSerializer):
    class Meta:
        model = ProcessHandleEvent
        fields = [
            'ProcessHandleLevel',
            'ProcessHandleTime',
            'ProcessHandleStatus',
            'ProcessHandler',
            'ProcessHandleInfo',
            'ProcessHandleResult',
        ]

class ListUnhandledProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessRaiseEvent
        fields = [
            'id',
            'ProcessRaiseTitle',
            'ProcessRaiser',
            'ProcessRaiseTime',
            'ProcessRaiseStatus',
        ]

class HandleProcessSerializerForGet(serializers.ModelSerializer):
    lookup_field = 'ProcessOriginalEvent'
    ProcessOriginalEventTitle = serializers.CharField(source='ProcessOriginalEvent.ProcessRaiseTitle')
    class Meta:
        model = ProcessHandleEvent
        fields=[
            'ProcessOriginalEvent',
            'ProcessOriginalEventTitle',
            "ProcessHandler",
            "ProcessHandleLevel",
            "ProcessHandleInfo",
            "ProcessHandleResult",
            "ProcessHandleStatus",
        ]

class HandleProcessSerializerForPut(serializers.ModelSerializer):
    lookup_field = 'ProcessOriginalEvent'
    class Meta:
        model = ProcessHandleEvent
        exclude=[
            "id",
            'ProcessHandleLevel',
            'ProcessHandleTime',
            'ProcessHandleStatus',
            'ProcessOriginalEvent',
            'ProcessHandler',
        ]

    def validate_ProcessHandleInfo(self, value):
        schema  =  {
            "type":"object",
            "properties":{
                "hdlInfo" : {"type" :"string"}
            },
            "required" : ["hdlInfo"]
        }
        try:
            validate(value, schema)
        except ValidationError as e:
            raise serializers.ValidationError("请求参数不合法")
        else:
            return value

    def validate_ProcessHandleResult(self, value):
        if value==1 or value==2 or value==3:
            return value
        else:
             raise serializers.ValidationError("请求参数不合法")

    def update(self,instance,validated_data):
        instance.ProcessHandleInfo = validated_data.get('ProcessHandleInfo',None)
        instance.ProcessHandleResult = validated_data.get('ProcessHandleResult',None)
        instance.ProcessHandleStatus = 3
        instance.save()
        #注意如果当前级为1则将流程设为2，第一步判断
        #此处涉及几点 如果res为1 accepted则判断是否有下一级，如有下一级则流转入下一级（当前级的status更新为3，下一级status更新为2）
        #如无下一级则直接将流程终止，设为3
        #如为 2 rejected 则直接终止流程设为4
        #如为 3 返回则将流转返回至前一级，此处还涉及一点就是如当前级为第一级则将raise的状态设为5需要修改
        #给出意见后均将本级设为3
        processRaiseEvent = ProcessRaiseEvent.objects.get(pk=instance.ProcessOriginalEvent.id)
        if instance.ProcessHandleLevel == 1:
            processRaiseEvent.ProcessRaiseStatus=2
        if instance.ProcessHandleResult == 1:
            Steps_count=len(ProcessHandleEvent.objects.filter(ProcessOriginalEvent=instance.ProcessOriginalEvent.id))
            if Steps_count == instance.ProcessHandleLevel:
                processRaiseEvent.ProcessRaiseStatus=3
            else:
                nextProcessHandleEvent = ProcessHandleEvent.objects.get(ProcessOriginalEvent=instance.ProcessOriginalEvent.id,ProcessHandleLevel=(instance.ProcessHandleLevel+1))
                nextProcessHandleEvent.ProcessHandleStatus = 2
                nextProcessHandleEvent.save()
        elif instance.ProcessHandleResult == 2:
            processRaiseEvent.ProcessRaiseStatus=4
        else:
            if instance.ProcessHandleLevel ==1:
                #流转回初始者
                processRaiseEvent.ProcessRaiseStatus=5
            else:
                #流转回前一级
                prevProcessHandleEvent = ProcessHandleEvent.objects.get(ProcessOriginalEvent=instance.ProcessOriginalEvent.id,ProcessHandleLevel=(instance.ProcessHandleLevel-1))
                prevProcessHandleEvent.ProcessHandleStatus = 2
                prevProcessHandleEvent.save()
        processRaiseEvent.save()
        return instance

class ModifyProcessRaiseEventSerializerForPut(serializers.ModelSerializer):
    class Meta:
        model = ProcessRaiseEvent
        fields=[
            "ProcessRaiseTitle",
            "ProcessRaiseInfo",
        ]
    
    def validate_ProcessRaiseInfo(self, value):
        schema  =  {
            "type":"object",
            "properties":{
                "reqInfo" : {"type" :"string"}
            },
            "required" : ["reqInfo"]
        }
        try:
            validate(value, schema)
        except ValidationError as e:
            raise serializers.ValidationError("请求参数不合法")
        else:
            return value
    
    def update(self,instance,validated_data):
        instance.ProcessRaiseTitle=validated_data.get('ProcessRaiseTitle',None)
        instance.ProcessRaiseInfo=validated_data.get('ProcessRaiseInfo',None)
        instance.ProcessRaiseStatus=1
        instance.save()
        nextProcessHandleEvent = ProcessHandleEvent.objects.get(ProcessOriginalEvent=instance.id,ProcessHandleLevel=1)
        nextProcessHandleEvent.ProcessHandleStatus = 2
        nextProcessHandleEvent.save()
        return instance

class ModifyProcessRaiseEventSerializerForGet(serializers.ModelSerializer):
    class Meta:
        model = ProcessRaiseEvent
        fields=[
            "id",
            "ProcessRaiseTitle",
            "ProcessRaiser",
            "ProcessRaiseTime",
            "ProcessRaiseInfo",
            "ProcessRaiseStatus",
        ]

class CreateNoticeSerializer(serializers.ModelSerializer):
    CreateNoticeReceivers = serializers.JSONField(write_only=True,default={"ntcRev": []})
    NoticeNeedToRelay=serializers.BooleanField(write_only=True)
    NoticeForAllFellow = serializers.BooleanField(write_only=True)
    #CreateProcessReceivers = serializers.CharField(max_length=2048)
    class Meta:
        model = NoticeRaiseEvent
        fields = [
            'NoticeRaiseTitle',
            'NoticeRaiseInfo',
            'NoticeForAllFellow',
            'CreateNoticeReceivers',
            'NoticeNeedToRelay'
        ]
        extra_kwargs = {
            'CreateNoticeReceivers': {'write_only':True, 'required': False,'default':{"ntcRev": []}},
            'NoticeNeedToRelay': {'write_only':True, 'required': True},
            'NoticeForAllFellow': {'write_only':True, 'required': False},
        }

    def validate_NoticeRaiseInfo(self, value):
        schema  =  {
            "type":"object",
            "properties":{
                "ntcInfo" : {"type" :"string"}
            },
            "required" : ["ntcInfo"]
        }
        try:
            validate(value, schema)
        except ValidationError as e:
            raise serializers.ValidationError("请求参数不合法")
        else:
            return value

    def validate_CreateNoticeReceivers(self, value):
        if value==None:
            return value
        schema  =  {
            "type":"object",
            "properties":{
                "ntcRev" : {
                    "type" :"array",
                    "items" : {
                        "type": "integer"
                    },
                    "minItems": 1,
                    "uniqueItems": True
                },
            },
            "required" : ["ntcRev"]
        }
        try:
            validate(value, schema)
            NoticeReceivers=value['ntcRev']
            print(NoticeReceivers)
            if self.context['request'].user.PersonNo in NoticeReceivers:
                raise serializers.ValidationError("通知目标不可以为自己")
            qst=CustomUsers.objects.filter(PersonNo__in=NoticeReceivers)
            for q in qst:
                if q.PersonDirectSuperior!=self.context['request'].user:
                    raise serializers.ValidationError("通知目标必须为直接下级")
        except ValidationError as e:
            raise serializers.ValidationError("请求参数不合法")
        else:
            return value

    def validate(self, attrs):
        if attrs['NoticeForAllFellow']==None and attrs['NoticeReceivers']==None:
            raise serializers.ValidationError("通知目标不可以为空")
        return attrs

    def create(self,validated_data):
        NoticeReceivers=validated_data.pop('CreateNoticeReceivers',None)
        noticeNeedToRelay=validated_data.pop('NoticeNeedToRelay',None)
        NoticeForAllFellow=validated_data.pop('NoticeForAllFellow',None)
        #handle
        print("debug")
        if NoticeReceivers!=None:
            NoticeReceivers=NoticeReceivers['ntcRev']#array
        #print(NoticeReceivers)
        print(validated_data)
        noticeRaiseEvent = NoticeRaiseEvent.objects.create(
            NoticeRaiser=self.context['request'].user,
            **validated_data
            )
        if NoticeForAllFellow==1:
            qst=CustomUsers.objects.filter(PersonDirectSuperior=self.context['request'].user)
            # ProcList=[]
            for q in qst:
                if q.PersonNo!=self.context['request'].user.PersonNo:
                    NoticeReceiveEvent.objects.create(
                    NoticeOriginalEvent=noticeRaiseEvent,
                    NoticeReceiver=q,
                    NeedToRelay=noticeNeedToRelay & CustomUsers.objects.filter(PersonDirectSuperior=q).exists(),#有下属才行
                    )
                    # ProcList.append(q['PersonNo'])
        else:            
            for i in range(len(NoticeReceivers)):
                #当前级处理者为NoticeReceivers[i] 当前级为i
                #print(CustomUsers.objects.filter(PersonNo=NoticeReceivers[i]))
                #当前级处理者为NoticeReceivers[i] 当前级为i
                NoticeReceiveEvent.objects.create(
                    NoticeOriginalEvent=noticeRaiseEvent,
                    NoticeReceiver=CustomUsers.objects.filter(PersonNo=NoticeReceivers[i])[0],
                    NeedToRelay=noticeNeedToRelay & CustomUsers.objects.filter(PersonDirectSuperior=NoticeReceivers[i]).exists()#有下属才行
                )
        noticeNeedToRelay=validated_data.pop('NoticeNeedToRelay',None)
        
        return noticeRaiseEvent

class ModifyNoticeDetailSerializerForPut(serializers.ModelSerializer):
    class Meta:
        model = NoticeRaiseEvent
        fields=[
            "NoticeRaiseTitle",
            "NoticeRaiseInfo",
        ]
    def validate_NoticeRaiseInfo(self, value):
        schema  =  {
            "type":"object",
            "properties":{
                "ntcInfo" : {"type" :"string"}
            },
            "required" : ["ntcInfo"]
        }
        try:
            validate(value, schema)
        except ValidationError as e:
            raise serializers.ValidationError("请求参数不合法")
        else:
            return value
    
    def update(self,instance,validated_data):
        instance.NoticeRaiseTitle=validated_data.get('NoticeRaiseTitle',None)
        instance.NoticeRaiseInfo=validated_data.get('NoticeRaiseInfo',None)
        instance.save()
        # NoticeOriginalEvent=instance.id 全部 NoticeRead=0
        NoticeReceiveEvent.objects.filter(NoticeOriginalEvent=instance.id).update(NoticeRead=0)
        return instance

class ModifyNoticeDetailSerializerForGet(serializers.ModelSerializer):
    class Meta:
        model = NoticeRaiseEvent
        fields=[
            "id",
            "NoticeRaiseTitle",
            "NoticeRaiser",
            "NoticeRaiseTime",
            "NoticeRaiseInfo",
        ]

class NoticeDetailSerializerForPutForReceiver(serializers.ModelSerializer):
    NoticeRead=serializers.BooleanField(write_only=True) #是否已读
    class Meta:
        model = NoticeRaiseEvent
        fields=[
            "NoticeRead",
        ]
        extra_kwargs = {
            'NoticeRead': {'write_only':True, 'required': True},
        }

    def validate_NoticeRead(self, value):
        if value!=True:
            raise serializers.ValidationError("请勾选已读")
        else:
            return value
    
    def update(self,instance,validated_data):
        ist=NoticeReceiveEvent.objects.get(NoticeOriginalEvent=instance.id, NoticeReceiver=self.context['request'].user)
        ist.NoticeRead=True
        ist.save()
        return instance

class NoticeDetailSerializerForPutForRelayer(serializers.ModelSerializer):
    NoticeRelay=serializers.BooleanField(write_only=True) #是否转发
    NoticeReceivers = serializers.JSONField(write_only=True,default={"ntcRev": []})
    NoticeForAllFellow = serializers.BooleanField(write_only=True)
    NoticeNeedToRelay=serializers.BooleanField(write_only=True)
    class Meta:
        model = NoticeRaiseEvent
        fields=[
            "NoticeRelay", #是否完成转发
            "NoticeForAllFellow",#全部
            "NoticeReceivers", #接收者
            "NoticeNeedToRelay",  #下一级是否需要转发
        ]
        extra_kwargs = {
            'NoticeRelay': {'write_only':True, 'required': True},
            'NoticeForAllFellow': {'write_only':True, 'required': False},
            'NoticeReceivers': {'write_only':True, 'required': False,'default':{"ntcRev": []}},
            'NoticeNeedToRelay': {'write_only':True, 'required': True}
        }
    
    def validate_NoticeRelay(self, value):
        if value!=True:
            raise serializers.ValidationError("请勾选转发")
        else:
            return value

    def validate_NoticeReceivers(self, value):
        if value==None:
            return value
        schema  =  {
            "type":"object",
            "properties":{
                "ntcRev" : {
                    "type" :"array",
                    "items" : {
                        "type": "integer"
                    },
                    "minItems": 1,
                    "uniqueItems": True
                },
            },
            "required" : ["ntcRev"]
        }
        try:
            validate(value, schema)
            NoticeReceivers=value['ntcRev']
            print(NoticeReceivers)
            if self.context['request'].user.PersonNo in NoticeReceivers:
                raise serializers.ValidationError("通知目标不可以为自己")
            qst=CustomUsers.objects.filter(PersonNo__in=NoticeReceivers)
            for q in qst:
                if q.PersonDirectSuperior!=self.context['request'].user:
                    raise serializers.ValidationError("通知目标必须为直接下级")
        except ValidationError as e:
            raise serializers.ValidationError("请求参数不合法")
        else:
            return value

    def validate(self, attrs):
        if attrs['NoticeForAllFellow']==None and attrs['NoticeReceivers']==None:
            raise serializers.ValidationError("通知目标不可以为空")
        return attrs

    def update(self,instance,validated_data):
        ist=NoticeReceiveEvent.objects.get(NoticeOriginalEvent=instance.id, NoticeReceiver=self.context['request'].user)
        ist.NoticeRead=True
        ist.NoticeRelay=validated_data.get('NoticeRelay',None)
        ist.save()
        noticeNeedToRelay=validated_data.pop('NoticeNeedToRelay',None)
        if validated_data.get('NoticeForAllFellow',None)==1:
            qst=CustomUsers.objects.filter(PersonDirectSuperior=self.context['request'].user)
            # ProcList=[]
            for q in qst:
                if q.PersonNo!=self.context['request'].user.PersonNo:
                    NoticeReceiveEvent.objects.create(
                    NoticeOriginalEvent=instance,
                    NoticeReceiver=q,
                    NeedToRelay=noticeNeedToRelay & CustomUsers.objects.filter(PersonDirectSuperior=q).exists(),#有下属才行
                    )
                    # ProcList.append(q['PersonNo'])
        else:
            NoticeReceivers=validated_data.pop('NoticeReceivers',None)
            NoticeReceivers=NoticeReceivers['ntcRev']
            
            for i in range(len(NoticeReceivers)):
                #当前级处理者为NoticeReceivers[i] 当前级为i
                #print(CustomUsers.objects.filter(PersonNo=NoticeReceivers[i]))
                NoticeReceiveEvent.objects.create(
                    NoticeOriginalEvent=instance,
                    NoticeReceiver=CustomUsers.objects.filter(PersonNo=NoticeReceivers[i])[0],
                    NeedToRelay=noticeNeedToRelay & CustomUsers.objects.filter(PersonDirectSuperior=NoticeReceivers[i]).exists(),#有下属才行
                )
        return instance

class NoticeDetailSerializerForGet(serializers.ModelSerializer):
    class Meta:
        model = NoticeRaiseEvent
        fields=[
            "id",
            "NoticeRaiseTitle",
            "NoticeRaiser",
            "NoticeRaiseTime",
            "NoticeRaiseInfo",
        ]

class ListUnreadNoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoticeRaiseEvent
        fields = [
            'id',
            'NoticeRaiseTitle',
            'NoticeRaiser',
            'NoticeRaiseTime',
        ]

class NoticeStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUsers
        fields = [
            'PersonNo',
            'PersonLastName',
            'PersonFirstName',
            'PersonPhone',
        ]

#{"reqInfo": "测试"}
#{"reqRev": [2019214290,2019214288]}

#{"hdlInfo": "测试"}

#{"ntcInfo": "测试通知"}
#{"ntcRev": [2019214245,2019214288]}