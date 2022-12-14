from django.contrib import admin
from django.contrib import messages
from django.contrib.admin import SimpleListFilter
from import_export.admin import ImportExportModelAdmin
from numpy import rec
from django.contrib.admin.models import LogEntry, CHANGE
from .models import  Activity ,ActivitySuggestion , ActivityCategory  , ActivityRequest , ActivityRestorationRequest  
from Users.models import User , ROLE
from django.utils.translation import gettext_lazy as _
import datetime
import pytz
from django import forms
from .forms import CategoryForm , ActivityForm
from .resources import CategoryResource , ActivityResource

# Register your models here.

    
class Filter(admin.SimpleListFilter):
    title = _('Archived')
    parameter_name = 'is_archived'
    # default = 'Yes'
    def lookups(self, request, model_admin):

        return (
            (None, _('Active')),
            
            ('yes', _('Archived')),

            ("all",_('all')),
        )



    def choices(self, cl):
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == lookup,
                'query_string': cl.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title,
            }

    def queryset(self, request, queryset):
        
        if self.value() == 'yes':
            return queryset.filter(is_archived=True)  

        elif self.value() == None:
            return queryset.filter(is_archived = False)


    
class Filter2(admin.SimpleListFilter):
    title = _('Accepted')
    parameter_name = 'is_accepted'
    # default = 'Yes'
    def lookups(self, request, model_admin):

        return (
            ("no", _('Accepted')),
            
            ('yes', _('not accepted')),

            (None,_('all')),
        )



    def choices(self, cl):
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == lookup,
                'query_string': cl.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title,
            }

    def queryset(self, request, queryset):
        
        if self.value() == 'yes':
            return queryset.filter(is_accepted=False)  

        elif self.value() == 'no':
            return queryset.all()

@admin.action(description='Archive Category')
def AdminArchiveCategory(modeladmin, request, queryset):
        
    queryset.update(is_archived = True)
    
    for category in queryset:
        Activity.objects.filter(category = category).update(is_archived = True)
        ActivityCategory.objects.filter(pk = category.id).update(is_archived = True)
        print (not ActivityCategory.objects.filter(owner = category.owner , is_archived = False).exists())
        if not ActivityCategory.objects.filter(owner = category.owner , is_archived = False).exists() and not ActivityCategory.objects.filter(owner = category.owner)[0].owner.role == ROLE[0][0]:
            User.objects.filter(pk = category.owner.emp_id).update(role = ROLE[2][0])
        # ActivityRequest.objects.filter(category = category).update(is_archived = True)
    # messages.error(request, f'Activity cannot be restored after the end date of id {cat.id} with the name of {cat.activity_name}')  
    messages.success(request, f'Category(ies) Archived successfully')  
    

@admin.action(description='Restore Category')
def AdminRestoreCategory (modeladmin, request, queryset):
    utc=pytz.UTC
    d = datetime.date( datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.now().day)
    count=0
    for obj in queryset:
        cat = ActivityCategory.objects.filter(id = obj.id)[0]
        if  cat.end_date >= d and cat.is_archived==True:
            ActivityCategory.objects.filter(id=cat.id).update(is_archived = False)
            count=count+1
        elif cat.is_archived==False:
            messages.error(request, f'Category {cat.category_name} cannot be restored since it already is not archived')  
        elif cat.end_date < d:
            messages.error(request, f'Category {cat.category_name} cannot be restored after the end date.')
        if obj.owner.is_active == False:
            messages.error(request, f'Category {cat.category_name} cannot as category owner {obj.owner.first_name} {obj.owner.last_name} is not active.')

              
        if obj.owner.role == ROLE[2][0]:
            User.objects.filter(pk = obj.owner.emp_id).update(role = ROLE[1][0])
    if count != 0:
            messages.success(request, f'{count} Category(ies) restored successfully')
        
       
