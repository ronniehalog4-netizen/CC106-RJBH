from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import student


class StudentDirectoryTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.staff_user = user_model.objects.create_user(
            username='staff',
            password='test-password',
            is_staff=True,
        )
        self.client.force_login(self.staff_user)
        self.record = student.objects.create(
            student_id='S001',
            first_name='Ada',
            last_name='Lovelace',
            gender='Female',
            date_of_birth='2000-12-10',
            contact_number='1234567890',
        )

    def test_student_list_searches_id_and_name(self):
        response = self.client.get(reverse('student_list'), {'q': 'love'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'S001')
        self.assertEqual(list(response.context['students']), [self.record])

    def test_student_detail_displays_contact_number(self):
        response = self.client.get(
            reverse('student_detail', args=[self.record.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '1234567890')

    def test_registration_and_form_pages_render(self):
        urls = [
            reverse('student_registration'),
            reverse('student_create'),
            reverse('student_update', args=[self.record.pk]),
        ]

        for url in urls:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_student_create_saves_valid_form(self):
        response = self.client.post(
            reverse('student_create'),
            {
                'student_id': 'S002',
                'first_name': 'Grace',
                'last_name': 'Hopper',
                'gender': 'Female',
                'date_of_birth': '2001-01-02',
                'contact_number': '0987654321',
            },
        )

        self.assertRedirects(response, reverse('student_list'))
        self.assertTrue(student.objects.filter(student_id='S002').exists())

    def test_student_update_changes_record(self):
        response = self.client.post(
            reverse('student_update', args=[self.record.pk]),
            {
                'student_id': 'S001',
                'first_name': 'Augusta',
                'last_name': 'Lovelace',
                'gender': 'Female',
                'date_of_birth': '2000-12-10',
                'contact_number': '1234567890',
            },
            follow=True,
        )

        self.record.refresh_from_db()
        self.assertRedirects(
            response,
            reverse('student_detail', args=[self.record.pk]),
        )
        self.assertEqual(self.record.first_name, 'Augusta')
        self.assertContains(response, 'Student record updated successfully.')

    def test_student_delete_requires_post(self):
        detail_url = reverse('student_delete', args=[self.record.pk])
        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(student.objects.filter(pk=self.record.pk).exists())

        response = self.client.post(detail_url)

        self.assertRedirects(response, reverse('student_list'))
        self.assertFalse(student.objects.filter(pk=self.record.pk).exists())

    def test_existing_registration_route_still_works(self):
        response = self.client.post(
            reverse('register'),
            {
                'student_id': 'S002',
                'first_name': 'Grace',
                'last_name': 'Hopper',
                'gender': 'Female',
                'date_of_birth': '2001-01-02',
                'contact_number': '0987654321',
            },
        )

        self.assertRedirects(response, reverse('registration_success'))
        self.assertTrue(student.objects.filter(student_id='S002').exists())

    def test_home_pages_link_to_student_features(self):
        for url in ('/', reverse('home')):
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, reverse('student_list'))


class StaffAuthenticationTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.staff_user = user_model.objects.create_user(
            username='staff',
            password='test-password',
            is_staff=True,
        )
        self.regular_user = user_model.objects.create_user(
            username='student',
            password='test-password',
        )
        self.record = student.objects.create(
            student_id='AUTH001',
            first_name='Staff',
            last_name='Test',
            gender='Female',
            date_of_birth='2000-01-01',
            contact_number='1234567890',
        )

    def test_login_page_and_invalid_credentials(self):
        response = self.client.post(
            reverse('login'),
            {'username': 'staff', 'password': 'wrong-password'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid username or password')

    def test_staff_login_redirects_to_dashboard(self):
        response = self.client.post(
            reverse('login'),
            {'username': 'staff', 'password': 'test-password'},
        )

        self.assertRedirects(response, reverse('staff_dashboard'))
        dashboard_response = self.client.get(reverse('staff_dashboard'))
        self.assertEqual(dashboard_response.status_code, 200)
        self.assertContains(dashboard_response, 'Register New Student')
        self.assertContains(
            dashboard_response,
            f'href="{reverse("student_create")}"',
        )

    def test_dashboard_calculates_summary_and_searches_report(self):
        self.client.force_login(self.staff_user)
        student.objects.create(
            student_id='AUTH002',
            first_name='Alan',
            last_name='Turing',
            gender='Male',
            date_of_birth='1912-06-23',
            contact_number='5551234567',
        )

        response = self.client.get(reverse('staff_dashboard'))

        self.assertEqual(response.context['total_students'], 2)
        self.assertEqual(response.context['male_students'], 1)
        self.assertEqual(response.context['female_students'], 1)
        self.assertEqual(response.context['male_percent'], 50)
        self.assertEqual(response.context['female_percent'], 50)

        search_response = self.client.get(
            reverse('staff_dashboard'),
            {'q': 'turing'},
        )
        self.assertEqual(search_response.context['total_students'], 2)
        self.assertEqual(
            list(search_response.context['students']),
            [student.objects.get(student_id='AUTH002')],
        )

    def test_anonymous_users_are_redirected_from_staff_pages(self):
        for url in (
            reverse('staff_dashboard'),
            reverse('student_list'),
            reverse('student_create'),
            reverse('student_detail', args=[self.record.pk]),
            reverse('student_update', args=[self.record.pk]),
            reverse('student_delete', args=[self.record.pk]),
        ):
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)
                self.assertEqual(response.url.split('?')[0], reverse('login'))

    def test_non_staff_user_cannot_access_staff_pages(self):
        self.client.force_login(self.regular_user)

        for url in (
            reverse('staff_dashboard'),
            reverse('student_list'),
            reverse('student_create'),
            reverse('student_detail', args=[self.record.pk]),
            reverse('student_update', args=[self.record.pk]),
            reverse('student_delete', args=[self.record.pk]),
        ):
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)
                self.assertEqual(response.url.split('?')[0], reverse('login'))

    def test_public_student_registration_remains_available(self):
        response = self.client.get(reverse('student_registration'))

        self.assertEqual(response.status_code, 200)

    def test_public_student_registration_can_submit(self):
        response = self.client.post(
            reverse('student_registration'),
            {
                'student_id': 'PUBLIC001',
                'first_name': 'Public',
                'last_name': 'Student',
                'gender': 'Female',
                'date_of_birth': '2002-02-02',
                'contact_number': '0987654321',
            },
        )

        self.assertRedirects(response, reverse('registration_success'))
        self.assertTrue(student.objects.filter(student_id='PUBLIC001').exists())

    def test_logout_ends_session_and_redirects_to_login(self):
        self.client.force_login(self.staff_user)

        response = self.client.post(reverse('logout'))

        self.assertRedirects(response, reverse('login'))
        self.assertRedirects(
            self.client.get(reverse('staff_dashboard')),
            f"{reverse('login')}?next={reverse('staff_dashboard')}",
        )

    def test_student_registration_is_available_in_django_admin(self):
        admin_user = get_user_model().objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='test-password',
        )
        self.client.force_login(admin_user)

        response = self.client.get(
            reverse('admin:registration_student_add')
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Add student')
        self.assertContains(response, 'name="student_id"')
