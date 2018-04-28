from django.test import TestCase

from .models import UserConsult, UserFavorite, UserMessage, UserCourse, CourseComment
from users.tests.test_models import UserModuleModelsDBConnectionTest as UMT
from courses.tests import CourseModuleDBConnectionTest as CMT
from organizations.tests.tests_modules import OrganizationsModuleDBConnectionTest as OMT


class OperationsModuleDBConnectionTest(TestCase):

    def test_user_consult_can_saving_and_retrieving_from_db(self):
        from_amy = UserConsult(
            name="Amy",
            mobile="13888777888",
            course_name="Advance technology in Web Development",
        )
        from_jeff = UserConsult(
            name="Jeff",
            mobile="13888777666",
            course_name="Introduction to Python"
        )
        from_amy.save()
        from_jeff.save()

        consults = UserConsult.objects.all()
        self.assertEqual(consults.count(), 2)
        self.assertEqual(consults[0].name, from_amy.name)
        self.assertEqual(consults[1].name, from_jeff.name)

    def test_user_fav_can_saving_and_retrieving_from_db(self):
        john, jim = UMT.gen_user()
        python_intro, algorithms = CMT.get_courses()
        tsinghua, fudan = OMT.get_orgs()
        mschen, mrzhou = OMT.get_instructors()

        fav1 = UserFavorite(
            user=john,
            fav_type=1,
            fav_id=python_intro.id,
        )
        fav2 = UserFavorite(
            user=jim,
            fav_type=2,
            fav_id=tsinghua.id,
        )
        fav3 = UserFavorite(
            user=jim,
            fav_type=3,
            fav_id=mschen.id,
        )
        fav1.save()
        fav2.save()
        fav3.save()

        favs = UserFavorite.objects.all()
        self.assertEqual(favs.count(), 3)
        self.assertEqual(fav1.fav_id, python_intro.id)
        self.assertEqual(fav2.fav_type, 2)
        self.assertEqual(fav3.user, jim)

    def test_user_message_can_saving_and_retrieving_from_db(self):
        john, jim = UMT.gen_user()
        to_john = UserMessage(
            user=john,
            message="Good luck with your hard work.",
        )
        to_jim = UserMessage(
            user=jim,
            message="Happy birthday to you!",
        )
        to_john.save()
        to_jim.save()

        messages = UserMessage.objects.all()
        self.assertEqual(messages.count(), 2)
        self.assertEqual(messages[0].user, john)
        self.assertEqual(messages[1].user, jim)

    def test_user_course_can_saving_and_retrieving_from_db(self):
        john, jim = UMT.gen_user()
        python_intro, algorithms = CMT.get_courses()
        enr1 = UserCourse(
            user=john,
            course=python_intro,
        )
        enr2 = UserCourse(
            user=john,
            course=algorithms,
        )
        enr3 = UserCourse(
            user=jim,
            course=python_intro,
        )
        enr1.save()
        enr2.save()
        enr3.save()

        enrs = UserCourse.objects.all()
        self.assertEqual(enrs.count(), 3)
        self.assertEqual(enrs[0].user, john)
        self.assertEqual(enrs[1].course, algorithms)
        self.assertEqual(enrs[2].user, jim)

    def test_course_comment_can_saving_and_retrieving_from_db(self):
        john, jim = UMT.gen_user()
        python_intro, algorithms = CMT.get_courses()

        com1 = CourseComment(
            user=john,
            course=python_intro,
            comment="Great course",
        )
        com2 = CourseComment(
            user=john,
            course=algorithms,
            comment="Amazing trip to the algorithms",
        )
        com3 = CourseComment(
            user=jim,
            course=python_intro,
            comment="It's good"
        )
        com4 = CourseComment(
            user=jim,
            course=algorithms,
            comment="Not bad"
        )
        com1.save()
        com2.save()
        com3.save()
        com4.save()

        comments = CourseComment.objects.all()
        self.assertEqual(comments.count(), 4)
        self.assertEqual(comments[0].user, john)
        self.assertEqual(comments[1].user, john)
        self.assertEqual(comments[2].user, jim)
        self.assertEqual(comments[3].user, jim)
