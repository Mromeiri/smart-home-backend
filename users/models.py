from django.db import models
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from firebase_admin.messaging import Message as mm, Notification as bb, send

def send_push_notification_to_confirme(noti):
    user = noti.user
    notificaion_detail = NotificationML.objects.filter(pk=noti.id).first()

    if noti.itemControlled =="light":
        # print("class wanted to apply is "+noti.classWantedToApply)
        # print(noti.classWantedToApply)
        if str(noti.classWantedToApply)=="0":
            print("class wanted to apply is "+noti.classWantedToApply)
            notificaion_detail.detail="Souhaitez-vous éteindre la lumière"
            additional_data = {
                'data_type':'ML',
                'id': str(noti.id),
                'title': 'ML',
                'date': str(noti.date),
                'detail': "Souhaitez-vous éteindre la lumière",
                
                'classWantedToApply':str(noti.classWantedToApply),
                'itemControlled': str(noti.itemControlled),
                # 'date': noti.date.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'type': 'ML',
                # Add more key-value pairs as needed
            }
        else:
            notificaion_detail.detail="Souhaitez-vous allumer la lumière"
            additional_data = {
                'data_type':'ML',
                'id': str(noti.id),
                'title': 'ML',
                'date': str(noti.date),
                'detail': "Souhaitez-vous allumer la lumière",
                
                'classWantedToApply':str(noti.classWantedToApply),
                'itemControlled': str(noti.itemControlled),
                # 'date': noti.date.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'type': 'ML',
                # Add more key-value pairs as needed
            }
    elif noti.itemControlled =="weather":
        notificaion_detail.detail="Souhaitez-vous augmenter la vitesse de ventilateur a "+str(noti.classWantedToApply)+"?"
        additional_data = {
            'data_type':'ML',
            'id': str(noti.id),
            'title': 'ML',
            
            
            'detail': "Souhaitez-vous augmenter la vitesse de ventilateur a "+str(noti.classWantedToApply)+"?",
            'date': str(noti.date),
            # 'date': noti.date.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'classWantedToApply':str(noti.classWantedToApply),
                'itemControlled': str(noti.itemControlled),
                # 'date': noti.date.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'type': 'ML',
            # Add more key-value pairs as needed
        } 
    else:
        notificaion_detail.detail="Voudriez-vous changer la chaîne de télévision en "+str(noti.classWantedToApply)+"?"
        additional_data = {
            'data_type':'ML',
            'id': str(noti.id),
            'title': 'ML',
            
            
            'detail': "Voudriez-vous changer la chaîne de télévision en "+str(noti.classWantedToApply)+"?",
           
            'date': str(noti.date),
            # 'date': noti.date.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'classWantedToApply':str(noti.classWantedToApply),
                'itemControlled': str(noti.itemControlled),
                # 'date': noti.date.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'type': 'ML',
            # Add more key-value pairs as needed
        } 
    notificaion_detail.save()
    message = mm(
            notification=bb(
                title=noti.title,  # Access the title attribute of the Notification instance
                body=noti.detail,  # Access the detail attribute of the Notification instance
                ),
            data=additional_data,
            token=user.token,
        )
    

    response = send(message)

    print('Successfully sent message:', response)



def send_push_notification(noti):
    user = noti.user
    additional_data = {
        'data_type':'notification',
        'id': str(noti.id),
        'title': str(noti.title),
        'detail': str(noti.detail),
        'thumnail': str(noti.image),
        'date': str(noti.date),
        # 'date': noti.date.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        'type': 'Notification',
        # Add more key-value pairs as needed
    }  
    message = mm(
            notification=bb(
                title=noti.title,  # Access the title attribute of the Notification instance
                body=noti.detail,  # Access the detail attribute of the Notification instance
                ),
            data=additional_data,
            token=user.token,
        )
    

    response = send(message)

    print('Successfully sent message:', response)

def send_push_annoncment(noti):
    user = AppUser.objects.all()
    additional_data = {
        'data_type':'notification',
        'id': str(noti.id),
        'title': str(noti.title),
        'detail': str(noti.detail),
        'thumnail': str(noti.image),
        'date': str(noti.date),
        # 'date': noti.date.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        'type': 'annoncment',
        # Add more key-value pairs as needed
    }  
    for user_id in user:
        if user_id.token :
            message = mm(
                    notification=bb(
                        title=noti.title,  # Access the title attribute of the Notification instance
                        body=noti.detail,  # Access the detail attribute of the Notification instance
                        ),
                    data=additional_data,
                    token=user_id.token,
                )
        

            response = send(message)

    print('Successfully sent message:', response)
class AppUser(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=30, unique=True, null=False)
    adress = models.CharField(max_length=50,null=True,blank=True)
    date_registration = models.DateTimeField(auto_now_add=True)
    token = models.TextField( null=True,blank=True)
    solde = models.DecimalField(max_digits=50, decimal_places=2, default=0)
    total_spend = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='user_images/', null=True, blank=True)


    def save(self, *args, **kwargs):
        # Check if the password has been changed
        if not self.pk:
            # If it's a new instance, hash the password
            self.password = make_password(self.password)
        else:
            # If it's an existing instance, check if the password has changed
            original = AppUser.objects.get(pk=self.pk)
            if original.password != self.password:
                self.password = make_password(self.password)

        self.username = self.username.lower()
        super().save(*args, **kwargs)



    def __str__(self):
        return self.username

class ContactMessage(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, null=True)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()

    class Meta:
        db_table = 'contact'

    def __str__(self):
        return str(self.user)

class AnnouncementModel(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    detail = models.TextField()

    class Meta:
        abstract = True  # This makes the BaseModel abstract and won't create a database table for it

class Notification(AnnouncementModel):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, null=True)
    isread = models.BooleanField(default=False)
    image = models.ImageField(upload_to='user_notification/', null=True, blank=True)
    def save(self, *args, **kwargs):
        if not self.pk:
            
        
            super().save(*args, **kwargs)
            send_push_notification(self)
        else :
            super().save(*args, **kwargs)


    def __str__(self):
        return f"Notification - {self.title}"

class NotificationML(AnnouncementModel):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, null=True)
    itemControlled = models.CharField(max_length=255)
    classWantedToApply = models.CharField(max_length=255)
    isread = models.BooleanField(default=False)
    def save(self, *args, **kwargs):
        if not self.pk:
            
        
            super().save(*args, **kwargs)
            send_push_notification_to_confirme(self)
        else :
            super().save(*args, **kwargs)


    def __str__(self):
        return f"NotificationML - {self.title}"
class Announcement(AnnouncementModel):
    image = models.ImageField(upload_to='Announcement/', null=True, blank=True)
    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)
            send_push_annoncment(self)
        else :
            super().save(*args, **kwargs)
    def __str__(self):
        return f"Announcement - {self.title}"

class ReadAnnouncement(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('announcement', 'user')

    def __str__(self):
        return f"ReadAnnouncement - {self.id}"