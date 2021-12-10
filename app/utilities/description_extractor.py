import json
from pokemon import Pokemon


class PokemonRepository:
    def __init__(self, filename):
        try:
            f = open(filename, "r", encoding="utf-8")
            data = json.load(f)

            self.pokemon = {}
            self.output = {}
            self.output["pokemon"] = []

            for pkmn in data:
                # name as key
                self.pokemon[pkmn["name"]] = Pokemon(pkmn["id"], pkmn["name"], pkmn["type"], pkmn["evolutions"], pkmn["stats"], pkmn["description"])
                # id as key
                # self.pokemon[pkmn["id"]] = Pokemon(pkmn["id"], pkmn["name"], pkmn["type"], pkmn["evolutions"], pkmn["stats"], pkmn["description"])
                # print(self.pokemon[pkmn["id"]].to_string())  # test
                self.output["pokemon"].append({
                    "nome": pkmn["name"],
                    "descrizione": pkmn["description"]["it"]
                }
                )

            '''for tmp in self.output["pokemon"]:
                print("nome: " + tmp["nome"] + ": " + tmp["descrizione"])'''

            with open("descrizioni.json", 'w', encoding="utf-8") as out_file:
                json.dump(self.output, out_file, indent=2, ensure_ascii=False)
            # TEST: if we want to get info about the "to" evolution, we have to loop again since that pokemon is later
            # on the pokèdex and we hadn't loaded it yet, in the cycle
            # for pkmn in self.pokemon.values():
            #     print(pkmn.to_string_evo(self.get_evolutions(pkmn)))
        except OSError:
            print("Cannot open file " + filename)

# Test
PokemonRepository("utilities/first_gen_pokedex.json")

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