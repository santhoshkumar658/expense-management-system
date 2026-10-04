from io import BytesIO
from tempfile import TemporaryDirectory

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from .models import Profile


class ProfileViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='profile-user', password='test-password-123'
        )
        self.client.login(username='profile-user', password='test-password-123')

    def make_png(self):
        image_bytes = BytesIO()
        Image.new('RGB', (12, 12), color='green').save(image_bytes, format='PNG')
        return image_bytes.getvalue()

    def test_profile_page_creates_profile_for_existing_user(self):
        response = self.client.get(reverse('profile'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Profile.objects.filter(user=self.user).exists())

    def test_dashboard_renders_for_user_without_profile_record(self):
        response = self.client.get(reverse('dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Profile.objects.filter(user=self.user).exists())

    def test_user_can_update_account_details_and_upload_photo(self):
        with TemporaryDirectory() as media_root, override_settings(MEDIA_ROOT=media_root):
            response = self.client.post(reverse('profile'), {
                'username': 'updated-user',
                'first_name': 'Casey',
                'last_name': 'Rivera',
                'email': 'casey@example.com',
                'phone_number': '555-0102',
                'bio': 'Saving for a first home.',
                'photo': SimpleUploadedFile(
                    'portrait.png', self.make_png(), content_type='image/png'
                ),
            })

            self.assertRedirects(response, reverse('profile'))
            self.user.refresh_from_db()
            profile = Profile.objects.get(user=self.user)
            self.assertEqual(self.user.username, 'updated-user')
            self.assertEqual(self.user.first_name, 'Casey')
            self.assertEqual(self.user.email, 'casey@example.com')
            self.assertEqual(profile.phone_number, '555-0102')
            self.assertEqual(profile.bio, 'Saving for a first home.')
            self.assertTrue(profile.photo.name.endswith('.png'))

    def test_invalid_image_is_rejected(self):
        response = self.client.post(reverse('profile'), {
            'username': self.user.username,
            'first_name': '',
            'last_name': '',
            'email': '',
            'phone_number': '',
            'bio': '',
            'photo': SimpleUploadedFile(
                'not-an-image.png', b'not an image', content_type='image/png'
            ),
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn('photo', response.context['profile_form'].errors)