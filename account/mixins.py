class PermissionMixin:
    def has_role(self, role):
        return self.role == role

    @property
    def full_name(self):
        return self.get_full_name()

    @property
    def is_manager(self):
        return self.role == 'manager'

    @property
    def is_supervisor(self):
        return self.role == 'supervisor'

    @property
    def is_guest(self):
        return self.role == 'guest'

    @property
    def is_employee(self):
        return self.role == 'staff'
