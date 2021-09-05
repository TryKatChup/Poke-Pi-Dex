

class Pokemon:
    def __init__(self, num, name, types, stats, description):
        self.num = num
        self.name = name
        self.types = types
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

    def get_stats(self):
        result = "HP: " + str(self.stats["HP"]) + ", Attack: " + str(self.stats["Attack"]) + ", Defense: " \
                + str(self.stats["Defense"]) + ", Sp. Attack: " + str(self.stats["Sp. Attack"]) + ", Sp. Defense: " \
                + str(self.stats["Sp. Defense"]) + ", Speed: " + str(self.stats["Speed"])

        return result

    def to_string(self):
        return "N°: " + str(self.num) + ", name: " + self.name + ", type(s): [" + self.get_types() + "], stats: {" \
               + self.get_stats() + "}, description: " + self.description
