

class Pokemon:
    def __init__(self, num, name, types, evolutions, stats, description):
        self.num = num
        self.name = name
        self.types = types
        self.evolutions = evolutions
        self.stats = stats
        self.description = description

    # utility methods
    def get_types(self):
        result = ""
        for n in range(len(self.types)):
            result += self.types[n]
            if n + 1 != len(self.types):
                result += ", "

        return result

    def get_evolutions(self):
        result = ""
        if self.evolutions["from"] is not None:
            result += "evolves from: " + self.evolutions["from"]
        if self.evolutions["to"] is not None:
            if len(result) > 0:
                result += ", "
            result += "evolves to: " + self.evolutions["to"]
        return result

    def get_stats(self):
        result = "HP: " + str(self.stats["HP"]) + ", Attack: " + str(self.stats["Attack"]) + ", Defense: " \
                + str(self.stats["Defense"]) + ", Sp. Attack: " + str(self.stats["Sp. Attack"]) + ", Sp. Defense: " \
                + str(self.stats["Sp. Defense"]) + ", Speed: " + str(self.stats["Speed"])

        return result

    def to_string(self):
        return "N°: " + str(self.num) + ", name: " + self.name + ", type(s): [" + self.get_types() + "], evolutions: "\
               + self.get_evolutions() + ", stats: {" + self.get_stats() + "}, description: " + self.description

    def to_string_evo(self, evolutions):
        return "N°: " + str(self.num) + ", name: " + self.name + ", type(s): [" + self.get_types() + "], evolutions: {"\
               + evolutions + "}, stats: {" + self.get_stats() + "}, description: " + self.description