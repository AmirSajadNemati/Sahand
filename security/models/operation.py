from datetime import datetime

from django.db import models, transaction

from security.models import Role


class Operation(models.Model):
    OPERATION_TYPE_CHOICES = [
        (1, 'table'),
        (2, 'static'),
        (3, 'tree-node'),
        (4, 'tree-table')
    ]
    DATA_TYPE_CHOICES = [
        (1, 'page'),
        (2, 'modal')
    ]
    # COUNTED_TYPE_CHOICES = []
    key = models.CharField(max_length=500, null=True, blank=True)
    title = models.CharField(max_length=500, null=True, blank=True)
    icon_lib = models.CharField(max_length=500, null=True, blank=True)
    icon_name = models.CharField(max_length=500, null=True, blank=True)
    url = models.CharField(max_length=1000, null=True, blank=True)
    operation_type = models.PositiveIntegerField(choices=OPERATION_TYPE_CHOICES, null=True, blank=True)
    data_type = models.PositiveIntegerField(choices=DATA_TYPE_CHOICES, null=True, blank=True)
    # counted_type = models.IntegerField()
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    order_num = models.IntegerField()
    create_row_date = models.DateTimeField(auto_now_add=True)
    update_row_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    status = models.IntegerField()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'security_operation'

    def save(self, *args, **kwargs):
        # Check if the operation is new or being updated
        is_new = self._state.adding  # True if creating a new object, False if updating
        # Save the operation (this performs the actual database save)
        super().save(*args, **kwargs)

        # Only update roles if this is an update (not creation)
        if not is_new:
            self.update_related_roles()

    def update_related_roles(self):

        with transaction.atomic():
            # Find all roles that have this operation in their features_selected list
            roles_to_update = Role.objects.filter(
                features_selected__contains=[{'id': self.id}]
            )

            for role in roles_to_update:
                # Extract the list of operations (features_selected)
                features = role.features_selected

                # Iterate through the list to find the matching operation and update all fields
                for operation in features:
                    if operation.get("id") == self.id:  # Find the operation with the matching id
                        # Update all fields from self (assuming self has corresponding attributes)
                        operation["key"] = self.key
                        operation["title"] = self.title
                        operation["icon_lib"] = self.icon_lib
                        operation["icon_name"] = self.icon_name
                        operation["url"] = self.url
                        operation["operation_type"] = self.operation_type
                        operation["data_type"] = self.data_type
                        operation["order_num"] = self.order_num
                        operation["create_row_date"] = (
                            self.create_row_date.isoformat() if isinstance(self.create_row_date,
                                                                           datetime) else self.create_row_date
                        )
                        operation["update_row_date"] = (
                            self.update_row_date.isoformat() if isinstance(self.update_row_date,
                                                                           datetime) else self.update_row_date
                        )
                        operation["is_deleted"] = self.is_deleted
                        operation["status"] = self.status
                        operation["parent"] = self.parent.id if self.parent else None
                        break  # Exit loop after updating the operation

                # Save the updated features_selected back to the role
                role.features_selected = features
                role.save()