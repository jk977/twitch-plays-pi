def permissions(required_role, silent=False):
    """
    Decorator for commands that sets permission level.
    e.g, commands marked with @permissions(Roles.DEFAULT) can
    be used by anyone that isn't banned. PermissionError is raised
    if silent is false and the user doesn't have the required role.
    """
    def outer(func):
        def inner(*args, **kwargs):
            user = kwargs.get('user', None)

            if user:
                if user.role & required_role:
                    func(*args, **kwargs)
                elif not silent:
                    raise PermissionError('You don\'t have permission to do that!')
            else:
                raise ValueError('"user" parameter not found')

        return inner

    return outer
