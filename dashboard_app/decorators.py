from django.http import HttpResponseForbidden

def admin_or_seller_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not (request.user.is_admin() or request.user.is_seller()):
            return HttpResponseForbidden("คุณไม่มีสิทธิ์เข้าถึงหน้านี้!")
        return view_func(request, *args, **kwargs)
    return wrapper
