import json
from pokemon import Pokemon


class PokemonRepository:
    def __init__(self, filename):
        try:
            f = open(filename, "r", encoding="utf-8")
            data = json.load(f)

            self.pokemon = {}

            for pkmn in data:
                self.pokemon[pkmn["id"]] = Pokemon(pkmn["id"], pkmn["name"], pkmn["type"], pkmn["evolutions"], pkmn["stats"], pkmn["description"])
                # print(self.pokemon[pkmn["id"]].to_string())  # test

            # TEST: if we want to get info about the "to" evolution, we have to loop again since that pokemon is later
            # on the pokèdex and we hadn't loaded it yet, in the cycle
            # for pkmn in self.pokemon.values():
            #     print(pkmn.to_string_evo(self.get_evolutions(pkmn)))
        except OSError:
            print("Cannot open file " + filename)
    '''
    # test
    def get_evolutions(self, pkmn):
        result = ""
        if pkmn.evolutions["from"] is not None:
            result += "from: " + self.pokemon[pkmn.evolutions["from"]].name
        if pkmn.evolutions["to"] is not None:
            if len(result) > 0:
                result += ", "
            # since pokèmon like Eevee can have multiple evolutions, we want to show them all
            if type(pkmn.evolutions["to"]) is int:
                result += "to: " + self.pokemon[pkmn.evolutions["to"]].name
            elif type(pkmn.evolutions["to"]) is list:
                result += "to: "
                for i in range(len(pkmn.evolutions["to"])):
                    result += self.pokemon[pkmn.evolutions["to"][i]].name
                    if i + 1 != len(pkmn.evolutions["to"]):
                        result += ", "
        return result
    '''

'''
# Test
pokemon_repo = PokemonRepository("utilities/first_gen_pokedex.json")

while True:
    try:
        # example: get pokèmon by pokèdex id (Squirtle == 7) and print the information
        pkmn_id = int(input("Pokemon ID: "))
        if pkmn_id < 1 or pkmn_id > 151:
            print("ID must be an integer between 1 and 151 inclusive")
            continue
        pkmn = pokemon_repo.pokemon[pkmn_id]
        print(pkmn.to_string_evo(pokemon_repo.get_evolutions(pkmn)))
    except ValueError:
        print("ID must be an integer between 1 and 151 inclusive")
'''

'''
NB: conversion from JSON obj to python obj

obj             -> dict
array           -> list
string          -> str
null            -> None
number(int)     -> int
number(real)    -> float
true            -> True
false           -> False
'''