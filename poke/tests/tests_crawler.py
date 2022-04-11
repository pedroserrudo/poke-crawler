from django.test import TestCase, Client

from poke.apps.monsters.models import Pokemon
from poke.apps.crawler.api import crawler


class TestCrawler(TestCase):

    test_id = 25

    def setUp(self) -> None:
        pass

    def test_bootstrap(self):
        crawler.update_all_monsters()
        self.assertGreater(Pokemon.objects.count(), 100)

    def test_update_monster(self):
        crawler.update_all_details(self.test_id)
        pika = Pokemon.objects.get(pk=self.test_id)
        self.assertEqual('pikachu', pika.name)
        self.assertEqual(35, pika.order)
        self.assertEqual(60, pika.weight)
        self.assertEqual(4, pika.height)
        self.assertEqual(96, pika.moves.count())
        self.assertEqual(2, pika.held_items.count())

    def test_page(self):
        crawler.update_all_details(self.test_id)
        pika = Pokemon.objects.get(pk=self.test_id)
        c = Client()
        response = c.get(pika.get_absolute_url())
        self.assertEqual(200, response.status_code)

