import binascii
import os
from datetime import datetime

from django.contrib.auth import login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.cache import cache  # Or use another storage mechanism
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from Sahand import settings
from base.models import Photo, StaticPage, Menu, FaqCategory, Faq
from cms.models import ContentCategory, Blog, Video, Banner, Service, Post
from content_manager.models import ContentManager
from course.models import Course, CourseCategory
from file_manager.models import FileManager
from info.models import WhyUs, Statistic
from utilities.number_generator import generate_random_number
from utilities.sms import send_sms_login
from .forms import PhoneForm, SMSCodeForm
from security.models import User, Operation

import json
from django.utils.dateparse import parse_datetime
from django.db import IntegrityError
from rest_framework.views import APIView

from security.models import User  # Replace 'myapp' with your app name


# from .utils import send_sms_code  # Custom utility to send SMS
def loginUser(request):
    if request.user.is_authenticated:
        return redirect('swagger-ui')
    if request.method == 'POST':
        form = PhoneForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            user = User.objects.filter(phone_number__iexact=phone).first()
            if user is None:
                form.add_error('phone', 'شماره همراه اشتباه است!')
                return redirect('login')
            user.phone_number_code = generate_random_number(4)
            user.save()
            send_sms_login(phone, user.phone_number_code)
            request.session['phone'] = phone
            return redirect('sms_code_entry')
    else:
        form = PhoneForm()

    return render(request, 'home/login.html', {'form': form})


def phone_entry_view(request):
    if request.method == 'POST':
        form = PhoneForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            user = User.objects.filter(phone_number__iexact=phone).first()
            if user is None:
                form.add_error('phone', 'شماره همراه اشتباه است!')
                return render(request, 'home/phone_entry_view.html', {'form': form})
            if not user.is_superuser:
                form.add_error('phone', 'عدم دسترسی!')
                return render(request, 'home/phone_entry_view.html', {'form': form})

            request.session['phone'] = phone
            return redirect('sms_code_entry')
    else:
        form = PhoneForm()

    return render(request, 'home/phone_entry_view.html', {'form': form})


def sms_code_entry_view(request):
    if request.method == 'POST':
        form = SMSCodeForm(request.POST)
        if form.is_valid():
            phone = request.session.get('phone')
            entered_code = form.cleaned_data['sms_code']

            # Dummy SMS code check (replace with your actual SMS code logic)
            user = User.objects.filter(phone_number__iexact=phone).first()
            if user is None:
                form.add_error('sms_code', 'شماره همراه اشتباه است!')
            if not user.is_superuser:
                form.add_error('sms_code', 'عدم دسترسی!')
                return render(request, 'home/sms_code_entry.html', {'form': form})
            if entered_code == user.phone_number_code:
                # Log in the user
                login(request, user)
                return redirect('swagger-ui')

            else:
                messages.error(request, 'Invalid SMS code.')
    else:
        form = SMSCodeForm()

    return render(request, 'home/sms_code_entry.html', {'form': form})


def LogOutView(request):
    """
    Logs out the user, displays a message, and redirects them to a specified page.
    """
    logout(request)
    messages.success(request, "You have successfully logged out.")  # Add a success message
    return redirect('login')


