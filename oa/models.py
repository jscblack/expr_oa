from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import constraints
from oa.customUserManager import CustomUserManager
# Create your models here.

class CustomUsers(AbstractUser):
    username=None
    first_name=None
    last_name=None
    email=None
    date_joined=None
    PersonGenerChoice=(
        (1, 'Female'),
        (2, 'Male'),
    )
    PersonNo=models.IntegerField(primary_key=True)
    PersonEmail = models.EmailField()
    PersonLastName=models.CharField(max_length=50)
    PersonFirstName=models.CharField(max_length=50)
    PersonGender=models.IntegerField(choices =PersonGenerChoice)
    PersonAge = models.IntegerField()
    PersonPhone = models.CharField(max_length=11)
    PersonJob=models.CharField(max_length=50)
    PersonDirectSuperior=models.ForeignKey("self",on_delete=models.PROTECT)
    USERNAME_FIELD = 'PersonNo'
    REQUIRED_FIELDS = ['PersonEmail','PersonLastName','PersonFirstName','PersonGender','PersonAge','PersonPhone','PersonJob','PersonDirectSuperior'] 
    EMAIL_FIELD = 'PersonEmail'

    objects = CustomUserManager()

    def get_full_name(self):
        return self.PersonLastName+self.PersonFirstName

    def get_short_name(self):
        return self.PersonLastName

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name
        

    def __str__(self):
        return f"{self.PersonNo} ({self.PersonLastName} {self.PersonFirstName})"

class ProcessRaiseEvent(models.Model):
    #ProcessNo
    ProcessRaiseStatusTypes=[
        (1, 'Unhandled'),#未处理
        (2, 'Handling'),#待处理
        (3, 'HandledAndAccepted'),#已处理并接受
        (4, 'HandledAndRejected'),#已处理并拒绝
        (5, 'WaittingToBeModified'),#需要修改
    ]
    ProcessRaiser=models.ForeignKey("CustomUsers", on_delete=models.PROTECT)
    ProcessRaiseTime=models.DateTimeField(auto_now=True)
    ProcessRaiseTitle=models.CharField(max_length=50)
    ProcessRaiseInfo=models.JSONField()
    ProcessRaiseStatus=models.IntegerField(default=1,choices=ProcessRaiseStatusTypes)
    class Meta:
        verbose_name = "processraiseevent"
        verbose_name_plural = "processraiseevents"

    def __str__(self):
        # return f"({self.id}) {self.ProcessRaiseInfo}"
        return f"{self.id} ({self.ProcessRaiseTitle})"
        pass

    # def get_absolute_url(self):
    #     return reverse("processraiseevent_detail", kwargs={"pk": self.pk})

class ProcessHandleEvent(models.Model):
    ProcessHandleStatusTypes=[
        (1, 'Unhandled'),#未处理但不需要处理
        (2, 'WaitingToBeHandled'),#待处理
        (3, 'Handled'),#已处理
    ]
    ProcessHandleResultTypes=[
        (1, 'Accepted'),#通过并进入下一级（本级处理状态置为3，下一级状态置为2）
        (2, 'Rejected'),#拒绝不进入下一级（本级处理状态置为3）
        (3, 'Revert'),#拒绝打回重新提交（需要将上一级的处理状态置为2，本级置为1）
    ]
    ProcessOriginalEvent=models.ForeignKey("ProcessRaiseEvent", on_delete=models.PROTECT)
    ProcessHandleLevel=models.IntegerField()
    ProcessHandleTime=models.DateTimeField(auto_now=True)
    ProcessHandleStatus=models.IntegerField(choices=ProcessHandleStatusTypes)
    ProcessHandler=models.ForeignKey("CustomUsers", on_delete=models.PROTECT)
    ProcessHandleInfo=models.JSONField(null=True)
    ProcessHandleResult=models.IntegerField(null=True,choices=ProcessHandleResultTypes)
    
    class Meta:
        verbose_name = 'ProcessHandleEvent'
        verbose_name_plural = 'ProcessHandleEvents'

    def __str__(self):
        # return f"({self.ProcessOriginalEvent})"
        pass

class NoticeRaiseEvent(models.Model):
    NoticeRaiser=models.ForeignKey("CustomUsers", on_delete=models.PROTECT)
    NoticeRaiseTime=models.DateTimeField(auto_now=True)
    NoticeRaiseTitle=models.CharField(max_length=50)
    NoticeRaiseInfo=models.JSONField()
    
    def __str__(self):
        pass

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'NoticeRaiseEvent'
        verbose_name_plural = 'NoticeRaiseEvents'

class NoticeReceiveEvent(models.Model):
    NoticeOriginalEvent=models.ForeignKey("NoticeRaiseEvent", on_delete=models.PROTECT)
    NoticeReceiver=models.ForeignKey("CustomUsers", on_delete=models.PROTECT)
    NeedToRelay=models.BooleanField(default=False) #是否需要向下一级转发（由上一级给定）
    NoticeRelay=models.BooleanField(default=False) #是否已转发
    NoticeRead=models.BooleanField(default=False) #是否已读
    
    # 向下一级转发的指令应当依附于当前级 

    def __str__(self):
        pass

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'NoticeReceiveEvent'
        verbose_name_plural = 'NoticeReceiveEvents'