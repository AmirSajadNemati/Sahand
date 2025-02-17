from django.http import HttpResponse, Http404
from django.shortcuts import render

# Create your views here.
import mimetypes
# region BaseData
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from file_manager.models import FileManager
from file_manager.serializers import FileManagerSearchSerializer, ResponseDataSerializer, FileAndFolderSerializer, \
    FileManagerBaseDataSerializer, FileManagerSerializer, MessageResponseSerializer


class FileManagerBaseDataView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=None,
        responses={
            200: OpenApiResponse(response=FileManagerBaseDataSerializer),
        },
        description="Add or Update DeviceType"
    )
    def post(self, request):
        total_size = 0  # محاسبه اندازه کلی فضای استفاده‌شده
        used_size = 0  # محاسبه فضای استفاده‌شده
        total_file = FileManager.objects.filter(is_folder=False).count()
        total_folder = FileManager.objects.filter(is_folder=True).count()

        file_types = [
            {"value": 1, "label": "File", "extension": ".*"},
            {"value": 2, "label": "Folder", "extension": ""}
        ]

        base_data = {
            "totalSize": total_size,
            "totalSizeValue": f"{total_size} MB",
            "usedSize": used_size,
            "usedSizeValue": f"{used_size} MB",
            "totalFile": total_file,
            "totalFolder": total_folder,
            "fileTypes": file_types,
        }

        return Response(base_data)


# endregion

# region get data
class FileManagerGetDataView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=FileManagerSearchSerializer,
        responses={
            200: OpenApiResponse(
                response=ResponseDataSerializer
            )
        },
        description="دریافت داده‌های فایل‌ها و پوشه‌ها"
    )
    def post(self, request):
        search = request.data.get('search', '')
        url = request.data.get('url', '')  # Parent path
        file_type = request.data.get('fileType', 1)

        if url:
            files = FileManager.objects.filter(parentUrl=url)
        else:
            files = FileManager.objects.filter(parentUrl='/')

        if file_type == 2:
            files = files.filter(is_folder=True)
        elif file_type == 3:
            files = files.filter(is_folder=False)
        if search:
            files = files.filter(name__icontains=search)

        file_and_folders = FileAndFolderSerializer(files, many=True).data
        breadcrumbs = self.get_breadcrumbs(url)

        response_data = {
            "url": url,
            "breadCrumbs": breadcrumbs,
            "fileAndFolders": file_and_folders,
            "baseData": FileManagerBaseDataView().post(request).data,
        }
        return Response(response_data)

    def get_breadcrumbs(self, path):
        breadcrumbs = []
        if path:
            parts = path.strip("/").split("/")
            for i in range(len(parts)):
                breadcrumbs.append({"name": parts[i], "url": "/".join(parts[: i + 1])})
        return breadcrumbs

    def get_folder_by_path(self, path):
        """
        Resolves the folder instance based on the given parentUrl path.
        """
        path = path.strip("/")  # Clean up leading/trailing slashes
        if not path:
            return None  # Root folder
        try:
            # Attempt to retrieve the folder by matching the full path
            return FileManager.objects.get(parentUrl=path, is_folder=True)
        except FileManager.DoesNotExist:
            return None


# endregion

