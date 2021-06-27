from django.contrib.auth.models import User, Group
from rest_framework import viewsets,permissions,generics
from drf_multiple_model.views import ObjectMultipleModelAPIView
from drf_multiple_model.pagination import MultipleModelLimitOffsetPagination
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
    def get_queryset(self):
        queryset = ProcessRaiseEvent.objects.filter(ProcessRaiser=self.request.user)
        return queryset
    serializer_class = ListProcessSerializer

class LimitPagination(MultipleModelLimitOffsetPagination):
    default_limit = 10

class ProcessDetail(ObjectMultipleModelAPIView):
    #查看流程的具体细节(必须是该请求的所历环节才可查看)，参数为流程号
    permission_classes = [IsOwnerOrTargetOfRequest]
    pagination_class = LimitPagination
    def get_querylist(self):
        Pid=self.kwargs['pk']
        print(Pid)
        querylist = [
            {'queryset': ProcessRaiseEvent.objects.filter(id=Pid), 'serializer_class': ProcessDetailSerializerOfProcessRaiseEvent},
            {'queryset': ProcessHandleEvent.objects.filter(ProcessOriginalEvent=Pid), 'serializer_class': ProcessDetailSerializerOfProcessHandleEvent},
        ]
        return querylist
    # def get_queryset(self):
    #     queryset = ProcessRaiseEvent.objects.filter(ProcessRaiser=self.request.user)
    #     return queryset
    # return queryset
    
    # serializer_class = ProcessDetailSerializer

class ListUnhandledProcess(generics.ListAPIView):
    #查看待办的所有流程，无参
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        qst = ProcessHandleEvent.objects.filter(ProcessHandler=self.request.user).filter(ProcessHandleStatus=2).values('ProcessOriginalEvent')
        ProcList=[]
        for q in qst:
            ProcList.append(q['ProcessOriginalEvent'])
        queryset=ProcessRaiseEvent.objects.filter(id__in=ProcList)
        return queryset
    serializer_class = ListUnhandledProcessSerializer

class HandleProcess(generics.UpdateAPIView):
    #处理流程，参数为流程号
    permission_classes = [permissions.IsAuthenticated]
