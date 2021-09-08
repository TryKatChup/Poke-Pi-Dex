import tkinter as tk
from PIL import ImageTk, Image
from pokemon_repository import PokemonRepository
import playsound as ps

class App:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        self.window.geometry("480x320")
        self.pokemon_repo = PokemonRepository("utilities/first_gen_pokedex.json")

        self.frame_left = tk.Frame(width=240, height=320, background="lime")
        self.frame_left.pack(side=tk.LEFT, fill=None, expand=False)
        self.frame_left.pack_propagate(0)
        self.frame_right = tk.Frame(width=240, height=320, background="blue")
        self.frame_right.pack(side=tk.RIGHT, fill=None, expand=False)
        self.frame_right.pack_propagate(0)  # set the frame so that its children cannot control its size

        self.frame_top = tk.Frame(master=self.frame_right, width=240)
        self.frame_top.pack(side=tk.TOP)

        # Top-right
        self.frame_top_right = tk.Frame(master=self.frame_top)
        self.frame_top_right.pack(side=tk.RIGHT, anchor="n")
        # Evolution (to)
        image = Image.open("utilities/sprites/0.png").resize((40, 40), Image.ANTIALIAS)
        self.image_evo_to = ImageTk.PhotoImage(image)
        self.label_evo_to = tk.Label(master=self.frame_top_right, image=self.image_evo_to, width=40, height=40)
        self.label_evo_to.pack(side=tk.TOP, anchor="w")

        # Image
        image = Image.open("utilities/thumbnails/0.png").resize((65, 65), Image.ANTIALIAS)
        self.thumbnail = ImageTk.PhotoImage(image)
        self.label_thumb = tk.Label(master=self.frame_top, image=self.thumbnail, width=65, height=65)
        self.label_thumb.pack(side=tk.RIGHT, anchor="n", fill=tk.BOTH)

        # Top-left
        self.frame_top_left = tk.Frame(master=self.frame_top)
        self.frame_top_left.pack(side=tk.BOTTOM, anchor="w")
        # Evolution (from)
        image = Image.open("utilities/sprites/0.png").resize((40, 40), Image.ANTIALIAS)
        self.image_evo_from = ImageTk.PhotoImage(image)
        self.label_evo_from = tk.Label(master=self.frame_top_left, image=self.image_evo_from, width=40, height=40)
        self.label_evo_from.pack(side=tk.TOP, anchor="e")
        # Cry
        self.label_cry = tk.Label(master=self.frame_top_left, text="Cry:")
        self.image_button_cry = ImageTk.PhotoImage(Image.open("utilities/icons/icon-sound.png").resize((20, 20), Image.ANTIALIAS))
        self.button_cry = tk.Button(master=self.frame_top_left, image=self.image_button_cry, command=lambda: self.play_cry(self.entry_id.get()))
        self.label_cry.pack(side=tk.LEFT)
        self.button_cry.pack(side=tk.LEFT)

        # Settings & About (?)

        # Name
        self.frame_name = tk.Frame(master=self.frame_right)
        self.frame_name.pack(side=tk.TOP)
        self.label_name = tk.Label(master=self.frame_name, text="Name: ")
        self.entry_name_text = tk.StringVar()
        self.entry_name = tk.Entry(master=self.frame_name, width=11, textvariable=self.entry_name_text)
        self.entry_name.config(state="readonly")
        self.label_name.pack(side=tk.LEFT)
        self.entry_name.pack(side=tk.LEFT)

        # ID and Type(s)
        self.frame_id_types = tk.Frame(master=self.frame_right)
        self.frame_id_types.pack()
        self.label_id = tk.Label(master=self.frame_id_types, text="ID: ")
        self.entry_id = tk.Entry(master=self.frame_id_types, width=3)
        self.button_id = tk.Button(master=self.frame_id_types, text="Search", command=lambda: self.load_pokemon(self.entry_id.get()))
        self.label_id.pack(side=tk.LEFT)
        self.entry_id.pack(side=tk.LEFT)
        self.button_id.pack(side=tk.LEFT)

        self.label_types = tk.Label(master=self.frame_id_types, text="Type(s): ")
        self.entry_types_text = tk.StringVar()
        self.entry_types = tk.Entry(master=self.frame_id_types, textvariable=self.entry_types_text, width=18)
        self.entry_types.config(state="readonly")
        self.label_types.pack(side=tk.LEFT)
        self.entry_types.pack(side=tk.LEFT)

        '''# evolutions test (sostituire con immagini)
        self.frame_evolutions = tk.Frame()
        self.frame_evolutions.pack()
        self.label_evolutions = tk.Label(master=self.frame_evolutions, text="Evolutions: ")
        self.label_evolutions_from = tk.Label(master=self.frame_evolutions, text="From: ")
        self.entry_evolutions_from_text = tk.StringVar()
        self.entry_evolutions_from = tk.Entry(master=self.frame_evolutions, textvariable=self.entry_evolutions_from_text)
        self.label_evolutions_to = tk.Label(master=self.frame_evolutions, text=" To: ")
        self.entry_evolutions_to_text = tk.StringVar()
        self.entry_evolutions_to = tk.Entry(master=self.frame_evolutions, textvariable=self.entry_evolutions_to_text)
        self.label_evolutions.pack()
        self.label_evolutions_from.pack(side=tk.LEFT)
        self.entry_evolutions_from.pack(side=tk.LEFT)
        self.entry_evolutions_to.pack(side=tk.RIGHT)
        self.label_evolutions_to.pack(side=tk.RIGHT)'''

        # description
        #self.label_description = tk.Label(master=self.frame_right, text="Description: ")
        self.text_description = tk.Text(master=self.frame_right, height=4)
        self.text_description.config(state="disabled")
        #self.label_description.pack()
        self.text_description.pack()

        # Stats
        self.x1 = 2
        self.y1 = 4
        self.x2 = 50
        self.y2 = 16
        # HP
        self.frame_hp = tk.Frame(master=self.frame_right, width=240)
        self.frame_hp.pack()
        self.label_hp = tk.Label(master=self.frame_hp, width=7, text="HP:", anchor=tk.W)
        self.entry_hp_text = tk.StringVar()
        self.entry_hp = tk.Entry(master=self.frame_hp, width=3, textvariable=self.entry_hp_text)
        self.entry_hp.config(state="readonly")
        self.canvas_hp = tk.Canvas(master=self.frame_hp, width=160, height=18)  # bg="yellow" test
        self.rect_hp = self.canvas_hp.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill="red")  # x1, y1, x2, y2
        self.label_hp.pack(side=tk.LEFT)
        self.entry_hp.pack(side=tk.LEFT)
        self.canvas_hp.pack(side=tk.LEFT)
        # Attack
        self.frame_attack = tk.Frame(master=self.frame_right, width=240)
        self.frame_attack.pack()
        self.label_attack = tk.Label(master=self.frame_attack, width=7, text="Attack:", anchor=tk.W)  # anchor=tk.W to justify the text
        self.entry_attack_text = tk.StringVar()
        self.entry_attack = tk.Entry(master=self.frame_attack, width=3, textvariable=self.entry_attack_text)
        self.entry_attack.config(state="readonly")
        self.canvas_attack = tk.Canvas(master=self.frame_attack, width=160, height=18)
        self.rect_attack = self.canvas_attack.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill="red")
        self.label_attack.pack(side=tk.LEFT)
        self.entry_attack.pack(side=tk.LEFT)
        self.canvas_attack.pack(side=tk.LEFT)
        # Defense
        self.frame_defense = tk.Frame(master=self.frame_right, width=240)
        self.frame_defense.pack()
        self.label_defense = tk.Label(master=self.frame_defense, width=7, text="Defense:", anchor=tk.W)
        self.entry_defense_text = tk.StringVar()
        self.entry_defense = tk.Entry(master=self.frame_defense, width=3, textvariable=self.entry_defense_text)
        self.entry_defense.config(state="readonly")
        self.canvas_defense = tk.Canvas(master=self.frame_defense, width=160, height=18)
        self.rect_defense = self.canvas_defense.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill="red")
        self.label_defense.pack(side=tk.LEFT)
        self.entry_defense.pack(side=tk.LEFT)
        self.canvas_defense.pack(side=tk.LEFT)
        # Sp. Atk
        self.frame_sp_atk = tk.Frame(master=self.frame_right, width=240)
        self.frame_sp_atk.pack()
        self.label_sp_atk = tk.Label(master=self.frame_sp_atk, width=7, text="Sp. Atk:", anchor=tk.W)
        self.entry_sp_atk_text = tk.StringVar()
        self.entry_sp_atk = tk.Entry(master=self.frame_sp_atk, width=3, textvariable=self.entry_sp_atk_text)
        self.entry_sp_atk.config(state="readonly")
        self.canvas_sp_atk = tk.Canvas(master=self.frame_sp_atk, width=160, height=18)
        self.rect_sp_atk = self.canvas_sp_atk.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill="red")
        self.label_sp_atk.pack(side=tk.LEFT)
        self.entry_sp_atk.pack(side=tk.LEFT)
        self.canvas_sp_atk.pack(side=tk.LEFT)
        # Sp. Def
        self.frame_sp_def = tk.Frame(master=self.frame_right, width=240)
        self.frame_sp_def.pack()
        self.label_sp_def = tk.Label(master=self.frame_sp_def, width=7, text="Sp. Def:", anchor=tk.W)
        self.entry_sp_def_text = tk.StringVar()
        self.entry_sp_def = tk.Entry(master=self.frame_sp_def, width=3, textvariable=self.entry_sp_def_text)
        self.entry_sp_def.config(state="readonly")
        self.canvas_sp_def = tk.Canvas(master=self.frame_sp_def, width=160, height=18)
        self.rect_sp_def = self.canvas_sp_def.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill="red")
        self.label_sp_def.pack(side=tk.LEFT)
        self.entry_sp_def.pack(side=tk.LEFT)
        self.canvas_sp_def.pack(side=tk.LEFT)
        # Speed
        self.frame_speed = tk.Frame(master=self.frame_right, width=240)
        self.frame_speed.pack()
        self.label_speed = tk.Label(master=self.frame_speed, width=7, text="Speed:", anchor=tk.W)
        self.entry_speed_text = tk.StringVar()
        self.entry_speed = tk.Entry(master=self.frame_speed, width=3, textvariable=self.entry_speed_text)
        self.entry_speed.config(state="readonly")
        self.canvas_speed = tk.Canvas(master=self.frame_speed, width=160, height=18)
        self.rect_speed = self.canvas_speed.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill="red")
        self.label_speed.pack(side=tk.LEFT)
        self.entry_speed.pack(side=tk.LEFT)
        self.canvas_speed.pack(side=tk.LEFT)

    def run(self):
        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 1
        self.update()
        self.window.mainloop()

    def update(self):
        self.window.after(self.delay, self.update)

    def load_pokemon(self, pkmn_id):
        try:
            pkmn_id = int(pkmn_id)
        except ValueError:
            print("The ID must be an integer between 1 and 151 inclusive")
            return
        if 1 <= pkmn_id <= 151:
            print("Loading pokemon with id: " + str(pkmn_id))
            pokemon = self.pokemon_repo.pokemon[pkmn_id]

            self.load_image(pokemon)
            self.load_name(pokemon)
            # set ID
            self.load_types(pokemon)
            self.load_description(pokemon)
            self.load_stats(pokemon)
            self.load_evolutions(pokemon)

    # update image
    def load_image(self, pkmn):
        path_image = "utilities/thumbnails/" + str(pkmn.num) + ".png"
        image = Image.open(path_image).resize((50, 50), Image.ANTIALIAS)
        self.thumbnail = ImageTk.PhotoImage(image)
        self.label_thumb.configure(image=self.thumbnail)

    # update name
    def load_name(self, pkmn):
        self.entry_name_text.set(pkmn.name)  # self.entry_name.delete(0, tk.END), self.entry_name.insert(0, pokemon.name) # alternative

    # update type(s)
    def load_types(self, pkmn):
        types = pkmn.types[0]
        if len(pkmn.types) == 2:
            types += ", " + pkmn.types[1]
        self.entry_types_text.set(types)

    # update description
    def load_description(self, pkmn):
        self.text_description.config(state="normal")
        self.text_description.delete('1.0', tk.END)
        self.text_description.insert('1.0', pkmn.description)
        self.text_description.config(state="disabled")

    # update stats
    def load_stats(self, pkmn):
        print("load stats")
        self.entry_hp_text.set(pkmn.stats["HP"])
        self.canvas_hp.coords(self.rect_hp, self.x1, self.y1, int(pkmn.stats["HP"]) / 2, self.y2)
        self.canvas_hp.itemconfig(self.rect_hp, fill=self.get_color(int(pkmn.stats["HP"])))
        self.entry_attack_text.set(pkmn.stats["Attack"])
        self.canvas_attack.coords(self.rect_hp, self.x1, self.y1, int(pkmn.stats["Attack"]) / 2, self.y2)
        self.canvas_attack.itemconfig(self.rect_attack, fill=self.get_color(int(pkmn.stats["Attack"])))
        self.entry_defense_text.set(pkmn.stats["Defense"])
        self.canvas_defense.coords(self.rect_hp, self.x1, self.y1, int(pkmn.stats["Defense"]) / 2, self.y2)
        self.canvas_defense.itemconfig(self.rect_defense, fill=self.get_color(int(pkmn.stats["Defense"])))
        self.entry_sp_atk_text.set(pkmn.stats["Sp. Attack"])
        self.canvas_sp_atk.coords(self.rect_hp, self.x1, self.y1, int(pkmn.stats["Sp. Attack"]) / 2, self.y2)
        self.canvas_sp_atk.itemconfig(self.rect_sp_atk, fill=self.get_color(int(pkmn.stats["Sp. Attack"])))
        self.entry_sp_def_text.set(pkmn.stats["Sp. Defense"])
        self.canvas_sp_def.coords(self.rect_hp, self.x1, self.y1, int(pkmn.stats["Sp. Defense"]) / 2, self.y2)
        self.canvas_sp_def.itemconfig(self.rect_sp_def, fill=self.get_color(int(pkmn.stats["Sp. Defense"])))
        self.entry_speed_text.set(pkmn.stats["Speed"])
        self.canvas_speed.coords(self.rect_hp, self.x1, self.y1, int(pkmn.stats["Speed"]) / 2, self.y2)
        self.canvas_speed.itemconfig(self.rect_speed, fill=self.get_color(int(pkmn.stats["Speed"])))

    # update evolutions
    def load_evolutions(self, pkmn):
        # from
        if pkmn.evolutions["from"] is not None:
            path_image = "utilities/sprites/" + str(pkmn.evolutions["from"]) + ".png"
        else:
            path_image = "utilities/sprites/0.png"
        self.image_evo_from = ImageTk.PhotoImage(Image.open(path_image).resize((40, 40), Image.ANTIALIAS))
        self.label_evo_from.configure(image=self.image_evo_from)
        # to (NB: Eevee has 3 evolutions)
        if pkmn.evolutions["to"] is not None:
            if type(pkmn.evolutions["to"]) is int:
                path_image = "utilities/sprites/" + str(pkmn.evolutions["to"]) + ".png"
            elif type(pkmn.evolutions["to"]) is list:
                '''for i in range(len(pkmn.evolutions["to"])):
                    '''
                # temporary solution (we need to add 2 more evolution sprites)
                path_image = "utilities/sprites/" + str(pkmn.evolutions["to"][0]) + ".png"
                self.image_evo_to = ImageTk.PhotoImage(Image.open(path_image).resize((40, 40), Image.ANTIALIAS))
                self.label_evo_to.configure(image=self.image_evo_to)
                return
        else:
            path_image = "utilities/sprites/0.png"
        self.image_evo_to = ImageTk.PhotoImage(Image.open(path_image).resize((40, 40), Image.ANTIALIAS))
        self.label_evo_to.configure(image=self.image_evo_to)
        # if pkmn.evolutions["to"] is not None:

    '''def load_evolutions(self, pkmn):
        self.entry_evolutions_from_text.set("")
        self.entry_evolutions_to_text.set("")
        evo_from = pkmn.evolutions["from"]
        if evo_from is not None:
            self.entry_evolutions_from_text.set(self.pokemon_repo.pokemon[evo_from].name)
        evo_to = pkmn.evolutions["to"]
        if evo_to is not None:
            self.entry_evolutions_to_text.set(self.pokemon_repo.pokemon[evo_to].name)'''

    # play cry
    def play_cry(self, pkmn_id):
        try:
            pkmn_id = int(pkmn_id)
        except ValueError:
            print("The ID must be an integer between 1 and 151 inclusive")
            return
        if 1 <= pkmn_id <= 151:
            print("play cry")
            ps.playsound("utilities/cries/" + str(pkmn_id) + ".mp3")

    # get RGB color from stat
    def get_color(self, stat):
        if 0 <= stat < 25:
            return "#ff0000"
        if 25 <= stat < 50:
            return "#ff5500"
        if 50 <= stat < 75:
            return "#ffaa00"
        if 75 <= stat < 100:
            return "#ffff00"
        if 100 <= stat < 125:
            return "#7fff00"
        if 125 <= stat < 150:
            return "#00ff00"
        if 150 <= stat < 200:
            return "#00ff80"
        return "#00ffff"


app = App(tk.Tk(), "pokedex")
app.run()