class AddBlogView1(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        successful_count = 0  # To track how many records were saved successfully
        failed_count = 0  # To track how many failed to save
        error_details = []  # To store error details for each failed blog

        # Define the path to the JSON file
        file_path = os.path.join(settings.BASE_DIR, 'data', 'blogs.json')

        try:
            # Open and load the JSON data from the file
            with open(file_path, 'r', encoding='utf-8') as json_file:
                file_data = json.load(json_file)
        except FileNotFoundError:
            return Response({'error': 'JSON file not found.'}, status=400)
        except json.JSONDecodeError:
            return Response({'error': 'Failed to decode JSON file.'}, status=400)

        # Loop through each JSON object and create/update Blog instances
        for blog_entry in Blog.objects.all():
            try:
                blog_entry.blog_type = 1

                blog_entry.save()
                # blog = Blog.objects.get(id=blog_entry['Id'])
                # blog.keywords = blog_entry['Keywords']
                # blog.save()
                # content = ContentManager.objects.get(
                #     id=blog_entry['Id'] + 142)  # Assuming the 'id' of the Blog is the same as the 'id' of the Content
                # StaticPage.objects.create(
                #     id=blog_entry['Id'],
                #     content=content,
                #     static_page_type=None,
                #     status=1
                # )

                successful_count += 1
            except Exception as e:
                failed_count += 1
                error_details.append({
                    "id": blog_entry.get("Id"),
                    "error": str(e)
                })

        # Return a response with counts of successful and failed records, and error details
        return Response({
            "message": "Processing complete",
            "successful_count": successful_count,
            "failed_count": failed_count,
            "error_details": error_details,
        }, status=200)


class AddBlogView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        successful_count = 0  # To track how many records were saved successfully
        failed_count = 0  # To track how many failed to save
        error_details = []  # To store error details for each failed blog

        # Define the path to the JSON file
        file_path = os.path.join(settings.BASE_DIR, 'data', 'post.json')

        try:
            # Open and load the JSON data from the file
            with open(file_path, 'r', encoding='utf-8') as json_file:
                file_data = json.load(json_file)
        except FileNotFoundError:
            return Response({'error': 'JSON file not found.'}, status=400)
        except json.JSONDecodeError:
            return Response({'error': 'Failed to decode JSON file.'}, status=400)

        # Loop through each JSON object and create/update Blog instances
        for blog_entry in file_data:
            try:
                photo_id = None
                if blog_entry["PhotoId"] != 0:
                    photo_id = None if blog_entry["PhotoId"].strip(",") == "0" else blog_entry["PhotoId"].strip(",")

                photo_instance = None
                if photo_id:
                    try:
                        # Assign the Photo instance directly or None if not found
                        photo_instance = FileManager.objects.get(id=photo_id)
                    except ObjectDoesNotExist:
                        photo_instance = None
                video_id = None
                if blog_entry["VideoId"] != 0:
                    video_id = None if blog_entry["VideoId"].strip(",") == "0" else blog_entry["VideoId"].strip(",")

                video_instance = None
                if video_id:
                    try:
                        # Assign the Photo instance directly or None if not found
                        video_instance = FileManager.objects.get(id=video_id)
                    except ObjectDoesNotExist:
                        video_instance = None
                cat = CourseCategory.objects.get(id=2)
                # Create or update the Blog object
                Post.objects.update_or_create(
                    id=blog_entry["Id"],
                    title=blog_entry['Name'],
                    english_title=blog_entry['EnglishName'],
                    photo=photo_instance,
                    video=video_instance,
                    hashtag=blog_entry['Hashtag'],
                    count_view=blog_entry['ViewCount'],
                    count_like=blog_entry['LikeCount'],
                    count_share=blog_entry['ShareCount'],
                    count_comment=blog_entry['CommentCount'],
                    status=1,
                    rate=blog_entry['Rate'],
                    post_type=blog_entry['Type'],
                    is_published=blog_entry['IsPublish'],
                    publish_date=blog_entry["PublishDate"],
                    create_row_date=blog_entry["CreateRowDate"],
                    update_row_date=blog_entry["UpdateRowDate"],
                )

                successful_count += 1
            except Exception as e:
                failed_count += 1
                error_details.append({
                    "id": blog_entry.get("Id"),
                    "error": str(e)
                })

        # Return a response with counts of successful and failed records, and error details
        return Response({
            "message": "Processing complete",
            "successful_count": successful_count,
            "failed_count": failed_count,
            "error_details": error_details,
        }, status=200)

# class AddBlogView(APIView):
#     permission_classes = [AllowAny]
#
#     def post(self, request):
#         successful_count = 0  # To track how many records were saved successfully
#         failed_count = 0  # To track how many failed to save
#         error_details = []  # To store error details for each failed user
#
#         # Define the path to the JSON file
#         file_path = os.path.join(settings.BASE_DIR, 'data', 'csvjson.json')
#
#         try:
#             # Open and load the JSON data from the file
#             with open(file_path, 'r', encoding='utf-8') as json_file:
#                 file_data = json.load(json_file)
#         except FileNotFoundError:
#             return Response({'error': 'JSON file not found.'}, status=400)
#         except json.JSONDecodeError:
#             return Response({'error': 'Failed to decode JSON file.'}, status=400)
#
#         # Define a mapping between JSON fields and Django model fields
#         field_mapping = {
#             "Id": "id",
#             "ConcurrencyStamp": "concurrency_stamp",
#             "SecurityStamp": "security_stamp",
#             "PasswordHash": "password",
#             "NormalizedUserName": "username",
#             "UserName": "username",
#             "PhoneNumber": "phone_number",
#             "UserType": "user_type",
#             "CreateRowDate": "create_row_date",
#             "IsDelete": "is_deleted",
#             "Sex": "sex",
#             "FullName": "full_name",
#             "PasswordText": "password_text",
#             "Telephone": "telephone",
#             "PostalCode": "postal_code",
#             "Address": "address",
#             "PhoneNumberCode": "phone_number_code",
#             "CountSendSMS": "count_send_sms",
#             "LastSendSMS": "last_send_sms",
#             "Status": "status",
#             "Balance": "balance",
#             "PhotoId": "photo_id",
#             "IsSupport": "is_support",
#             "IsConsult": "is_consult",
#             "IsDeveloper": "is_developer",
#             "NationalCode": "national_code",
#             "Job": "job",
#             "Education": "education",
#             "UrlName": "url_name",
#             "EmailConfirmed": "email_confirmed",
#             "PhoneNumberConfirmed": "phone_number_confirmed",
#             "TwoFactorEnabled": "two_factor_enabled",
#             "LockoutEnabled": "lockout_enabled",
#             "AccessFailedCount": "access_failed_count",
#         }
#
#         # Loop through each JSON object and create/update User instances
#         for user_entry in file_data:
#             try:
#                 # Map JSON fields to model fields
#                 mapped_data = {field_mapping[key]: value for key, value in user_entry.items() if key in field_mapping}
#
#                 # Parse datetime fields (if needed)
#                 if "create_row_date" in mapped_data:
#                     mapped_data["create_row_date"] = parse_datetime(mapped_data["create_row_date"])
#                 if "last_send_sms" in mapped_data:
#                     mapped_data["last_send_sms"] = parse_datetime(mapped_data["last_send_sms"])
#
#                 # Increment the id by 2
#                 mapped_data["id"] = mapped_data.get("id")
#
#                 # Create or update the User object
#                 User.objects.update_or_create(
#                     id=mapped_data["id"],
#                     defaults=mapped_data,
#                 )
#                 successful_count += 1
#             except Exception as e:
#                 failed_count += 1
#                 error_details.append({
#                     "id": user_entry.get("Id"),
#                     "error": str(e)
#                 })
#
#         # Return a response with counts of successful and failed records, and error details
#         return Response({
#             "message": "Processing complete",
#             "successful_count": successful_count,
#             "failed_count": failed_count,
#             "error_details": error_details,
#         }, status=200)
