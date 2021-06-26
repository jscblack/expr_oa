from django.contrib.auth.models import User, Group
from rest_framework import viewsets,permissions,generics
from oa.serializers import *
from oa.models import *
from oa.permissions import *

# Create your views here.

class CustomUserAll(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUsers.objects.all()
    #对于所有人可以查看所有的用户列表
    serializer_class = CustomUserAllSerializer
    # serializer_class = CustomUserSerializer
    
class CustomUserDetail(generics.RetrieveAPIView):
    #users/pk
    permission_classes = [IsSuperiorOfRequestOrAdmin]
    #permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        print(self.kwargs['pk'])
        queryset = CustomUsers.objects.filter(PersonNo=self.kwargs['pk'])
        return queryset
    # 只可以查看自己直接下属或间接下属的详细信息
    # def get_serializer_class(self):
    #     if self.request.method == "PUT":
    #         return CustomUserDetailUpdateSerializer
    #     return CustomUserDetailSerializer
    serializer_class = CustomUserDetailSerializer

class CustomUserAdd(generics.CreateAPIView):
    #只有管理员可创建用户
    permission_classes = [permissions.IsAdminUser]
    serializer_class = CustomUserAddSerializer

class CreateProcess(generics.CreateAPIView):
    #所有用户均可创建流程，无参
    permission_classes = [permissions.IsAuthenticated]
    #queryset=
    serializer_class = CreateProcessSerializer

class ListProcess(generics.ListAPIView):
    #查看自己发起的所有流程，无参
    permission_classes = [permissions.IsAuthenticated]
    #queryset = 
    #serializer_class = 

class ProcessDetail(generics.RetrieveAPIView):
    #查看流程的具体细节(必须是该请求的所历环节才可查看)，参数为流程号
    permission_classes = [permissions.IsAuthenticated]
    #queryset=
    #serializer_class = 

class ListUnhandledProcess(generics.ListAPIView):
    #查看待办的所有流程，无参
    permission_classes = [permissions.IsAuthenticated]
    #queryset=
    #serializer_class = 

class HandleProcess(generics.UpdateAPIView):
    #处理流程，参数为流程号
    permission_classes = [permissions.IsAuthenticated]


