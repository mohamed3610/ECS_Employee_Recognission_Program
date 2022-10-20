from datetime import datetime
from unicodedata import category
from django.db import models
from Users.models import User, Role
from enum import Enum
from django.db.models import Sum
from django.core.exceptions import ValidationError
from Rewards.models import budget

# Create your models here.


# validate category budget
def validate_budget(value):
    total_budget = budget.objects.filter(Archived_at = None)[0].budget_compare
    used_budget = ActivityCategory.objects.aggregate(Sum('budget_compare'))['budget_compare__sum']
    if(not used_budget):
        used_budget = 0
    if(value>total_budget-used_budget):
        raise ValidationError("Budget exceeded the limit")

class ActivityCategory(models.Model):
    category_name = models.CharField(max_length=30,null=False, blank= False, unique = True)
    description =  models.CharField(max_length=255,null=False, blank= False, default="")
    creation_date = models.DateTimeField(auto_now_add=True,editable=False)
    start_date = models.DateTimeField(editable=True, null = True, blank = True)
    end_date = models.DateTimeField(editable=True , null = True, blank = True)
    owner = models.ForeignKey(User,on_delete=models.CASCADE,null=True, related_name="category_owner")
    budget = models.IntegerField(null = False, blank = False, validators = [validate_budget])
    budget_compare = models.IntegerField(null = False, blank = False)

    def clean(self, *args, **kwargs):
        if(self.start_date>self.end_date):
            raise ValidationError("Start Date must be before end date")
        if(self.budget_compare<self.budget):
            raise ValidationError("Remaining budget can not be bigger than the original budget")
        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.category_name

class CategoryArchive(models.Model):
    category_name = models.CharField(max_length=30,null=False, blank= False, unique = True)
    description =  models.CharField(max_length=255,null=False, blank= False, default = "")
    creation_date = models.DateTimeField(auto_now_add=True,editable=False)
    start_date = models.DateTimeField(editable=True)
    end_date = models.DateTimeField(editable=True , null = True)
    owner = models.ForeignKey(User,on_delete=models.CASCADE,null=True, related_name="archivedcategory_owner")
    budget = models.IntegerField(null = False, blank = False)
    budget_compare = models.IntegerField(null = False, blank = False)
    archive_date = models.DateTimeField(auto_now_add=True,editable=False)
    archived_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True, related_name="archived_by")



class Activity(models.Model):
    activity_name = models.CharField(max_length=30,null=False, blank= False, unique=True)
    activity_description = models.CharField(max_length=1024,null=False, blank= True)
    category = models.ForeignKey(ActivityCategory,on_delete=models.CASCADE,null=False)
    points = models.IntegerField(null = False, blank = False)
    approved_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    evidence_needed =  models.CharField(max_length=1024,null=False, blank= False)
    creation_date = models.DateTimeField(auto_now_add=True,editable=False)
    start_date = models.DateTimeField(editable=True)
    end_date = models.DateTimeField(editable=True,null=True)
    is_approved = models.BooleanField(null=False,blank = False , default=False)

    def clean(self, *args, **kwargs):
        if(self.start_date>self.end_date):
            raise ValidationError("Start Date must be before end date")
        category_budget = self.category.budget
        conversion_rate = budget.objects.filter(Archived_at = None)[0].EGP / budget.objects.filter(Archived_at = None)[0].point
        if(self.points*conversion_rate>category_budget):
            raise ValidationError("Activity points cannot fit within the category remaining budget")
        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.activity_name


class ActivityCategoryEdit(models.Model):
    original_category = models.ForeignKey(ActivityCategory, on_delete=models.CASCADE,null=False)
    category_name = models.CharField(max_length=30,null=False, blank= False)
    description =  models.CharField(max_length=255,null=False, blank= False, default="")
    end_date = models.DateTimeField(editable=True , null = True)
    budget = models.IntegerField(null = False, blank = False)
    edited = models.BooleanField(null=False,blank = False , default=False)
    deleted = models.BooleanField(null=False,blank = False , default=False)