# region AddFile
class FileManagerAddFileView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [AllowAny]

    def post(self, request):
        parent_url = request.data.get('parentUrl', None)
        file = request.FILES.get('file')

        if not file:
            return Response({"message": "فایل ارسال نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        # Validate the parent URL
        if not parent_url or parent_url == "":
            parent_url = "/"  # If empty, set to "/"
        elif not parent_url.endswith("/"):
            parent_url = parent_url + "/"  # Ensure '/' is at the end

        # Check for duplicate file names
        if FileManager.objects.filter(name=file.name, parentUrl=parent_url).exists():
            return Response({"message": "فایل با همچین نامی موجود است!"},
                            status=status.HTTP_400_BAD_REQUEST)

        file_instance = FileManager(name=file.name, parentUrl=parent_url, is_folder=False)
        file_instance.save_file(file)

        return Response({"message": "فایل با موفقیت ارسال شد!", "id": file_instance.id}, status=status.HTTP_200_OK)



# endregion

# region EditFile
class FileManagerEditFileView(APIView):
    @extend_schema(
        request=FileManagerSerializer,
        responses={200: OpenApiResponse(response=MessageResponseSerializer)},
        description="Edit the name of a file."
    )
    def post(self, request):
        file_id = request.data.get('id', None)
        new_name = request.data.get('name', None)

        if not file_id or not new_name:
            return Response({"message": "نام جدید و شناسه ی فایل را وارد کنید."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            file_instance = FileManager.objects.get(id=file_id, is_folder=False)
        except FileManager.DoesNotExist:
            return Response({"message": "فایل یافت نشد."}, status=status.HTTP_404_NOT_FOUND)

        # Ensure no duplicate file names
        if FileManager.objects.filter(name=new_name, parent=file_instance.parent).exists():
            return Response({"message": "قایلی با همین اسم در این مکان وجود دارد! "},
                            status=status.HTTP_400_BAD_REQUEST)

        # Update the file name
        file_instance.name = new_name
        file_instance.save()
        print(file_instance.get_file_data)
        return Response({"message": "فایل با موفقیت ویرایش شد!"}, status=status.HTTP_200_OK)


# endregion
class FileManagerShowFileView(APIView):
    permission_classes = [AllowAny]  # Adjust this based on your needs

    def get(self, request, file_id):
        try:
            # Retrieve the file object from the database
            file_instance = FileManager.objects.get(pk=file_id, is_folder=False)

            # Use the file_extension to guess the MIME type
            mime_type = mimetypes.types_map.get(file_instance.file_extension,
                                                'application/octet-stream')  # Fallback to a binary type

            # Prepare the response with the file's binary data
            response = HttpResponse(file_instance.file_data, content_type=mime_type)

            # Set the content-disposition header to prompt download with the original file name
            response['Content-Disposition'] = f'attachment; filename="{file_instance.name}"'

            return response

        except FileManager.DoesNotExist:
            return Response({"message": "فایل یافت نشد"}, status=status.HTTP_400_BAD_REQUEST)


class FileManagerAddOrUpdateFolderView(APIView):
    def post(self, request):
        parent_url = request.data.get('parentUrl', '/')
        name = request.data.get('name')
        folder_id = request.data.get('id', 0)

        if not name:
            return Response({"message": "Folder name is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure parent_url ends with '/'
        if not parent_url or parent_url == "":
            parent_url = "/"  # If empty, set to "/"
        elif not parent_url.endswith("/"):
            parent_url = parent_url + "/"  # Ensure '/' is at the end

        if folder_id == 0:  # Create new folder
            if FileManager.objects.filter(name=name, parentUrl=parent_url, is_folder=True).exists():
                return Response({"message": "A folder with this name already exists."},
                                status=status.HTTP_400_BAD_REQUEST)
            folder = FileManager.objects.create(name=name, parentUrl=parent_url, is_folder=True)
            return Response({"message": "Folder created successfully!", "id": folder.id}, status=status.HTTP_200_OK)
        else:  # Update existing folder
            try:
                folder = FileManager.objects.get(id=folder_id, is_folder=True)
            except FileManager.DoesNotExist:
                return Response({"message": "Folder not found."}, status=status.HTTP_404_NOT_FOUND)

            if FileManager.objects.filter(name=name, parentUrl=folder.parentUrl, is_folder=True).exclude(
                    id=folder_id).exists():
                return Response({"message": "A folder with this name already exists."},
                                status=status.HTTP_400_BAD_REQUEST)

            folder.name = name
            folder.save()
            return Response({"message": "Folder updated successfully!"}, status=status.HTTP_200_OK)


class FileManagerDeleteFileAndFolderView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=None,
        responses={200: OpenApiResponse(response=MessageResponseSerializer)},
        description="Physically delete a file or a folder. Folders can only be deleted if they have no child elements."
    )
    def post(self, request):
        file_or_folder_id = request.data.get('id', None)

        if not file_or_folder_id:
            return Response({"message": "شناسه فایل یا پوشه را وارد کنید."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Retrieve the file or folder object
            file_or_folder = FileManager.objects.get(id=file_or_folder_id)
        except FileManager.DoesNotExist:
            return Response({"message": "فایل یا پوشه یافت نشد."}, status=status.HTTP_404_NOT_FOUND)

        # Handle folder deletion
        if file_or_folder.is_folder:
            # Check if the folder is empty
            if file_or_folder.children.exists():
                return Response({"message": "این پوشه دارای فایل‌ها یا پوشه‌های دیگر است و نمی‌تواند حذف شود."},
                                status=status.HTTP_400_BAD_REQUEST)

            # Delete the folder entry from the database
            file_or_folder.delete()
            return Response({"message": "پوشه با موفقیت حذف شد!"}, status=status.HTTP_200_OK)

        else:
            # Physically delete the file by clearing its binary data
            file_or_folder.file_data = None
            file_or_folder.size = 0
            file_or_folder.file_extension = None
            file_or_folder.save()

            # Remove the database entry
            file_or_folder.delete()
            return Response({"message": "فایل با موفقیت حذف شد!"}, status=status.HTTP_200_OK)


class FileManagerAddFileByIdView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [AllowAny]

    @extend_schema(
        operation_id="upload_file",
        summary="Upload a file by ID",
        description="This endpoint allows users to upload a file to a specified parent directory. The file is uploaded as a multipart request.",
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "parentUrl": {
                        "type": "string",
                        "description": "The parent directory URL where the file will be uploaded.",
                        "example": "/uploads/",
                    },
                    "file": {
                        "type": "string",
                        "format": "binary",
                        "description": "The file to be uploaded.",
                    },
                    "id": {
                        "type": "integer",
                        "description": "The unique identifier for the file.",
                        "example": 12345,
                    },
                },
                "required": ["file"],
            }
        },
        responses={
            200: {
                "description": "File uploaded successfully.",
                "content": {
                    "application/json": {
                        "example": {
                            "message": "File uploaded successfully!",
                            "id": 12345
                        }
                    }
                },
            },
        },
        examples=[
            OpenApiExample(
                "Successful Upload",
                description="An example of a successful file upload.",
                value={
                    "parentUrl": "/uploads/",
                    "id": 12345,
                    "file": "(binary content)",
                },
                request_only=True,
            ),
            OpenApiExample(
                "File Already Exists",
                description="Error response when a file with the same name already exists.",
                value={
                    "message": "A file with the same name already exists!"
                },
                response_only=True,
            ),
        ],
    )
    def post(self, request):
        parent_url = request.data.get('parentUrl', None)
        file = request.FILES.get('file')
        file_id = request.data.get('id')

        if not file:
            return Response({"message": "No file was sent!"}, status=status.HTTP_400_BAD_REQUEST)

        # Validate the parent URL
        if not parent_url or parent_url == "":
            parent_url = "/"  # If empty, set to "/"
        elif not parent_url.endswith("/"):
            parent_url = parent_url + "/"  # Ensure '/' is at the end

        # Check for duplicate file names
        if FileManager.objects.filter(id=file_id, name=file.name, parentUrl=parent_url).exists():
            return Response({"message": "A file with the same name already exists!"},
                            status=status.HTTP_400_BAD_REQUEST)

        file_instance = FileManager(id=file_id, name=file.name, parentUrl=parent_url, is_folder=False)
        file_instance.save_file(file)

        return Response({"message": "File uploaded successfully!", "id": file_instance.id}, status=status.HTTP_200_OK)


class FileManagerAddFolderByIdView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        operation_id="add_folder",
        summary="Add a folder by ID",
        description="This endpoint allows you to create a folder under a specific parent URL.",
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "parentUrl": {
                        "type": "string",
                        "description": "The parent directory URL. Defaults to root ('/').",
                        "example": "/documents/",
                    },
                    "name": {
                        "type": "string",
                        "description": "The name of the new folder.",
                        "example": "New Folder",
                    },
                    "id": {
                        "type": "int",
                        "description": "The unique identifier for the folder.",
                        "example": 1,
                    },
                    "size": {
                        "type": "integer",
                        "description": "The size of the folder (optional).",
                        "example": 0,
                    },
                },
                "required": ["name", "id", "size"],

            }
        },
        responses={
            200: {
                "description": "Folder updated successfully.",
                "content": {
                    "application/json": {
                        "example": {
                            "message": "Folder updated successfully!"
                        }
                    }
                },
            },

        },
        examples=[
            OpenApiExample(
                "Create New Folder",
                description="Example payload for creating a new folder.",
                value={
                    "parentUrl": "/documents/",
                    "name": "Project Files",
                    "id": 1,
                    "size": 0,
                },
                request_only=True,  # This example applies to requests
            ),
            OpenApiExample(
                "Folder Already Exists",
                description="Error response when the folder already exists.",
                value={
                    "message": "A folder with this name already exists."
                },
                response_only=True,  # This example applies to responses
            ),
        ],
    )
    def post(self, request):
        parent_url = request.data.get('parentUrl', '/')
        name = request.data.get('name')
        folder_id = request.data.get('id')
        size = request.data.get('size')

        if not name:
            return Response({"message": "Folder name is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure parent_url ends with '/'
        if not parent_url or parent_url == "":
            parent_url = "/"  # If empty, set to "/"
        elif not parent_url.endswith("/"):
            parent_url = parent_url + "/"  # Ensure '/' is at the end

        if FileManager.objects.filter(name=name, parentUrl=parent_url, is_folder=True).exists():
            return Response({"message": "A folder with this name already exists."},
                            status=status.HTTP_400_BAD_REQUEST)
        folder = FileManager.objects.create(id=folder_id, name=name, parentUrl=parent_url, size=size, is_folder=True)
        folder.save()

        return Response({"message": "Folder updated successfully!"}, status=status.HTTP_200_OK)
