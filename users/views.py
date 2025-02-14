from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password,make_password
from firebase_admin.messaging import Message as mm, Notification, send
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from states.models import States

# import users
from .models import *
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils import timezone
from django.db import IntegrityError, DataError
from django.core.exceptions import ValidationError 
@csrf_exempt 
def verify_user(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        password = data.get('password')
        token = data.get('token')

        try:
            user = AppUser.objects.get(username=username)
            # Check if the provided password matches the hashed password in the database
            print(check_password(password, user.password))
            if check_password(password, user.password):
               
                    if user.is_active == True:
                        user.token = token
                        user_data = {
                            'id':user.pk,
                            'username': user.username,
                            'first_name': user.first_name,
                            'last_name': user.last_name,
                            'email': user.email,
                            'phone': user.phone,
                            'date_registration': user.date_registration,
                            'solde': user.solde,
                            'total_spend': user.total_spend,
                            'is_active': user.is_active,
                            'adress':user.adress,
                            'image': str(user.image),
                        }
                        user.token = token
                        user.save()
                        return JsonResponse(user_data)
                    else : 
                        return JsonResponse({'error': 'account Disabled'})
            else:
                return JsonResponse({'error': 'Invalid credentials'})
        except AppUser.DoesNotExist:
            return JsonResponse({'error': 'User not found'})

    return JsonResponse({'error': 'Invalid request method'})

@csrf_exempt
def logout(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        code = data.get('code')
        
        user = get_object_or_404(AppUser, pk=code)
        user.token =''
        user.save()
        return JsonResponse({'success': True, 'message': 'Password changed successfully'})

    else:
        return JsonResponse({'success': False})

@csrf_exempt
def isActive(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        user_id = data.get('id')
        
        user = get_object_or_404(AppUser, pk=user_id)
        if user.is_active == True:
        
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})

    else:
        return JsonResponse({'success': False})

@csrf_exempt
def change_password(request):
    if request.method == 'POST':
        user_id = request.POST.get('id')
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')

        # Fetch the user object based on the user_id
        user = get_object_or_404(AppUser, pk=user_id)

        # Check old password
        if not check_password(old_password, user.password):
            return JsonResponse({'success': False, 'message': 'Old password is incorrect'})

        # Update password
        user.password =new_password
        user.save()

        return JsonResponse({'success': True, 'message': 'Password changed successfully'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})


@csrf_exempt  # Add this decorator if you want to bypass CSRF protection for this view
def update_image(request):
    if request.method == 'POST':
        # Retrieve the additional data from the request's POST data
            user_id = request.POST.get('id')
            

        # Check if the message type is "MESSAGE"

            # Access the uploaded image
            uploaded_image = request.FILES.get('photo')

            # Check if an image file was provided
            if uploaded_image is not None:
                user = AppUser.objects.get(id=user_id)
                user.image = uploaded_image
                
                user.save()
                # send_push_notification(chat_message,user_token)
                return JsonResponse({'message': 'Photo uploaded successfully','url':str(user.image)})

            else:
                return JsonResponse({'message': 'Invalid request, image file is required'}, status=400)

        # Return a JSON response to confirm the successful upload

    return JsonResponse({'message': 'Invalid request method'}, status=405)


@csrf_exempt
def submit_contact_message(request):
    if request.method == 'POST':
        user_id = request.POST.get('user')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        user = get_object_or_404(AppUser, pk=user_id)
        # Create a new ContactMessage instance
        new_message = ContactMessage.objects.create(user=user, email=email, subject=subject, message=message)

        return JsonResponse({'status': 'success', 'message_id': new_message.id})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
 
@csrf_exempt 
def create_user(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        password = data.get('password')
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        phone = data.get('phone')
        mail = data.get('email')
        adress = data.get('adress')
        print(mail)

        try:
            user = AppUser(
             first_name = firstname,
             last_name = lastname,
             username = username,
             password = password,
             email =mail,
             phone = phone,
             adress = adress,
             

            )
            user.save()
          
            

            return JsonResponse({'status': 'success'})
        except IntegrityError as e:
            error_message = str(e)

            if 'username' in error_message:
                return JsonResponse({'status': 'error', 'message': 'Username already exists.'})
            elif 'email' in error_message:
                return JsonResponse({'status': 'error', 'message': 'Email already exists.'})
            elif 'phone' in error_message:
                return JsonResponse({'status': 'error', 'message': 'Phone already exists.'})
            else:
                return JsonResponse({'status': 'error', 'message': 'An error occurred during user creation.'})
        except DataError:
            return JsonResponse({'status': 'error', 'message': 'Invalid data format or length.'})
        except ValidationError as ve:
            return JsonResponse({'status': 'error', 'message': ve.message})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': 'An error occurred during user creation.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})






