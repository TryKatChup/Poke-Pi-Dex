import json
from pokemon import Pokemon


class PokemonRepository:
    def __init__(self, filename):
        try:
            f = open(filename, "r")
            data = json.load(f)

            self.pokemon = {}

            for pkmn in data:
                self.pokemon[pkmn["id"]] = Pokemon(pkmn["id"], pkmn["name"], pkmn["type"], pkmn["stats"], pkmn["description"])
                print(self.pokemon[pkmn["id"]].to_string()) # test
        except OSError:
            print("Cannot open file " + filename)


PokemonRepository("utilities/first_gen_pokedex_simple_names.json")
