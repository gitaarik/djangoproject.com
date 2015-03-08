from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from .models import Entry


class EntryTestCase(TestCase):
    def setUp(self):
        self.now = timezone.now()
        self.yesterday = self.now - timedelta(days=1)
        self.tomorrow = self.now + timedelta(days=1)

    def test_manager_active(self):
        """
        Make sure that the Entry manager's `active` method works
        """
        Entry.objects.create(pub_date=self.now, is_active=False)
        Entry.objects.create(pub_date=self.now, is_active=True)

        self.assertEqual(Entry.objects.active().count(), 1)

    def test_manager_published(self):
        """
        Make sure that the Entry manager's `published` method works
        """
        Entry.objects.create(pub_date=self.yesterday, is_active=False)
        Entry.objects.create(pub_date=self.yesterday, is_active=True)
        Entry.objects.create(pub_date=self.tomorrow, is_active=False)
        Entry.objects.create(pub_date=self.tomorrow, is_active=True)

        self.assertEqual(Entry.objects.published().count(), 1)