class ActivityEdit(models.Model):
    original_activity = models.ForeignKey(Activity, on_delete=models.SET_NULL,null=True )
    activity_name = models.CharField(max_length=30,null=False, blank= False)
    activity_description = models.CharField(max_length=1024,null=False, blank= True)
    points = models.IntegerField(null = False, blank = False)
    end_date = models.DateTimeField(editable=True,null=True)
    edited = models.BooleanField(null=False,blank = False , default=False)
    deleted = models.BooleanField(null=False,blank = False , default=False)


class ActivityRequest(models.Model):
    STATUS = [
        ("PENDING" , "Pending"),
        ("ACCEPTED" , "Accpeted"),
        ("REJECTED" , "Rejected"),
        ("WITHDRAWN" , "Withdrawn"),         
    ]
    emp = models.ForeignKey(User, on_delete=models.CASCADE, null=True,related_name="Activity_submitter")
    submission_date = models.DateTimeField(auto_now_add=True)
    date_of_action = models.DateTimeField(null = False)
    category = models.ForeignKey(ActivityCategory, on_delete=models.CASCADE,  null=False, db_constraint= True)
    activity = models.ForeignKey(Activity, on_delete = models.CASCADE,  null=True, db_constraint= True)
    status = models.CharField(max_length=10, null = False , blank = False, choices=STATUS, default=STATUS[0])
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, null = True, related_name="Activity_approver")
    evidence_needed = models.CharField(max_length=1024,null=False, blank= False, default="Provide evidence please")
    proof_of_action = models.FileField(upload_to = "proofs/",null=False, blank= False)
    activity_approval_date = models.DateTimeField(auto_now_add=False, auto_now=False, null = True, blank = False)

class OldActivityRequest(models.Model):
    STATUS = [
        ("PENDING" , "Pending"),
        ("ACCEPTED" , "Accpeted"),
        ("REJECTED" , "Rejected"),
        ("WITHDRAWN" , "Withdrawn"),     
    ]
    emp = models.ForeignKey(User, on_delete=models.CASCADE, null=True,related_name="OldActivity_submitter")
    submission_date = models.DateTimeField()
    date_of_action = models.DateTimeField(null = False)
    category = models.ForeignKey(ActivityCategory, on_delete=models.CASCADE,  null=False, db_constraint= True)
    activity = models.ForeignKey(Activity, on_delete = models.CASCADE,  null=True, db_constraint= True)
    status = models.CharField(max_length=10, null = False , blank = False, choices=STATUS)
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE , null = True, related_name="OldActivity_approver")
    evidence_needed = models.CharField(max_length=1024,null=False, blank = False, default="Provide evidence please")
    proof_of_action = models.FileField(upload_to = "proofs/",null=False, blank = False)
    activity_approval_date = models.DateTimeField(auto_now_add=False, auto_now=False, null = True, blank = False)
    update_date = models.DateTimeField(auto_now_add=True,editable=False)
    updated_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True, related_name="OldActivity_update_activityrequest_by")
    updated_approved_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True, related_name="OldActivity_update_approved_by")


    
    
class ActivitySuggestion(models.Model):
    activity_name = models.CharField(max_length=30 , null = False, blank=False)
    category = models.ForeignKey(ActivityCategory , on_delete=models.CASCADE , null=False)
    activity_description = models.CharField(max_length=1024 , null = False, blank=False)
    justification = models.CharField(max_length=30 , null = True, blank=True)
    evidence_needed = models.CharField(max_length=1024 , null = True, blank=True)
    is_archived = models.BooleanField(null=False , default = False)
    
class Points(models.Model):
    points = models.IntegerField(null = False, blank = False)
    amounts = models.IntegerField(null = False, blank = False)
    start_date = models.DateTimeField(auto_now_add=True,editable=False)
    end_date = models.DateTimeField(editable=False)
    employee = models.ForeignKey(User , on_delete=models.CASCADE,null=True , related_name="earned_to")
    is_used = models.BooleanField(null=False,blank = False , default=False)
    



