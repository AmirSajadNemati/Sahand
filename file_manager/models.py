import os

from django.db import models


class FileManager(models.Model):
    name = models.CharField(max_length=255)  # Name of the file or folder
    # url = models.CharField(max_length=500, blank=True, null=True)
    file_data = models.BinaryField(blank=True, null=True)  # Store raw file data
    # parent = models.ForeignKey('self', related_name='children', on_delete=models.PROTECT, blank=True, null=True)
    parentUrl = models.CharField(max_length=1000, default='/')
    is_folder = models.BooleanField(default=False)  # Determines if it's a folder
    size = models.BigIntegerField(default=0)  # File size in bytes (used for metadata)
    created_at = models.DateTimeField(auto_now_add=True)
    file_extension = models.CharField(max_length=100, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'file_manager'  # Specify the table name here
        verbose_name = 'File Manager'
        verbose_name_plural = 'File Manager'

    def __str__(self):
        return self.name

    def save_file(self, file):
        # Read the file content as binary
        self.file_data = file.read()  # Directly store the raw bytes

        # Save the size in bytes
        self.size = file.size  # Update size in bytes
        self.file_extension = os.path.splitext(file.name)[1]
        self.save()

    def get_file_data(self):
        """
        Returns the file data as binary.
        """
        return self.file_data  # No decoding needed, just return raw bytes
