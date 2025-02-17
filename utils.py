import re

import jwt
from django.core.exceptions import FieldDoesNotExist
from functools import wraps

from rest_framework import status
from rest_framework.response import Response

from Sahand import settings
from security.models import Role, User


# def role_decorator(func):
#     @wraps(func)
#     def wrapper(view, request, *args, **kwargs):
#         return func(view, request, *args, **kwargs)
#
#     return wrapper


def role_decorator(func):
    @wraps(func)
    def wrapper(view, request, *args, **kwargs):
        role_id = request.headers.get('roleId')
        path = request.path
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith("Bearer "):
            return Response({"error": "Authorization token missing or invalid."}, status=401)

        token = auth_header.split(" ")[1]

        try:
            # Decode the JWT
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

            # Check if the user is a superuser
            user_id = decoded_token.get('user_id')
            is_superuser = User.objects.get(id=user_id).is_superuser

            if is_superuser:
                return func(view, request, *args, **kwargs)

        except jwt.ExpiredSignatureError:
            return Response({"error": "Token has expired."}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({"error": "Invalid token."}, status=status.HTTP_401_UNAUTHORIZED)
        if role_id is None:
            return Response({"message": "request closed, invalid role!"}, status=status.HTTP_403_FORBIDDEN)
        try:
            role_id = int(role_id)
        except Exception:
            return Response({"message": "request closed, invalid role!!"}, status=status.HTTP_403_FORBIDDEN)

        if int(role_id) not in request.user.roles:
            return Response({"message": "request closed, user has no such role!"}, status=status.HTTP_403_FORBIDDEN)

        # Your original code with trailing slash handling
        pattern = r'^(.*?)(List|Get|AddOrUpdate|Delete|UnDelete)$'

        # Strip the trailing slash if present for proper matching
        path_without_trailing_slash = path.rstrip('/')

        match = re.search(pattern, path_without_trailing_slash)

        if match:
            # Extract path and API name based on the regex match
            new_path = match.group(1)  # Path in lowercase
            api_name = match.group(2)  # Extracted API name
        else:
            # Default case if no match, return path as is and no API name
            new_path = path
            api_name = None

        print(f"New Path: {new_path}")
        print(f"API Name: {api_name}")

        role = Role.objects.get(id=role_id)
        features_selected = role.features_selected

        # Check if new_path exists in any of the selected URLs
        url_exists = any(feature['url'] == new_path for feature in features_selected)
        feature = next((feature for feature in features_selected if feature['url'] == new_path), None)

        if not url_exists:
            return Response({"message": "request closed1"}, status=status.HTTP_403_FORBIDDEN)
        # List
        if api_name == 'List':
            if not feature.get('isViewList'):
                return Response({"message": "request closed"}, status=status.HTTP_403_FORBIDDEN)
        # Get
        elif api_name == 'Get':
            if not feature.get('isView'):
                return Response({"message": "request closed"}, status=status.HTTP_403_FORBIDDEN)
        # Delete (soft & hard)
        elif api_name == 'Delete':
            if not feature.get('isDelete'):
                return Response({"message": "request closed"}, status=status.HTTP_403_FORBIDDEN)
            delete_type = request.data.get('type')
            # type 1, 2 => soft-delete
            if delete_type == 1 or delete_type == 2:
                if not feature.get('isSoftDelete'):
                    return Response({"message": "request closed"}, status=status.HTTP_403_FORBIDDEN)
            # type 3,4 => hard-delete
            if delete_type == 3 or delete_type == 4:
                if not feature.get('isHardDelete'):
                    return Response({"message": "request closed"}, status=status.HTTP_403_FORBIDDEN)
        # UnDelete
        elif api_name == 'UnDelete':
            if not feature.get('isUnDelete'):
                return Response({"message": "request closed"}, status=status.HTTP_403_FORBIDDEN)
        elif api_name == 'AddOrUpdate':
            object_id = request.data.get('id')
            if object_id == 0:
                if not feature.get('isAdd'):
                    return Response({"message": "request closed"}, status=status.HTTP_403_FORBIDDEN)
            else:
                if not feature.get('isEdit'):
                    return Response({"message": "request closed"}, status=status.HTTP_403_FORBIDDEN)

        return func(view, request, *args, **kwargs)

    return wrapper


def create_property_attribute(order, property_name, property_type, enums_select,
                              is_enum, is_enum_list, is_fk, fk_url, fk_level, fk_level_end,
                              fk_parent, fk_show, fk_multiple, is_file, file_types,
                              file_url, file_multiple, is_read_only, is_not_show,
                              is_hidden, date_type, is_date, is_color, is_price,
                              price_type, is_tag, is_editor, editor_type, is_location,
                              is_list, list_property, list_error, location_type, display_name):
    return {
        "order": order,
        "propertyName": property_name,
        "propertyType": property_type,
        "enumsSelect": enums_select,
        "isEnum": is_enum,
        "isEnumList": is_enum_list,
        "isFK": is_fk,
        "fkUrl": fk_url,
        "fkLevel": fk_level,
        "fkLevelEnd": fk_level_end,
        "fkParent": fk_parent,
        "fkShow": fk_show,
        "fkMultiple": fk_multiple,
        "isFile": is_file,
        "fileTypes": file_types,
        "fileUrl": file_url,
        "fileMultiple": file_multiple,
        "isReadOnly": is_read_only,
        "isNotShow": is_not_show,
        "isHidden": is_hidden,
        "dateType": date_type,
        "isDate": is_date,
        "isColor": is_color,
        "isPrice": is_price,
        "priceType": price_type,
        "isTag": is_tag,
        "isEditor": is_editor,
        "editorType": editor_type,
        "isLocation": is_location,
        "isList": is_list,
        "listProperty": list_property,
        "listError": list_error,
        "locationType": location_type,
        "attribute": [
            {
                "type": "DisplayAttribute",
                "value": display_name,
                "message": None
            }
        ]
    }


def get_property_type(model, field_name):
    # Retrieve the field from the model
    try:
        field = model._meta.get_field(field_name)
    except FieldDoesNotExist:
        return 'Unknown'

    # Map Django field types to your desired types
    field_type_mapping = {
        'IntegerField': 'System.Int32',
        'BigIntegerField': 'System.Int64',
        'CharField': 'System.String',
        'TextField': 'System.String',
        'BooleanField': 'System.Boolean',
        'DateTimeField': 'System.DateTime',
        'FloatField': 'System.Single',
        # Add any other necessary mappings
    }

    # Return the corresponding type or 'Unknown' if not found
    return field_type_mapping.get(field.get_internal_type(), 'Unknown')


def duration_maker(duration):
    """Convert a DurationField (timedelta) to HH:MM:SS format."""
    if duration:
        total_seconds = int(duration.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    return None
