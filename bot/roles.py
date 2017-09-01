from enum import Enum

class Roles(Enum):
    """User roles that affect available commands."""
    # TODO convert role usage from array to mask
    OWNER = 1
    MOD = 2
    BANNED = 4

    def get_role_names(array):
        output = []

        if Roles.OWNER in array:
            output.append('owner')

        if Roles.MOD in array:
            output.append('moderator')

        if Roles.BANNED in array:
            output.append('banned')

        return output
