import json
from pokemon import Pokemon


class PokemonRepository:
    def __init__(self, filename):
        try:
            f = open(filename, "r")
            data = json.load(f)

            self.pokemon = {}

            for pkmn in data:
                self.pokemon[pkmn["id"]] = Pokemon(pkmn["id"], pkmn["name"], pkmn["type"], pkmn["evolutions"], pkmn["stats"], pkmn["description"])
                #print(self.pokemon[pkmn["id"]].to_string())  # test

            # we have to loop again since usually the "to" evolution of a pokèmon is later on the
            # pokèdex so it isn't known yet in the previous cycle
            for pkmn in self.pokemon.values():
                evo = ""
                if pkmn.evolutions["from"] is not None:
                    evo += "from: " + self.pokemon[pkmn.evolutions["from"]].name
                if pkmn.evolutions["to"] is not None:
                    if len(evo) > 0:
                        evo += ", "
                    # since Eevee can have multiple evolutions, we want to show them all
                    if type(pkmn.evolutions["to"]) is int:
                        evo += "to: " + self.pokemon[pkmn.evolutions["to"]].name
                    elif type(pkmn.evolutions["to"]) is list:
                        evo += "to: "
                        for i in range(len(pkmn.evolutions["to"])):
                            evo += self.pokemon[pkmn.evolutions["to"][i]].name
                            if i+1 != len(pkmn.evolutions["to"]):
                                evo += ", "
                print(pkmn.to_string_evo(evo))
        except OSError:
            print("Cannot open file " + filename)


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