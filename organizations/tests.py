from django.test import TestCase

from .models import Location, Instructor, Org


class OrganizationsModuleDBConnectionTest(TestCase):

    def test_org_saving_and_retrieving_from_db(self):
        bj, sh = self.get_cities()
        tsinghua = Org(
            name="Tsinghua University",
            desc="A big university",
            hits=1002332,
            favorite_nums=89822,
            image="media/org/2018/04",
            address="Beside the Peiking University",
            located=bj,
        )
        fudan = Org(
            name="Fudan University",
            desc="Another big university",
            hits=98639,
            favorite_nums=34810,
            image="media/org/2018/04",
            address="Somewhere in ShangHai",
            located=sh,
        )
        tsinghua.save()
        fudan.save()

        orgs = Org.objects.all()
        self.assertEqual(orgs.count(), 2)
        self.assertEqual(orgs[0].name, tsinghua.name)
        self.assertEqual(orgs[1].name, fudan.name)

    def test_instructor_saving_and_retrieving_from_db(self):
        pass

    def test_location_saving_and_retrieving_from_db(self):
        pass

    def get_cities(self):
        beijing = Location(
            name="Beijing",
            desc="Just a city",
        )
        shanghai = Location(
            name="Shanghai",
            desc="Just another city",
        )
        beijing.save()
        shanghai.save()
        return beijing, shanghai