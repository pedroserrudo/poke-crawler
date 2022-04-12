import requests

from poke.apps.monsters.models import Pokemon, Move, HeldItem


class PokeCrawler:
    base_url = 'https://pokeapi.co/api/v2/'

    def get_all_monsters(self,):
        """
        Get all monsters from API
        Get next page if exists
        return: Monster List
        """
        monsters = []
        next_url = f"{self.base_url}pokemon?limit=100"
        while next_url:
            resp_json = requests.get(next_url).json()
            next_url = resp_json['next']

            # get ids and add monster to list to return
            for obj in resp_json['results']:
                url_parts = obj['url'].split('/')
                monsters.append({
                    'name': obj['name'],
                    'id': url_parts[-2],
                    'url': obj['url']
                })

        return monsters

    def get_monster_details(self, monster_id=None, api_url=None):
        """
        Get Monster Details API call
        return: json
        """
        url = f'{self.base_url}pokemon/{monster_id}' if monster_id else api_url
        resp = requests.get(url)
        return resp.json()

    def get_monster_moves(self, move_id=None, api_url=None):
        """
        Get Monster Moves API call
        return: json
        """
        url = f'{self.base_url}move/{move_id}' if move_id else api_url
        resp = requests.get(url)
        return resp.json()

    def get_monster_items(self, item_id=None, api_url=None):
        """
        Get Held Items API call
        return: json
        """
        url = f'{self.base_url}item/{item_id}' if item_id else api_url
        resp = requests.get(url)
        return resp.json()

    def update_all_details(self, monster_id):
        """
        Update pokemon by ID
        Update Moves & Held Items belonging to pokemon
        """
        print(f'Updating Pokemon #{monster_id}')
        details = self.get_monster_details(monster_id)
        poke, _ = Pokemon.objects.update_or_create(
            pk=monster_id,
            defaults={
                'name': details['name'],
                'avatar': details['sprites']['front_default'],
                'height': details['height'],
                'weight': details['weight'],
                'base_experience': details['base_experience'],
                'order': details['order']
            }
        )

        # Moves
        move_ids = []
        for move in details['moves']:
            move_details = self.get_monster_details(api_url=move['move']['url'])
            #print(f'Update Move {move_details["name"]}#{move_details["id"]} ')
            obj, _ = Move.objects.update_or_create(
                pk=move_details['id'],
                defaults={
                    'name': move_details['name'],
                    'api_url': move['move']['url'],
                    'pp': move_details['pp'],
                    'priority': move_details['priority'],
                    'accuracy': move_details['accuracy'],
                    'power': move_details['power'],
                    'effect': move_details['effect_entries'][0]['effect'] if move_details['effect_entries'] else None,
                    'short_effect': move_details['effect_entries'][0]['short_effect'] if move_details['effect_entries'] else None
                }
            )
            move_ids.append(obj.pk)

        # Check Moves M2M relations and set correct moves if it's not set yet
        if poke.moves.filter(pk__in=move_ids).count() != len(move_ids):
            poke.moves.set(Move.objects.filter(pk__in=move_ids))

        # Update Items
        item_ids = []
        for item in details['held_items']:
            item_details = self.get_monster_items(api_url=item['item']['url'])
            #print(f'Update Item {item_details["name"]}#{item_details["id"]}')
            item_obj, _ = HeldItem.objects.update_or_create(
                pk=item_details['id'],
                defaults={
                    'name': item_details['name'],
                    'cost': item_details['cost'],
                    'fling_power': item_details['fling_power'],
                    'image': item_details['sprites']['default'] if item_details['sprites'] else None
                }
            )
            item_ids.append(item_obj.pk)

        # Check Items M2M relations and set correct items if it's not set yet
        if poke.held_items.filter(pk__in=item_ids).count() != len(item_ids):
            poke.held_items.set(HeldItem.objects.filter(pk__in=item_ids))

    def update_all_monsters(self):
        """
        Bootstrap DB with all Pokemons.
        """
        monsters = self.get_all_monsters()

        for monster in monsters:
            obj, _ = Pokemon.objects.update_or_create(
                pk=monster['id'],
                defaults={'name': monster['name'], 'api_url': monster['url']}
            )


crawler = PokeCrawler()




