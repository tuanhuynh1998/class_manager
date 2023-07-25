from commons.exceptions import NotFoundException
from .models import User

def get_user_by_id(*,
    pk: int
) -> User:
    try:
        user = User.objects.get(pk=pk)
    except:
        raise NotFoundException({"message": "User not found"})
    return user