def get_annoucement_notification(request, user_id):
    user = get_object_or_404(AppUser, id=user_id)
    print(user)

    unread_ml_notifications = NotificationML.objects.filter(user=user, isread=False)
    # Get unread notifications for the user
    unread_notifications = Notification.objects.filter(user=user, isread=False)
    print(unread_notifications)
    # Get announcements that have not been read by the user
    unread_announcements = Announcement.objects.exclude(
        id__in=ReadAnnouncement.objects.filter(user=user).values_list('announcement_id', flat=True)
    )

    # Prepare the data for JSON response
    result = []
    for notification in unread_notifications:
        # Convert UTC datetime to user's timezone
        user_timezone = timezone.get_current_timezone()
        local_date = timezone.localtime(notification.date, user_timezone)
        
        result.append({
            'type': 'Notification',
            'id': notification.id,
            'title': notification.title,
            'body': notification.detail,
            'image': str(notification.image) if notification.image else None,
            'date': local_date.strftime('%Y-%m-%d %H:%M:%S'),  # Format as needed
        })

    for announcement in unread_announcements:
        # Convert UTC datetime to user's timezone
        user_timezone = timezone.get_current_timezone()
        local_date = timezone.localtime(announcement.date, user_timezone)
        
        result.append({
            'type': 'Announcement',
            'id': announcement.id,
            'title': announcement.title,
            'body': announcement.detail,
            'image': str(announcement.image) if announcement.image else None,
            'date': local_date.strftime('%Y-%m-%d %H:%M:%S'),  # Format as needed
        })
    for notification in unread_ml_notifications:
        # Convert UTC datetime to user's timezone
        user_timezone = timezone.get_current_timezone()
        local_date = timezone.localtime(notification.date, user_timezone)
        
        result.append({
            'type': 'ML',
            'id': notification.id,
            'title': notification.title,
            'body': notification.detail,
            'image':  None,
            'date': local_date.strftime('%Y-%m-%d %H:%M:%S'),
            'itemControlled' :notification.itemControlled,
             'predectedClass' :notification.classWantedToApply,# Format as needed
        })

    return JsonResponse(result, safe=False)


def send_push_notification(Notification,user_id):
    


    
        user = get_object_or_404(AppUser, pk=user_id)
        message = mm(
            notification=Notification(
                title=Notification.title,
                body=Notification.detail,
            ),
            token=user.token,
        )

        response = send(message)

        print('Successfully sent message:', response)


def set_notification_read(request ,notification_id):
        noti = get_object_or_404(Notification, id=notification_id)
        noti.isread = True
        noti.save()

        return JsonResponse({'status': 'success'})

def set_Annoucment_read(request ,announcement_id,user_id):
        anoc = get_object_or_404(Announcement, id=announcement_id)
        user = get_object_or_404(AppUser, id=user_id)
        read = ReadAnnouncement(
             user = user,
             announcement = anoc

        )
        
        read.save()

        return JsonResponse({'status': 'success'})

from django.core.mail import send_mail
from django.http import JsonResponse

from django.core.mail import send_mail
from django.http import JsonResponse

# def send_code_email(request, email, code):
#     subject = 'Verification Code'
#     message = f'Your verification code is: {code}'
#     from_email = 'omeiri.abdellah@gmail.com'
#     recipient_list = [email]

#     try:
#         send_mail(
#             subject,
#             message,
#             from_email,
#             recipient_list,
#             fail_silently=False,
#         )
#         return JsonResponse({'status': 'success', 'message': 'Code sent successfully'})
#     except Exception as e:
#         return JsonResponse({'status': 'error', 'message': str(e)})


def send_code_email(request, email, code):
    subject = 'Verification Code'
    message = f'Your verification code is: {code}'
    from_email = 'omeiri.abdellah@gmail.com'
    recipient_list = [email]

    try:
        # Configure email settings within the view
        smtp_host = 'smtp.gmail.com'
        smtp_port = 587
        smtp_user = 'omeiri.abdellah@gmail.com'
        smtp_password = 'xurxjgngdxnffnpo'

        # Connect to the SMTP server
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)

        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = ', '.join(recipient_list)
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        # Send the email
        server.sendmail(from_email, recipient_list, msg.as_string())
        server.quit()

        return JsonResponse({'status': 'success', 'message': 'Code sent successfully'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

def admin_logout(request):
    logout(request)
    # Redirect to the admin login page or another suitable location
    return redirect('/admin/login/?next=/admin/')
def index(request):
    # Your view logic here
    return render(request, 'index.html')

# class TopFournisseur(View):
#     def get(self, request , *args **)
from admin_soft.forms import RegistrationForm, LoginForm, UserPasswordResetForm, UserSetPasswordForm, UserPasswordChangeForm

# def register(request):
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
            
#             # Check if a user with the provided email already exists
#             if users.objects.filter(email=email).exists():
#                 form.add_error('email', 'This email is already in use. Please choose another one.')
#             else:
#                 # Create a new user only if the email is not already registered
#                 form.save()
#                 print('Account created successfully!')
#                 return redirect('/admin/login/?next=/admin/')
#         else:
#             print("Registration failed!")
#     else:
#         form = RegistrationForm()

#     context = {'form': form}
#     return render(request, 'accounts/register.html', context)


def answer_predict(request,notificationId,answer):
    print(answer)
    if answer =="true":
        print("in true")
        state = States.objects.get(pk=1)
        notification = NotificationML.objects.get(pk=notificationId)
        print(notification.itemControlled)
        if notification.itemControlled=="light":
            print("in light condition")
            print(notification.classWantedToApply)
            if notification.classWantedToApply=="0":
                print("in light classWantedToApply 0")
                state.light=False
            else :
                state.light=True
            notification.isread=True
            notification.save()
            state.save()
        elif notification.itemControlled=="weather":
            state.fanLevel=notification.classWantedToApply
            state.save()
        else:
            state.channelOn=notification.classWantedToApply
            state.channelName=""
            state.save()


    return JsonResponse({'status': 'success', 'message': 'Code sent successfully'})

        # elif NotificationML.itemControlled=="weather":
        
        # else:
