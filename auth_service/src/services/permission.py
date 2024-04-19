from models.user import User
from models.permission import Permission
from models.role import Role
from base_service import BaseService
from utils import decode_jwt, check_date_and_type_token, ACCESS_TOKEN_TYPE
from fastapi import HTTPException, status
from typing import List

class PermissionService(BaseService):
    async def get_user_permissions(self, access_token: str) -> List[Permission]:
        payload = decode_jwt(access_token)
        user_uuid = payload.get("sub")

        if check_date_and_type_token(payload, ACCESS_TOKEN_TYPE):
            # TODO: Retrieve user from the database using user_uuid
            user = User()  # Placeholder for database retrieval

            # Check if user exists
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found"
                )

            # Get user's roles
            roles = user.roles  # Assuming roles is a relationship in the User model

            # Retrieve permissions associated with user's roles
            permissions = []
            for role in roles:
                permissions.extend(role.permissions)

            return permissions

    async def has_permission(self, access_token: str, permission_name: str) -> bool:
        permissions = await self.get_user_permissions(access_token)

        # Check if the user has the required permission
        for permission in permissions:
            if permission.name == permission_name:
                return True

        return False

    async def create_permission(self, name: str) -> Permission:
        # TODO: Implement creation of a new permission in the database
        permission = Permission(name=name)  # Placeholder for database creation
        return permission

    async def assign_permission_to_role(self, role_name: str, permission_name: str) -> bool:
        # TODO: Implement assigning a permission to a role in the database
        # Retrieve role by name
        role = Role(name=role_name)  # Placeholder for database retrieval

        # Retrieve permission by name
        permission = Permission(name=permission_name)  # Placeholder for database retrieval

        # Add permission to role's permissions
        role.permissions.append(permission)  # Placeholder for database operation
        return True

    async def remove_permission_from_role(self, role_name: str, permission_name: str) -> bool:
        # TODO: Implement removing a permission from a role in the database
        # Retrieve role by name
        role = Role(name=role_name)  # Placeholder for database retrieval

        # Retrieve permission by name
        permission = Permission(name=permission_name)  # Placeholder for database retrieval

        # Remove permission from role's permissions
        role.permissions.remove(permission)  # Placeholder for database operation
        return True