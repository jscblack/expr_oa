from rest_framework import permissions
from rest_framework.permissions import IsAdminUser, SAFE_METHODS
from oa.models import *

class IsSuperiorOfRequestOrAdmin(permissions.BasePermission):
    #检查是否拥有该用户的上级权限
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        elif request.method in permissions.SAFE_METHODS or request.method=='PUT':
            # Check permissions for read-only request
            AuthList=[request.user.PersonNo]
            # print('lll')
            # print(self)
            #print(request.META)
            flag=1
            while flag==1:
                flag=0
                qst=CustomUsers.objects.filter(PersonDirectSuperior__in=AuthList)
                for q in qst:
                    if q.PersonNo not in AuthList:
                        flag=1
                        AuthList.append(q.PersonNo)
                #print(AuthList)
            return view.kwargs['pk'] in AuthList
        else:
            # Check permissions for write request
            return False

class IsOwnerOrTargetOfRequest(permissions.BasePermission):
    #检查是否拥有该用户是否拥有该流程的权限
    def has_permission(self, request, view):
        
        if not request.user.is_authenticated:
            return False
        elif request.method in permissions.SAFE_METHODS:
            # Check permissions for read-only request
            Pid = view.kwargs['pk']
            qsz = ProcessRaiseEvent.objects.values_list('ProcessRaiser', flat=True).get(pk=Pid)
            qst = ProcessHandleEvent.objects.filter(ProcessOriginalEvent=Pid).values('ProcessHandler')
            AuthList = []
            for a in qst:
                AuthList.append(a['ProcessHandler'])
            AuthList.append(qsz)
            return request.user.PersonNo in AuthList
        else:
            # Check permissions for write request
            return False

class IsCapableOfHandler(permissions.BasePermission):
    #检查是否拥有该用户是否拥有目前处理该流程的权限
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        elif request.method in permissions.SAFE_METHODS:
            # Check permissions for read-only request
            Pid = view.kwargs['ProcessOriginalEvent']
            # qsz = ProcessRaiseEvent.objects.values_list('ProcessRaiser', flat=True).get(pk=Pid)
            qst = ProcessHandleEvent.objects.filter(ProcessOriginalEvent=Pid,ProcessHandleStatus=2).values('ProcessHandler')
            AuthList = []
            for a in qst:
                AuthList.append(a['ProcessHandler'])
            return request.user.PersonNo in AuthList
        else:
            # Check permissions for write request
            Pid = view.kwargs['ProcessOriginalEvent']
            # qsz = ProcessRaiseEvent.objects.values_list('ProcessRaiser', flat=True).get(pk=Pid)
            qst = ProcessHandleEvent.objects.filter(ProcessOriginalEvent=Pid,ProcessHandleStatus=2).values('ProcessHandler')
            AuthList = []
            for a in qst:
                AuthList.append(a['ProcessHandler'])
            return request.user.PersonNo in AuthList

class IsAvailableOfModifyProcessRaiseEvent(permissions.BasePermission):
    #检查该用户是否拥有流程的所有权Get以及是否可以修改
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        elif request.method in permissions.SAFE_METHODS:
            # Check permissions for read-only request
            Pid = view.kwargs['pk']
            # qsz = ProcessRaiseEvent.objects.values_list('ProcessRaiser', flat=True).get(pk=Pid)
            print(Pid)
            qst = ProcessRaiseEvent.objects.filter(id=Pid).values('ProcessRaiser')
            if len(qst)!=1:
                 return False
            qst=qst[0]
            # print(qst)
            return request.user.PersonNo == qst['ProcessRaiser']
        else:
            Pid = view.kwargs['pk']
            # qsz = ProcessRaiseEvent.objects.values_list('ProcessRaiser', flat=True).get(pk=Pid)
            print(Pid)
            qst = ProcessRaiseEvent.objects.filter(id=Pid).values('ProcessRaiser')
            if len(qst)!=1:
                 return False
            qst=qst[0]
            if request.user.PersonNo != qst['ProcessRaiser']:
                print("fail put")
                return False

            return ProcessRaiseEvent.objects.values_list('ProcessRaiseStatus', flat=True).get(pk=Pid) in [1,5]


class IsAvailableOfModifyNotice(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        else:
            Pid = view.kwargs['pk']
            qst = NoticeRaiseEvent.objects.filter(id=Pid).values('NoticeRaiser')
            if len(qst)!=1:
                 return False
            qst=qst[0]
            return request.user.PersonNo == qst['NoticeRaiser']
            
class IsAvailableOfNotice(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        elif request.method in permissions.SAFE_METHODS:
            Pid = view.kwargs['pk']
            return NoticeReceiveEvent.objects.filter(NoticeOriginalEvent=Pid, NoticeReceiver=request.user).exists() or NoticeRaiseEvent.objects.filter(pk=Pid, NoticeRaiser=request.user)
        else:
            #检查是否需要有PUT权限即未read或未relay
            Pid = view.kwargs['pk']
            return NoticeReceiveEvent.objects.filter(NoticeOriginalEvent=Pid, NoticeReceiver=request.user, NoticeRead=False).exists()

class IsAvailableOfNoticeStatus(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        elif request.method in permissions.SAFE_METHODS:
            Pid = view.kwargs['pk']
            return NoticeReceiveEvent.objects.filter(NoticeOriginalEvent=Pid, NoticeReceiver=request.user, NeedToRelay=True).exists() or NoticeRaiseEvent.objects.filter(pk=Pid, NoticeRaiser=request.user)
        else:
            return False