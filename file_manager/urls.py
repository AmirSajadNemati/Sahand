from django.urls import path

from file_manager.views import FileManagerBaseDataView, FileManagerGetDataView, FileManagerAddFileView, \
    FileManagerEditFileView, FileManagerShowFileView, FileManagerAddOrUpdateFolderView, \
    FileManagerDeleteFileAndFolderView, FileManagerAddFolderByIdView, FileManagerAddFileByIdView

urlpatterns = [
    path('FileManagerBaseData/', FileManagerBaseDataView.as_view(), name='filemanager_base_data'),
    path('FileManagerGetData/', FileManagerGetDataView.as_view(), name='filemanager_get_data'),
    path('FileManagerAddFile/', FileManagerAddFileView.as_view(), name='filemanager_add_file'),
    path('FileManagerEditFile/', FileManagerEditFileView.as_view(), name='filemanager_edit_file'),
    path('FileManagerShowFile/<int:file_id>/', FileManagerShowFileView.as_view(), name='download_file'),
    path('FileManagerAddOrUpdateFolder/', FileManagerAddOrUpdateFolderView.as_view(), name='add_update_folder'),
    path('FileManagerDeleteFileOrFolder/', FileManagerDeleteFileAndFolderView.as_view(), name='delete_folder_file'),
    path('FileManagerAddFolderById/', FileManagerAddFolderByIdView.as_view(), name='add_folder_id'),
    path('FileManagerAddFileById/', FileManagerAddFileByIdView.as_view(), name='add_file_id'),
]