@admin.action(description='Restore Activity')
def AdminRestoreActivity (modeladmin, request, queryset):
    utc=pytz.UTC
    now = utc.localize(datetime.datetime.now())
    count=0
    for obj in queryset:
        cat = Activity.objects.filter(id = obj.id)[0]
        if cat.end_date >= datetime.date.today() and cat.category.is_archived==False and cat.is_archived==True:
            Activity.objects.filter(id=cat.id).update(is_archived = False)
            count=count+1
        elif cat.is_archived==False:
            messages.error(request, f'Activity with id {cat.id} and the name of {cat.activity_name} cannot be restored since it already is not archived') 
        elif cat.category.is_archived==True:
            messages.error(request, f'Activity with id {cat.id} and the name of {cat.activity_name} cannot be restored since the parent category with the name {cat.category.category_name} is archived')       
        else:
            messages.error(request, f'Activity with id {cat.id} and the name of {cat.activity_name} cannot be restored after the end date.')  
    if count != 0:
        messages.success(request, f'{count} Activity(ies) restored successfully')


# Register your models here.
@admin.display(description='Owner')
def owner(obj):
    return User.objects.filter(is_active = True)


        
@admin.register(ActivityCategory)
class ViewAdminCategory(ImportExportModelAdmin,admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'owner':
            return CategoryForm(queryset=User.objects.filter(is_active = True))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    resource_class = CategoryResource
    actions = [AdminArchiveCategory, AdminRestoreCategory]
    fields = ('category_name', 'description','owner','start_date','end_date','threshhold','is_archived')
    list_display = ["category_name","description","owner","start_date","end_date","is_archived"]
    list_filter = [Filter,"owner","start_date","end_date"]
    search_fields = ["category_name","owner__username"]
    readonly_fields = ['budget']
    # change_list_template: str


    def get_queryset(self, request):
        data = super().get_queryset(request)
        to_archive = data.filter(end_date__lte=datetime.date.today())
        to_archive.update(is_archived=True)
        for category in to_archive:
            Activity.objects.filter(category = category).update(is_archived = True)
            ActivityCategory.objects.filter(pk = category.id).update(is_archived = True)
        return data
@admin.action(description='Archive Activity')
def AdminArchiveActivity(modeladmin, request, queryset):
       
    queryset.update(is_archived = True)
    
    for category in queryset:
        Activity.objects.filter(pk = category.id).update(is_archived = True)
    messages.success(request, f'Activity(ies) Archived successfully')  

@admin.register(Activity)
class ViewAdmin(ImportExportModelAdmin , admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ActivityForm(queryset = ActivityCategory.objects.filter(is_archived = False))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    actions = [AdminRestoreActivity,AdminArchiveActivity]
    resource_class = ActivityResource
    fields = ('activity_name', 'category','activity_description','start_date','end_date','points','evidence_needed','is_archived','approved_by')

    list_display = ("activity_name","category","activity_description","start_date","end_date","is_archived")

    list_filter = [Filter,"category","start_date","end_date"]
    readonly_fields = ("approved_by",)
    def get_queryset(self, request):
        data = super().get_queryset(request)
        to_archive = data.filter(end_date__lte=datetime.date.today())
        to_archive.update(is_archived=True)
        for activity in to_archive:
            Activity.objects.filter(pk = activity.id).update(is_archived = True)
          
        return data

@admin.register(ActivitySuggestion)
class Viewsuggestion(admin.ModelAdmin):
    list_display = ("activity_name","category","activity_description","justification","is_accepted")
    readonly_fields = ["category"]
    list_filter = [Filter2]

    def has_add_permission(self, request):
            
        return False
    
@admin.register(ActivityRequest)
class Viewrequests(admin.ModelAdmin):
    list_display = ("employee","submitter","submission_date","date_of_action","category", "activity","status")

    readonly_fields = ["employee", "submitter","date_of_action", "category" , "activity", "approved_by" , "proof_of_action","activity_approval_date",]

    list_filter = ['status']

    def has_add_permission(self, request):
            
        return False
    class Meta:
        model= ActivityRequest
            

