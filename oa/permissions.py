from rest_framework import permissions
from rest_framework.permissions import IsAdminUser, SAFE_METHODS
from oa.models import *

class IsSuperiorOfRequestOrAdmin(permissions.BasePermission):
    #检查是否拥有该用户的上级权限
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        elif request.method in permissions.SAFE_METHODS:
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