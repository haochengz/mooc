
from datetime import timedelta

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from operations.models import UserFavorite, UserCourse


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

    @method_decorator(login_required(login_url="/user/login/"))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


def others_choice_of_course(course):
    user_ids = [uc.user.id for uc in UserCourse.objects.filter(course=course)]
    return [c.course for c in UserCourse.objects.filter(user_id__in=user_ids)]


def increasing_enrolled_nums(course, user):
    already_enrolled = UserCourse.objects.filter(course=course, user=user)
    if not len(already_enrolled):
        UserCourse.objects.create(
            course=course,
            user=user,
        )
        course.enrolled_nums += 1
        course.save()
