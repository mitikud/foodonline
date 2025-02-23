from django.db import models
from datetime import time
from accounts.models import User, UserProfile
from accounts.util import send_notification_is_approved
from datetime import datetime, date
# Create your models here.

class Vendor(models.Model):
    user = models.OneToOneField(User, related_name='vendor_user', on_delete=models.CASCADE,blank=True, null=True)
    user_profile = models.OneToOneField(UserProfile, related_name='user_profile', on_delete=models.CASCADE,blank=True, null=True)
    vendor_name = models.CharField(max_length=50)
    vendor_slug = models.SlugField(max_length=100, unique=True) 
    vendor_license = models.ImageField(upload_to='vendor/licence')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor_name
    def is_open(self):
        current_today = date.today()
        today = current_today.isoweekday()

        current_opening_hours = OpeningHours.objects.filter(vendor=self, day=today)
        
        now = datetime.now().time()  # Get current time as a time object
        current_time = now.strftime('%H:%M:%S')
        is_open = None  # Default to closed
    
        for i in current_opening_hours:
            # if not i.from_hour or not i.to_hour:
            #     continue

            if not i.is_closed:
                start = str(datetime.strptime(i.from_hour,"%I:%M %p").time())
                end = str(datetime.strptime(i.to_hour,"%I:%M %p").time())
                print(current_time > start and current_time < end)
                if current_time > start and current_time < end:
                    is_open = True
                    break
                else:
                    is_open = False     
        return is_open
    def save(self, *args, **kwargs):
        if self.pk is not None:
            #update
            org = Vendor.objects.get(pk=self.pk)
            if org.is_approved != self.is_approved:
                mail_template = "accounts/emails/admin_approval_email.html"
                context = {
                    'user': self.user,
                    'is_approved': self.is_approved
                }
                if self.is_approved == True:
                    #send email notification
                    mail_subject = "Congratulations! Your restaurant has been approved"
                    send_notification_is_approved(mail_subject, mail_template, context)
                else:
                    #send email notification
                    mail_subject = "We are sorry! you are not eligible for publishing your restaurant"
                    send_notification_is_approved(mail_subject, mail_template, context)


        return super(Vendor, self).save(*args, **kwargs)

DAYS =[
    (1,('Monday')),
    (2,('Tuesday')),
    (3,('Wednesday')),
    (4,('Thursday')),
    (5,('Friday')),
    (6,('Saturday')),
    (7,('Sunday')),

]

# HOURS_OF_DAY_24 = [(time(hr, m).strftime('%I:%M: %p'),time(hr, m).strftime('%I:%M: %p')) for hr in range(1,24) for m in range(0,30)]

HOURS_OF_DAY_24 = [
    (time(hr, m).strftime('%I:%M %p'), time(hr, m).strftime('%I:%M %p')) 
    for hr in range(0, 24) for m in (0, 30)
]


class OpeningHours(models.Model):
    vendor=models.ForeignKey(Vendor, on_delete=models.CASCADE)
    day=models.IntegerField(choices=DAYS)
    from_hour = models.CharField(choices=HOURS_OF_DAY_24, max_length=10, blank=True)
    to_hour = models.CharField(choices=HOURS_OF_DAY_24, max_length=10, blank=True)
    is_closed = models.BooleanField(default=False)

    class Meta:
        ordering = ('day','-from_hour',)
        unique_together = ('vendor','day','from_hour', 'to_hour')
    
   
    def __str__(self):
        return self.get_day_display()
