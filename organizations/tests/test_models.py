from django.test import TestCase

from organizations.models import Location, Instructor, Org


class OrganizationsModuleDBConnectionTest(TestCase):

    def test_org_saving_and_retrieving_from_db(self):
        tsinghua, fudan = OrganizationsModuleDBConnectionTest.get_orgs()

        orgs = Org.objects.all()
        self.assertEqual(orgs.count(), 2)
        self.assertEqual(orgs[0].name, tsinghua.name)
        self.assertEqual(orgs[1].name, fudan.name)

    def test_instructor_saving_and_retrieving_from_db(self):
        mschen, mrzhou = OrganizationsModuleDBConnectionTest.get_instructors()

        instructors = Instructor.objects.all()
        self.assertEqual(instructors.count(), 2)
        self.assertEqual(instructors[0].name, mschen.name)
        self.assertEqual(instructors[1].name, mrzhou.name)

    def test_location_saving_and_retrieving_from_db(self):
        bj, sh = OrganizationsModuleDBConnectionTest.get_cities()

        cities = Location.objects.all()
        self.assertEqual(cities.count(), 2)
        self.assertEqual(cities[0].name, bj.name)
        self.assertEqual(cities[1].name, sh.name)

    def test_org_foreigkey_correct(self):
        pass

    def test_instructor_foreigkey_correct(self):
        pass

    @staticmethod
    def get_cities():
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

    @staticmethod
    def get_orgs():
        bj, sh = OrganizationsModuleDBConnectionTest.get_cities()
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

        return tsinghua, fudan

    @staticmethod
    def get_instructors():
        tsinghua, fudan = OrganizationsModuleDBConnectionTest.get_orgs()
        mschen = Instructor(
            org=tsinghua,
            name="Ms. Chen",
            hits=787,
            favorite_nums=62,
            employed="Alphabet Co. Ltd.",
            position="Software Engineer",
            service_len=7,
            characteristics="Strong, fast, flexible",
        )
        mrzhou = Instructor(
            org=fudan,
            name="Mr. Zhou",
            hits=1488,
            favorite_nums=368,
            employed="UC Berkeley",
            position="Head of the software developent program",
            service_len=28,
            characteristics="Old, fun, happy",
        )
        mschen.save()
        mrzhou.save()

        return mschen, mrzhou
