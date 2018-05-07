
from datetime import timedelta

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from operations.models import UserFavorite


def minutes_ago(now, minutes):
    ago = now - timedelta(minutes=minutes)
    return ago


def add_favorite(fav_type, fav_id, user):
    fav = UserFavorite.objects.filter(fav_type=fav_type, fav_id=fav_id, user=user)
    if fav:
        fav.delete()
        return HttpResponse("{'status': 'success', 'msg': 'Undo Favorite'}")
    else:
        UserFavorite.objects.create(
            fav_id=fav_id,
            fav_type=fav_type,
            user=user,
        )
        return HttpResponse("{'status': 'success', 'msg': 'Add Favorite'}")


class LoginRequiredMixin:

    @method_decorator(login_required(login_url="/login/"))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
