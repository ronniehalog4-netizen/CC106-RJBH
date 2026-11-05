from django.test import TestCase
from django.urls import reverse

from .models import student


class StudentDirectoryTests(TestCase):
    def setUp(self):
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
