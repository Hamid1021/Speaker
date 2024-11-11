from extensions.utils import get_client_ip
from news.models import Ip_User_to_view


def get_filename(filename, request):
    return filename.upper()


# def seen_page(request):
    # userIp = get_client_ip(request)
    # if request.user.is_anonymous:
        # userName = "ثبت نام نشده"
    # else:
        # userName = request.user.get_full_name()
    # Ip_User_to_view.objects.create(
        # userIp=userIp, userName=userName
    # )
