from django.core.management.base import BaseCommand, CommandError

from poke.apps.crawler.api import crawler
from poke.apps.monsters.models import Pokemon


class Command(BaseCommand):
    help = 'Update Pokemon'

    ALLOWED_MODES = (
        'update',
        'update-random',
        'update-all',
        'bootstrap',

    )

    def add_arguments(self, parser):
        parser.add_argument('mode', help='Pokemon Update Mode.')
        parser.add_argument('poke_id', help='Pokemon ID to update.', nargs='?', default=0, type=int)

    def handle(self, *args, **options):
        mode = options['mode'].lower()
        if mode not in Command.ALLOWED_MODES:
            raise CommandError(f'Mode must be {self.ALLOWED_MODES[0]} or {self.ALLOWED_MODES[1]}')

        if options['mode'] == 'update' and options['poke_id']:
            poke_id = options['poke_id']
            self.stdout.write(f'run update one {poke_id}')
            crawler.update_all_details(poke_id)

        elif options['mode'] == 'update-random':
            # gives priority to incomplete if they exist
            self.stdout.write('run update random')
            poke = Pokemon.objects.filter(weight=None, height=None).order_by('?').first()\
                or Pokemon.objects.all().order_by('?').first().pk
            crawler.update_all_details(poke.pk)

        elif options['mode'] == 'update-all':
            self.stdout.write('run update all')
            for poke in Pokemon.objects.all().order_by('?'):
                crawler.update_all_details(poke.pk)

        elif options['mode'] == 'bootstrap':
            self.stdout.write('run boostrap')
            crawler.update_all_monsters()

        else:
            self.stderr.write('error on mode parse')
