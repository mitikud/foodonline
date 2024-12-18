from django.db import models
from accounts.models import User, UserProfile
from accounts.util import send_notification_is_approved
# Create your models here.

class Vendor(models.Model):
    user = models.OneToOneField(User, related_name='vendor_user', on_delete=models.CASCADE,blank=True, null=True)
    user_profile = models.OneToOneField(UserProfile, related_name='user_profile', on_delete=models.CASCADE,blank=True, null=True)
    vendor_name = models.CharField(max_length=50)
    vendor_license = models.ImageField(upload_to='vendor/licence')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor_name
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