class ActivityArchive(models.Model):
    activity_name = models.CharField(max_length=30,null=False, blank= False, unique=True)
    activity_description = models.CharField(max_length=1024,null=False, blank= True)
    category = models.ForeignKey(ActivityCategory,on_delete=models.CASCADE,null=False)
    points = models.IntegerField(null = False, blank = False)
    approved_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    evidence_needed =  models.CharField(max_length=1024,null=False, blank= False)
    creation_date = models.DateTimeField(auto_now_add=True,editable=False)
    archived_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True, related_name="archive_activity_by")
    start_date = models.DateTimeField(editable=True)
    end_date = models.DateTimeField(editable=True,null=True)
    is_approved = models.BooleanField(null=False,blank = False , default=False)
    archive_date = models.DateTimeField(auto_now_add=True,editable=False)

class ActivityRestorationRequest(models.Model):
    STATUS = [
        ("PENDING" , "Pending"),
        ("ACCEPTED" , "Accpeted"),
        ("REJECTED" , "Rejected"),
        ("WITHDRAWN" , "Withdrawn")              
    ]
    id = models.IntegerField(null = False, blank = False , primary_key = True)
    activity_name = models.CharField(max_length=30,null=False, blank= False, unique=True)
    activity_description = models.CharField(max_length=1024,null=False, blank= True)
    category = models.ForeignKey(ActivityCategory,on_delete=models.CASCADE,null=False)
    points = models.IntegerField(null = False, blank = False)
    approved_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    evidence_needed =  models.CharField(max_length=1024,null=False, blank= False)
    creation_date = models.DateTimeField(auto_now_add=True,editable=False)
    archived_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True, related_name="restore_activity_by")
    start_date = models.DateTimeField(editable=True)
    end_date = models.DateTimeField(editable=True,null=True)
    is_approved = models.BooleanField(null=False,blank = False , default=False)
    archive_date = models.DateTimeField(auto_now_add=True,editable=False)
    status = models.CharField(max_length=10, null = False , blank = False, choices=STATUS, default=STATUS[0])
 




class OldDataActivities(models.Model):
    original_activity = models.ForeignKey(Activity, on_delete=models.CASCADE,null=True )
    activity_name = models.CharField(max_length=30,null=False, blank= False, unique=True)
    activity_description = models.CharField(max_length=1024,null=False, blank= True)
    category = models.ForeignKey(ActivityCategory,on_delete=models.CASCADE,null=False)
    points = models.IntegerField(null = False, blank = False)
    approved_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    evidence_needed =  models.CharField(max_length=1024,null=False, blank= False)
    creation_date = models.DateTimeField(auto_now_add=True,editable=False)
    approve_update_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True, related_name="approve_update_activity_by")
    start_date = models.DateTimeField(editable=True)
    end_date = models.DateTimeField(editable=True,null=True)
    is_approved = models.BooleanField(null=False,blank = False , default=False)
    update_date = models.DateTimeField(auto_now_add=True,editable=False)
    updated_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True, related_name="OldData_update_activity_by")


class OldDataActivitySuggestion(models.Model):
    original_activity_suggestion = models.ForeignKey(ActivitySuggestion, on_delete=models.CASCADE,null=True )
    activity_name = models.CharField(max_length=30 , null = False, blank=False)
    category = models.ForeignKey(ActivityCategory , on_delete=models.CASCADE , null=False )
    activity_description = models.CharField(max_length=1024 , null = False, blank=False)
    justification = models.CharField(max_length=30 , null = True, blank=True)
    evidence_needed = models.CharField(max_length=1024 , null = True, blank=True)
    update_date = models.DateTimeField(auto_now_add=True,editable=False)
    updated_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True, related_name="update_categorySuggestion_by")



class OldDataCategory(models.Model):
    original_category = models.ForeignKey(ActivityCategory, on_delete=models.CASCADE,null=False)
    category_name = models.CharField(max_length=30,null=False, blank= False, unique = True)
    description =  models.CharField(max_length=255,null=False, blank= False, default="")
    creation_date = models.DateTimeField(auto_now_add=True,editable=False)
    start_date = models.DateTimeField(editable=True)
    end_date = models.DateTimeField(editable=True , null = True)
    owner = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    budget = models.IntegerField(null = False, blank = False)
    budget_compare = models.IntegerField(null = False, blank = False)
    update_date = models.DateTimeField(auto_now_add=True,editable=False)
    updated_by = models.ForeignKey(User,on_delete=models.CASCADE , null=True , related_name="OldData_update_category_by")
