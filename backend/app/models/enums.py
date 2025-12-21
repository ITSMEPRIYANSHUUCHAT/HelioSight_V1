import enum

class UserRole(str, enum.Enum):
    super_admin = "super_admin"
    company_admin = "company_admin"
    end_user = "end_user"
