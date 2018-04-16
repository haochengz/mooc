from django.test import TestCase
from django.utils import timezone

from .models import Course, Chapter, Section, Resource


class CourseModuleDBConnectionTest(TestCase):

    def test_course_saving_and_retrieving_from_db(self):
        python_intro, algorithms = self.get_courses()

        courses = Course.objects.all()
        self.assertEqual(courses.count(), 2)
        self.assertEqual(courses[0].name, python_intro.name)
        self.assertEqual(courses[1].name, algorithms.name)

    def test_chapter_saving_and_retrieving_from_db(self):
        decorator, dijsktra, binary_search = self.get_chapters()

        chapters = Chapter.objects.all()
        self.assertEqual(chapters.count(), 3)
        self.assertEqual(chapters[0].name, decorator.name)
        self.assertEqual(chapters[1].name, dijsktra.name)
        self.assertEqual(chapters[2].name, binary_search.name)

    def test_section_saving_and_retrieving_from_db(self):
        create_dec, use_dec, why_dec = self.get_sections()
        sections = Section.objects.all()

        self.assertEqual(sections.count(), 3)
        self.assertEqual(sections[0].name, create_dec.name)
        self.assertEqual(sections[1].name, use_dec.name)
        self.assertEqual(sections[2].name, why_dec.name)

    def test_resource_saving_and_retrieving_from_db(self):
        data, test, hello_world = self.get_resources()
        resources = Resource.objects.all()

        self.assertEqual(resources.count(), 3)
        self.assertEqual(data.name, resources[0].name)
        self.assertEqual(test.name, resources[1].name)
        self.assertEqual(hello_world.name, resources[2].name)

    def test_chapters_foreinkey_correct(self):
        # TODO: 测试外链正确
        pass

    def test_sections_foreinkey_correct(self):
        # TODO: 测试外链正确
        pass

    def test_resources_foreinkey_correct(self):
        # TODO: 测试外链正确
        pass

    def get_courses(self):
        python_intro = Course(
            name="Introduction to Python",
            desc="A introduction and tutorial to Python language.",
            detail="A brief introduction didn't dive into the language details.",
            degree="junior",
            duration_mins=100,
            enrolled_nums=1200,
            favorite_nums=8000,
            image="media/courses/2018/04",
            hits=35889,
            add_time=timezone.now(),
        )
        algorithms = Course(
            name="Algorithms",
            desc="The fundamental of computer science",
            detail="Step by step, taught yourself the essential of the algorithms.",
            degree="senior",
            duration_mins=300,
            enrolled_nums=800,
            favorite_nums=9000,
            image="media/courses/2018/04",
            hits=22000,
            add_time=timezone.now(),
        )
        python_intro.save()
        algorithms.save()
        return python_intro, algorithms

    def get_chapters(self):
        python_intro, algorithms = self.get_courses()
        decorator = Chapter(
            name="Decorator",
            add_time=timezone.now(),
            course=python_intro,
        )
        dijsktra = Chapter(
            name="Dijsktra Algorithms",
            add_time=timezone.now(),
            course=algorithms,
        )
        binary_search = Chapter(
            name="Binary Search",
            add_time=timezone.now(),
            course=algorithms,
        )
        decorator.save()
        dijsktra.save()
        binary_search.save()
        return decorator, dijsktra, binary_search

    def get_sections(self):
        decorator, dijsktra, binary_search = self.get_chapters()
        create_decorator = Section(
            chapter=decorator,
            name="How to create a decorator",
            add_time=timezone.now(),
        )
        use_decorator = Section(
            chapter=decorator,
            name="How to use a decorator",
            add_time=timezone.now(),
        )
        why_need_decorator = Section(
            chapter=decorator,
            name="Why do we need decorator when we developing",
            add_time=timezone.now(),
        )
        create_decorator.save()
        use_decorator.save()
        why_need_decorator.save()
        return create_decorator, use_decorator, why_need_decorator

    def get_resources(self):
        python_intro, algorithms = self.get_courses()
        data = Resource(
            name="Data sets for test",
            course=algorithms,
            path="media/courses/resources/2018/04",
            add_time=timezone.now(),
        )
        test = Resource(
            name="Test case of the algorithms",
            course=algorithms,
            path="media/courses/resources/2018/04",
            add_time=timezone.now(),
        )
        hello_world = Resource(
            name="Hello world program of Python",
            course=python_intro,
            path="media/courses/resources/2018/04",
            add_time=timezone.now(),
        )
        data.save()
        test.save()
        hello_world.save()
        return data, test, hello_world
