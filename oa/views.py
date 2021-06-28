from django.contrib.auth.models import User, Group
from rest_framework import viewsets,permissions,generics,filters
from drf_multiple_model.views import ObjectMultipleModelAPIView
from drf_multiple_model.pagination import MultipleModelLimitOffsetPagination
from oa.serializers import *
from oa.models import *
from oa.permissions import *

# Create your views here.

class CustomUserAll(generics.ListAPIView):
    # 对于所有人可以查看所有的用户列表
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUsers.objects.all()
    serializer_class = CustomUserAllSerializer
    # serializer_class = CustomUserSerializer

class CustomUserFilter(generics.ListAPIView):
    # 仅可查看自己直接下属或间接下属的信息并筛选
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        AuthList=[self.request.user.PersonNo]
        flag=1
        while flag==1:
            flag=0
            qst=CustomUsers.objects.filter(PersonDirectSuperior__in=AuthList)
            for q in qst:
                if q.PersonNo not in AuthList:
                    flag=1
                    AuthList.append(q.PersonNo)
        queryset = CustomUsers.objects.filter(PersonNo__in=AuthList)
        return queryset
    serializer_class = CustomUserDetailSerializerForGet
    filter_backends = [filters.SearchFilter]
    search_fields = ['=PersonEmail', 'PersonLastName','PersonFirstName','=PersonGender','=PersonAge','=PersonPhone','=PersonJob','=PersonDirectSuperior__PersonNo']

class CustomUserDetail(generics.RetrieveUpdateAPIView):
    # 只可以查看自己直接下属或间接下属的详细信息
    permission_classes = [IsSuperiorOfRequestOrAdmin]

    def get_queryset(self):
        #print(self.kwargs['pk'])
        queryset = CustomUsers.objects.filter(PersonNo=self.kwargs['pk'])
        #print(len(queryset))
        return queryset

    def get_serializer_class(self):
        if self.request.method == "PUT":
            #print("hhh")
            #print(self.request.user.PersonNo)
            if self.kwargs['pk'] == self.request.user.PersonNo:
                print("go CustomUserDetailSerializerForPutForSelf")
                return CustomUserDetailSerializerForPutForSelf
            else:
                print("go CustomUserDetailSerializerForPutForAdmin")
                return CustomUserDetailSerializerForPutForAdmin
        else:
            #print("hhh")
            return CustomUserDetailSerializerForGet

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

class ListUnhandledProcess(generics.ListAPIView):
    #查看待办的所有流程，无参
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        qst = ProcessHandleEvent.objects.filter(ProcessHandler=self.request.user, ProcessHandleStatus=2).values('ProcessOriginalEvent')
        ProcList=[]
        for q in qst:
            ProcList.append(q['ProcessOriginalEvent'])
        queryset=ProcessRaiseEvent.objects.filter(id__in=ProcList)
        return queryset
    serializer_class = ListUnhandledProcessSerializer

class HandleProcess(generics.RetrieveUpdateAPIView):
    #处理流程，参数为流程号
    lookup_field = 'ProcessOriginalEvent'
    permission_classes = [IsCapableOfHandler]
    
    def get_queryset(self):
        queryset=ProcessHandleEvent.objects.filter(ProcessHandler=self.request.user)
        return queryset
    def get_serializer_class(self):
        if self.request.method == "PUT":
            return HandleProcessSerializerForPut
        else:
            return HandleProcessSerializerForGet

class ModifyProcessRaiseEvent(generics.RetrieveUpdateAPIView):
    # 修改流程发起，仅1和5可修改
    # lookup_field = 'ProcessOriginalEvent'
    permission_classes = [IsAvailableOfModifyProcessRaiseEvent]
    
    def get_queryset(self):
        Pid=self.kwargs['pk']
        queryset=ProcessRaiseEvent.objects.filter(pk=Pid)
        return queryset

    def get_serializer_class(self):
        if self.request.method == "PUT":
            return ModifyProcessRaiseEventSerializerForPut
        else:
            return ModifyProcessRaiseEventSerializerForGet

class CreateNotice(generics.CreateAPIView):
    #发起通知 只可以向下级发起通知
    permission_classes = [permissions.IsAuthenticated]
    #queryset=
    serializer_class = CreateNoticeSerializer

class ModifyNoticeDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAvailableOfModifyNotice]
    
    def get_queryset(self):
        Pid=self.kwargs['pk']
        queryset=NoticeRaiseEvent.objects.filter(pk=Pid)
        return queryset

    def get_serializer_class(self):
        if self.request.method == "PUT":
            return ModifyNoticeDetailSerializerForPut
        else:
            return ModifyNoticeDetailSerializerForGet

class NoticeDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAvailableOfNotice]
    def get_queryset(self):
        Pid=self.kwargs['pk']
        queryset=NoticeRaiseEvent.objects.filter(pk=Pid)
        return queryset

    def get_serializer_class(self):
        if self.request.method == "PUT":
            if NoticeReceiveEvent.objects.filter(NoticeOriginalEvent=self.kwargs['pk'],NoticeReceiver=self.request.user,NeedToRelay=True).exists():
                return NoticeDetailSerializerForPutForRelayer
            else:
                return NoticeDetailSerializerForPutForReceiver
        else:
            return NoticeDetailSerializerForGet

class ListUnreadNotice(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        qst = NoticeReceiveEvent.objects.filter(NoticeReceiver=self.request.user, NoticeRead=False).values('NoticeOriginalEvent')
        ProcList=[]
        for q in qst:
            ProcList.append(q['NoticeOriginalEvent'])
        queryset=NoticeRaiseEvent.objects.filter(id__in=ProcList)
        return queryset
    serializer_class = ListUnreadNoticeSerializer

class NoticeStatus(generics.ListAPIView):
    permission_classes = [IsAvailableOfNoticeStatus]
    # pagination_class = LimitPagination
    def get_queryset(self):
        Pid=self.kwargs['pk']
        Qid=self.request.user
        # 查询 母通知为pid，未读的直接下属 结果应当为下属 
        #rqst = CustomUserManager.objects.raw("select NoticeReceiver_id from oa_noticereceiveevent where NoticeReceiver_id in (select PersonNo from oa_customusers where PersonDirectSuperior_id = %s) and NoticeRead=0 and NoticeOriginalEvent_id = %s",  (Qid,Pid,))
        # select PersonNo from oa_customusers where PersonDirectSuperior_id = %s
        innerqst=CustomUsers.objects.filter(PersonDirectSuperior=self.request.user).values('PersonNo')
        innerProcList=[]
        for q in innerqst:
            innerProcList.append(q['PersonNo'])
        outterqst=NoticeReceiveEvent.objects.filter(NoticeOriginalEvent=Pid, NoticeRead=False, NoticeReceiver__in=innerProcList).values('NoticeReceiver')
        outterProcList=[]
        for q in outterqst:
            outterProcList.append(q['NoticeReceiver'])
        print(q)
        return CustomUsers.objects.filter(PersonNo__in=outterProcList)
    serializer_class = NoticeStatusSerializer

