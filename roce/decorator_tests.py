"""Some tests I would expect to be in the default Django implementation.

Maybe they are somewhere out there django is so huge.

"""

def is_anonymous(user):
    """Helper for contrib.auth.decorators.user_passes_test."""
    return user.is_anonymous()
