from datetime import timedelta

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone

from .models import Entry, Event


class DateTimeMixin(object):
    def setUp(self):
        self.now = timezone.now()
        self.yesterday = self.now - timedelta(days=1)
        self.tomorrow = self.now + timedelta(days=1)


class EntryTestCase(DateTimeMixin, TestCase):
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


class EventTestCase(DateTimeMixin, TestCase):
    def test_manager_past__future(self):
        """
        Make sure that the Entry manager's `active` method works
        """
        Event.objects.create(date=self.yesterday, pub_date=self.now)
        Event.objects.create(date=self.tomorrow, pub_date=self.now)

        self.assertEqual(Event.objects.future().count(), 1)
        self.assertEqual(Event.objects.past().count(), 1)


class ViewsTestCase(DateTimeMixin, TestCase):
    def test_no_past_upcoming_events(self):
        """
        Make sure there are no past event in the "upcoming events" sidebar (#399)
        """
        # We need a published entry on the index page so that it doesn't return a 404
        Entry.objects.create(pub_date=self.yesterday, is_active=True)
        Event.objects.create(date=self.yesterday, pub_date=self.now, is_active=True, headline='Jezdezcon')
        response = self.client.get(reverse('weblog:index'))
        self.assertNotContains(response, 'Jezdezcon', status_code=200)
