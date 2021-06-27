from rest_framework import serializers
from oa.models import *
from jsonschema  import  ValidationError, validate

class CustomUserAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUsers
        fields = [
            "PersonNo",
            "PersonLastName",
            "PersonFirstName",
        ]

class CustomUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUsers
        exclude=[
            "password"
        ]

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
            'ProcessRaiser',
            'ProcessRaiseTime',
            'ProcessRaiseInfo',
            'ProcessRaiseStatus',
        ]

#{"reqInfo": "测试"}
#{"reqRev": [2019214290,2019214288]}