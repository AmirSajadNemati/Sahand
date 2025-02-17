from datetime import datetime


from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from base.models import SiteInfo, PageSeo, Menu, Photo, ContactInfo, StaticContent
from base.serializers import ContactInfoSerializer
from base_api.serializers import ServerTimeSerializer, PanelInfoResponseSerializer, AppInfoResponseSerializer, \
    AppAuthorizeResponseSerializer, GetSiteInfoRequestSerializer, SearchPanelRequestSerializer
from security.models import Operation, Role
from security.serializers import OperationSerializer
from task_manager.models import Notification


class ShowServerTimeView(APIView):
    @extend_schema(
        request=None,
        responses={200: OpenApiResponse(response=ServerTimeSerializer())},
        description="Show Server Time"
    )
    def post(self, request):
        # Get the current server date and time
        current_datetime = datetime.now()

        # Prepare the data for serialization
        data = {
            'time': current_datetime.time(),  # Get the time part
            'date': current_datetime.date()  # Get the date part
        }

        # Create a response using the serializer
        serializer = ServerTimeSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

# @method_decorator(role_decorator, name='post')
class GetPanelInfoView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=None,
        responses={200: OpenApiResponse(response=PanelInfoResponseSerializer())},
        description="Show Panel Information"
    )

    def post(self, request):
        is_authorized = request.user.is_authenticated
        role_id = request.headers.get('roleId')
        # Get site info
        site_info = SiteInfo.objects.first()  # Get the first SiteInfo or None

        # Prepare appVersion data
        app_version_data = {
            'year': 2024,  # Replace with actual logic for version year
            'version': 1,  # Replace with actual version logic
            'versionShow': '1.0.0',  # Replace with actual version display logic
            'requierdUpdate': False,  # Set according to your logic
            'downloadList': [
                {
                    'photo': 1,
                    'title': 'App Download',
                    'url': 'https://example.com/download'
                }
            ]
        }

        # Prepare appColor data from SiteInfo, handling missing attributes
        app_color_data = {
            'lightBaseColor': getattr(site_info, 'light_base_color', None),
            'lightSecondColor': getattr(site_info, 'light_second_color', None),
            'lightTextColor': getattr(site_info, 'light_text_color', None),
            'lightBoxColor': getattr(site_info, 'light_box_color', None),
            'lightBgColor': getattr(site_info, 'light_bg_color', None),
            'lightThirdColor': getattr(site_info, 'light_third_color', None),
            'darkBaseColor': getattr(site_info, 'dark_base_color', None),
            'darkSecondColor': getattr(site_info, 'dark_second_color', None),
            'darkTextColor': getattr(site_info, 'dark_text_color', None),
            'darkBoxColor': getattr(site_info, 'dark_box_color', None),
            'darkBgColor': getattr(site_info, 'dark_bg_color', None),
            'darkThirdColor': getattr(site_info, 'dark_third_color', None),
        }

        # Prepare the user profile

        role = Role.objects.filter(id=role_id).first()
        features_selected = role.features_selected if role else []

        # Function to build tree-like structure with nested children
        def build_feature_tree(features):
            nodes = {}
            tree = []

            # Create a dictionary of nodes
            for feature in features:
                nodes[feature['id']] = {**feature, 'children': []}

            # Organize features into a tree structure
            for feature in features:
                if feature['parent'] is not None:
                    # Add to parent's children if the feature has a parent
                    nodes[feature['parent']]['children'].append(nodes[feature['id']])
                else:
                    # If no parent, it's a root node, so add it to the tree
                    tree.append(nodes[feature['id']])

            return tree

        # Build the nested features
        filtered_features = [feature for feature in features_selected if not feature.get('isSubMenu', False)]

        # Build the nested features tree
        nested_features = build_feature_tree(filtered_features)

        # Prepare developer info, handling missing attributes
        developer_data = {
            'logo': getattr(site_info.developer_logo, 'id', None) if site_info and site_info.developer_logo else None,
            'name': getattr(site_info, 'developer_title', None),
            'englishTitle': getattr(site_info, 'developer_english_title', None),
            'url': getattr(site_info, 'developer_url', None)
        }

        appInfo = {
            "logo": getattr(site_info.logo, 'id', None) if site_info and site_info.logo else None,
            "name": getattr(site_info, 'title', None),
            "slogan": getattr(site_info, 'slogan', None),
            "footerLogo": getattr(site_info.logo, 'id', None) if site_info and site_info.logo else None,
            "englishTitle": getattr(site_info, 'english_title', None),
            "smallLogo": getattr(site_info.small_logo, 'id', None) if site_info and site_info.small_logo else None,
            "whiteLogo": getattr(site_info.white_logo, 'id', None) if site_info and site_info.white_logo else None
        }
        current_datetime = datetime.now()
        # Create the response data
        if not is_authorized:
            # If user is not authenticated, return a response with only isAuthorize
            current_datetime = datetime.now()
            response_data = {
                'isAuthorize': False,
                'appInfo': appInfo,
                'appVersion': app_version_data,
                'appColor': app_color_data,
                'profile': None,
                'features_selected': [],  # Ensure it's an empty list if no menus
                'developer': developer_data,
                'serverTime': {
                    'time': current_datetime.time(),  # Get the time part
                    'date': current_datetime.date()  # Get the date part
                }
            }
            return Response(response_data, status=status.HTTP_200_OK)
        user = request.user  # Get the logged-in user from the request
        count_not_read_message = 0
        if is_authorized:
            count_not_read_message = Notification.objects.filter(
                send_to__contains=[user.id], is_read=False
            ).count()
        profile_data = {
            'userName': getattr(user, 'username', None),
            'fullName': getattr(user, 'full_name', None),
            'fullNameWithSex': f"{getattr(user, 'full_name', '')} ({getattr(user, 'sex', 'N/A')})" if user.full_name and user.sex else None,
            'phoneNumber': getattr(user, 'phone_number', None),
            'photo': getattr(user.photo, 'id', None) if user.photo else None,  # Return FileManager ID
            'balance': getattr(user, 'balance', 0),
            'inviteCount': 0,  # Example static value
            'id': getattr(user, 'id', None),
        }
        response_data = {
            'isAuthorize': True,
            'appInfo': appInfo,
            'appVersion': app_version_data,
            'appColor': app_color_data,
            'profile': profile_data,
            'features_selected': nested_features or [],  # Ensure it's an empty list if no menus
            'developer': developer_data,
            'serverTime': {
                'time': current_datetime.time(),  # Get the time part
                'date': current_datetime.date()  # Get the date part
            },
            'countNotReadMessage': count_not_read_message
        }

        # Create the final serializer
        serializer = PanelInfoResponseSerializer(data=response_data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class GetAppInfoView(APIView):
    @extend_schema(
        request=None,
        responses={200: OpenApiResponse(response=AppAuthorizeResponseSerializer())},
        description="Get App Information"
    )
    def post(self, request):
        # Check if the user is authenticated
        is_authorized = request.user.is_authenticated

        if not is_authorized:
            # If user is not authenticated, return response with all fields as null
            response_data = {
                'isAuthorize': False,
                'appInfo': None,
                'appVersion': None,
                'appColor': None,
                "profile": None
            }
            return Response(response_data, status=status.HTTP_200_OK)

        # If user is authenticated, get site info and other data
        site_info = SiteInfo.objects.first()  # Get the first SiteInfo or None

        # Prepare appInfo data

        appInfo = {
            "logo": getattr(site_info.logo, 'id', None) if site_info and site_info.logo else None,
            "name": getattr(site_info, 'title', None),
            "slogan": getattr(site_info, 'slogan', None),
            "footerLogo": getattr(site_info.logo, 'id', None) if site_info and site_info.logo else None,
            "englishTitle": getattr(site_info, 'english_title', None),
            "smallLogo": getattr(site_info.small_logo, 'id', None) if site_info and site_info.small_logo else None,
            "whiteLogo": getattr(site_info.white_logo, 'id', None) if site_info and site_info.white_logo else None
        }

        # Prepare appVersion data
        app_version_data = {
            'year': 2024,  # Replace with actual logic for version year
            'version': 1,  # Replace with actual version logic
            'versionShow': '1.0.0',  # Replace with actual version display logic
            'requiredUpdate': False,  # Set according to your logic
            'downloadList': [
                {
                    'photo': 1,
                    'title': 'App Download',
                    'url': 'https://example.com/download'
                }
            ]
        }

        # Prepare appColor data from SiteInfo, handling missing attributes
        app_color_data = {
            'lightBaseColor': getattr(site_info, 'light_base_color', None),
            'lightSecoundColor': getattr(site_info, 'light_second_color', None),
            'lightTextColor': getattr(site_info, 'light_text_color', None),
            'lightBoxColor': getattr(site_info, 'light_box_color', None),
            'lightBgColor': getattr(site_info, 'light_bg_color', None),
            'lightThirdColor': getattr(site_info, 'light_third_color', None),
            'darkBaseColor': getattr(site_info, 'dark_base_color', None),
            'darkSecoundColor': getattr(site_info, 'dark_second_color', None),
            'darkTextColor': getattr(site_info, 'dark_text_color', None),
            'darkBoxColor': getattr(site_info, 'dark_box_color', None),
            'darkBgColor': getattr(site_info, 'dark_bg_color', None),
            'darkThirdColor': getattr(site_info, 'dark_third_color', None),
        }

        # Prepare profile data for the logged-in user
        user = request.user
        profile_data = {
            'userName': getattr(user, 'username', None),
            'fullName': getattr(user, 'full_name', None),
            'fullNameWithSex': f"{getattr(user, 'full_name', '')} ({getattr(user, 'sex', 'N/A')})" if user.full_name and user.sex else None,
            'phoneNumber': getattr(user, 'phone_number', None),
            'photo': getattr(user.photo, 'id', None) if user.photo else None,  # Return FileManager ID
            'balance': getattr(user, 'balance', 0),
            'inviteCount': 0,  # Example static value
            'id': getattr(user, 'id', None),
        }

        # Create the response data
        response_data = {
            'isAuthorize': True,
            'appInfo': appInfo,
            'appVersion': app_version_data,
            # 'appPushNotification': app_push_notification_data,
            'appColor': app_color_data,
            'profile': profile_data,
        }

        # Create the final serializer
        serializer = AppInfoResponseSerializer(data=response_data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class GetAuthorizeInfoView(APIView):
    @extend_schema(
        request=None,
        responses={200: OpenApiResponse(response=AppInfoResponseSerializer())},
        description="Get App Information"
    )
    def post(self, request):
        # Check if the user is authenticated
        is_authorized = request.user.is_authenticated

        if not is_authorized:
            # If user is not authenticated, return response with all fields as null
            response_data = {
                'isAuthorize': False,
                'appInfo': None,
                'appVersion': None,
                'appColor': None,
                "loginText": "string",
                "loginPhotoLight": "string",
                "loginPhotoDark": "string"

            }
            return Response(response_data, status=status.HTTP_200_OK)

        # If user is authenticated, get site info and other data
        site_info = SiteInfo.objects.first()  # Get the first SiteInfo or None

        # Prepare appInfo data
        appInfo = {
            "logo": getattr(site_info.logo, 'id', None) if site_info and site_info.logo else None,
            "name": getattr(site_info, 'title', None),
            "slogan": getattr(site_info, 'slogan', None),
            "footerLogo": getattr(site_info.logo, 'id', None) if site_info and site_info.logo else None,
            "englishTitle": getattr(site_info, 'english_title', None),
            "smallLogo": getattr(site_info.small_logo, 'id', None) if site_info and site_info.small_logo else None,
            "whiteLogo": getattr(site_info.white_logo, 'id', None) if site_info and site_info.white_logo else None
        }

        # Prepare appVersion data
        app_version_data = {
            'year': 2024,  # Replace with actual logic for version year
            'version': 1,  # Replace with actual version logic
            'versionShow': '1.0.0',  # Replace with actual version display logic
            'requiredUpdate': False,  # Set according to your logic
            'downloadList': [
                {
                    'photo': 'https://example.com/photo.png',
                    'title': 'App Download',
                    'url': 'https://example.com/download'
                }
            ]
        }

        # Prepare appColor data from SiteInfo, handling missing attributes
        app_color_data = {
            'lightBaseColor': getattr(site_info, 'light_base_color', None),
            'lightSecoundColor': getattr(site_info, 'light_second_color', None),
            'lightTextColor': getattr(site_info, 'light_text_color', None),
            'lightBoxColor': getattr(site_info, 'light_box_color', None),
            'lightBgColor': getattr(site_info, 'light_bg_color', None),
            'lightThirdColor': getattr(site_info, 'light_third_color', None),
            'darkBaseColor': getattr(site_info, 'dark_base_color', None),
            'darkSecoundColor': getattr(site_info, 'dark_second_color', None),
            'darkTextColor': getattr(site_info, 'dark_text_color', None),
            'darkBoxColor': getattr(site_info, 'dark_box_color', None),
            'darkBgColor': getattr(site_info, 'dark_bg_color', None),
            'darkThirdColor': getattr(site_info, 'dark_third_color', None),
        }

        # Prepare profile data for the logged-in user
        user = request.user
        # Create the response data
        response_data = {
            'isAuthorize': True,
            'appInfo': appInfo,
            'appVersion': app_version_data,
            # 'appPushNotification': app_push_notification_data,
            'appColor': app_color_data,
            "loginText": "string",
            "loginPhotoLight": "string",
            "loginPhotoDark": "string"
        }

        # Create the final serializer
        serializer = AppInfoResponseSerializer(data=response_data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class GetSiteInfoView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=GetSiteInfoRequestSerializer,
        responses={200: OpenApiResponse(response=AppInfoResponseSerializer())},
        description="Get App Information"
    )
    def post(self, request):
        url = request.data.get('url')  # Get the URL from the request

        # Fetch SEO information based on the provided URL
        seo_info = PageSeo.objects.filter(url=url).first()

        # Prepare SEO data
        seo_data = {
            "title": getattr(seo_info, 'title', None),
            "description": getattr(seo_info, 'description', None),
            "robot": getattr(seo_info, 'robot', None),
            "keyword": getattr(seo_info, 'keywords', None),
            "favIcon": "/fav.ico",  # Static value
            "touchIcon": "/smalllogo.png",  # Static value
            "baseColor": "#674ea7",  # Static value
            "charset": "UTF-8",  # Static value
            "language": "fa",  # Static value
            "copyright": "orod.co",  # Static value
            "headerTops": [],  # Static value
            "headerBottoms": [],  # Static value
            "bodyTops": [],  # Static value
            "bodyBottoms": []  # Static value
        }

        # Prepare menu data
        header_menu = self.get_menu_data(menu_type=1)
        responsive_menu = self.get_menu_data(menu_type=2)
        mega_menu = self.get_menu_data(menu_type=3)
        footer_menu1 = self.get_menu_data(menu_type=4)
        footer_menu2 = self.get_menu_data(menu_type=5)
        footer_menu3 = self.get_menu_data(menu_type=6)

        # Static data
        footer_text = None  # Default to None in case no matching content is found

        try:
            # Retrieve the footer content based on the content type
            footer_content = StaticContent.objects.filter(
                static_content_type=2,  # 2 corresponds to Footer in your choices
                is_deleted=False  # Ensure the content is not marked as deleted
            ).first()

            if footer_content and footer_content.content:
                footer_text = footer_content.content.content  # Adjust field (e.g., `title`) as per your ContentManager model
        except StaticContent.DoesNotExist:
            # Handle case where no content is found
            footer_text = "Default footer text"  # Provide fallback text
        address = "در انتظار تکمیل"  # Manually filled address

        contact_details = ContactInfo.objects.all()
        contact_detail_serialized = ContactInfoSerializer(contact_details, many=True).data

        # Prepare app info
        site_info = SiteInfo.objects.first()
        appInfo = {
            "logo": getattr(site_info.logo, 'id', None) if site_info and site_info.logo else None,
            "name": getattr(site_info, 'title', None),
            "slogan": getattr(site_info, 'slogan', None),
            "footerLogo": getattr(site_info.logo, 'id', None) if site_info and site_info.logo else None,
            "englishTitle": getattr(site_info, 'english_title', None),
            "smallLogo": getattr(site_info.small_logo, 'id', None) if site_info and site_info.small_logo else None,
            "whiteLogo": getattr(site_info.white_logo, 'id', None) if site_info and site_info.white_logo else None
        }

        # Prepare app version data
        app_version_data = {
            "year": 1403,  # Example static year
            "version": 100,  # Example static version
            "versionShow": "1.0.0",  # Example static version display
            "requierdUpdate": False,
            "downloadList": []  # Static download list
        }

        # Prepare app color data
        app_color_data = {
            "lightBaseColor": getattr(site_info, "light_base_color", None) if site_info else None,
            "lightSecoundColor": getattr(site_info, "light_second_color", None) if site_info else None,
            "lightTextColor": getattr(site_info, "light_text_color", None) if site_info else None,
            "lightBoxColor": getattr(site_info, "light_box_color", None) if site_info else None,
            "lightBgColor": getattr(site_info, "light_bg_color", None) if site_info else None,
            "lightThirdColor": getattr(site_info, "light_third_color", None) if site_info else None,
            "darkBaseColor": getattr(site_info, "dark_base_color", None) if site_info else None,
            "darkSecoundColor": getattr(site_info, "dark_second_color", None) if site_info else None,
            "darkTextColor": getattr(site_info, "dark_text_color", None) if site_info else None,
            "darkBoxColor": getattr(site_info, "dark_box_color", None) if site_info else None,
            "darkBgColor": getattr(site_info, "dark_bg_color", None) if site_info else None,
            "darkThirdColor": getattr(site_info, "dark_third_color", None) if site_info else None,
        }

        # Prepare sliders (photos) data
        photo_type_dict = dict(Photo.photo_type_choices)

        sliders = {}
        for photo_type in range(1, 6):  # Photo types from 1 to 5
            photos = Photo.objects.filter(photo_type=photo_type, is_deleted=False)

            # Get the human-readable name for the photo_type
            photo_type_name = photo_type_dict.get(photo_type)

            # Add to the sliders dictionary using the human-readable name as the key
            sliders[photo_type_name] = [{
                "id": photo.id,
                "title": photo.title,
                "url": photo.url,
                "file": getattr(photo.file, 'id', None) if photo.file else None
            } for photo in photos]

        # Prepare profile data (assuming the user is authenticated)
        if request.user.is_authenticated:
            profile_data = {
                "userName": getattr(request.user, "username", None),
                "fullName": getattr(request.user, "full_name", None),
                "fullNameWithSex": f"{getattr(request.user, 'full_name', '')} ({getattr(request.user, 'sex', 'N/A')})" if request.user.full_name and request.user.sex else None,
                "phoneNumber": getattr(request.user, "phone_number", None),
                "photo": getattr(request.user.photo, "id", None) if request.user.photo else None,
                "balance": getattr(request.user, "balance", 0),
                "inviteCount": 0,
                "id": getattr(request.user, "id", None),
            }
        else:
            profile_data = {}

        developer_data = {
            "logo": getattr(site_info.developer_logo, "id", None) if site_info and site_info.developer_logo else None,
            "name": getattr(site_info, "developer_title", None),
            "englishTitle": getattr(site_info, "developer_english_title", None),
            "url": getattr(site_info, "developer_url", None)
        }

        # Create the response data
        response_data = {
            "HeaderMenu": header_menu,
            "ResponsiveMenu": responsive_menu,
            "MegaMenu": mega_menu,
            "FooterMenu1": footer_menu1,
            "FooterMenu2": footer_menu2,
            "FooterMenu3": footer_menu3,
            "footerText": footer_text,
            "address": address,
            "contactDetail": contact_detail_serialized,
            "isAuthorize": request.user.is_authenticated,
            "appInfo": appInfo,
            "appVersion": app_version_data,
            "appColor": app_color_data,
            "profile": profile_data,
            "seo": seo_data,
            "developer": developer_data,
            "sliders": sliders
        }

        return Response(response_data, status=status.HTTP_200_OK)

    def get_menu_data(self, menu_type):
        # Fetch menus based on the menu type
        menus = Menu.objects.filter(menu_type=menu_type).order_by("order")
        menu_list = []

        for menu in menus:
            menu_item = {
                "title": menu.title,
                "url": menu.url,
                "icon": getattr(menu.icon, "id", None),
                "icon_name": menu.icon_name,
                "icon_lib": menu.icon_lib,
                "children": []  # Assuming no child menus; modify if needed
            }
            menu_list.append(menu_item)

        return menu_list



class SearchPanelMenuView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=SearchPanelRequestSerializer,
        responses={200: OpenApiResponse(response=OperationSerializer(many=True))},
        description="Get App Information"
    )
    def post(self, request):

        title = request.data.get('title')
        role_id = request.headers.get('roleId')

        if not title:
            return Response({"message": "عنوان را وارد کنید!"}, status=status.HTTP_400_BAD_REQUEST)

        role = Role.objects.get(id=role_id)
        features_selected = []
        if role:
            for item in role.features_selected:
                if item.get('operation_type') != 2 and title in item.get('title', ''):
                    features_selected.append(item)
        else:
            return Response({"message": "نقش یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(features_selected, status=status.HTTP_200_OK)

