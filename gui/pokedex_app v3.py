import tkinter as tk
from PIL import ImageTk, Image
from pokemon_repository import PokemonRepository
import playsound as ps
from pokemon import Pokemon
import time

# tkinter utility: https://www.tcl.tk/man/tcl/TkCmd/entry.html#M9

background = "grey"
icons_path = "utilities/icons/"
thumbnails_path = "utilities/thumbnails/"
sprites_path = "utilities/sprites/"
cries_path = "utilities/cries/"
sprite_size = (40, 40)

class App:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        self.window.geometry("480x320")
        image = ImageTk.PhotoImage(file=icons_path + "icon-pokeball.png")
        self.window.tk.call('wm', 'iconphoto', self.window._w, image)
        self.pokemon_repo = PokemonRepository("utilities/first_gen_pokedex.json")

        self.loaded_pokemon = Pokemon(0, "", "", {}, {}, "")
        self.evo_to_i = 0  # index of the multiple evolutions list

        self.frame_left = tk.Frame(width=240, height=320, background="lime")
        self.frame_left.pack(side=tk.LEFT, fill=None, expand=False)
        self.frame_left.pack_propagate(0)
        self.frame_right = tk.Frame(width=240, height=320, bg=background)
        self.frame_right.pack(side=tk.RIGHT, fill=None, expand=False)
        self.frame_right.pack_propagate(0)  # set the frame so that its children cannot control its size

        self.frame_top = tk.Frame(master=self.frame_right, width=240, bg=background)
        self.frame_top.pack(side=tk.TOP)

        # Settings & Info
        # Fake button to space on the left
        self.button_fake = tk.Button(master=self.frame_top, text=" ", bg=background, fg=background, bd=0, highlightthickness=0)
        self.button_fake.pack(side=tk.LEFT, anchor=tk.N)
        # Settings & info frame
        self.frame_settings_info = tk.Frame(master=self.frame_top, bg=background)
        self.frame_settings_info.pack(side=tk.RIGHT, anchor=tk.N)
        # Fake label to space between images and settings/info buttons
        self.label_fake = tk.Label(master=self.frame_settings_info, text="  ", bg=background)
        self.label_fake.pack(side=tk.LEFT)
        self.image_button_settings = ImageTk.PhotoImage(Image.open(icons_path + "icon-settings.png").resize((25, 25), Image.ANTIALIAS))
        self.button_settings = tk.Button(master=self.frame_settings_info, image=self.image_button_settings, bg=background, command=lambda: self.show_settings())
        self.button_settings.pack(side=tk.TOP, anchor=tk.E)
        self.image_button_info = ImageTk.PhotoImage(Image.open(icons_path + "icon-info.png").resize((25, 25), Image.ANTIALIAS))
        self.button_info = tk.Button(master=self.frame_settings_info, image=self.image_button_info, bg=background, command=lambda: self.show_info())
        self.button_info.pack(side=tk.TOP, anchor=tk.E)

        # Top (right)
        self.frame_top_right = tk.Frame(master=self.frame_top, bg=background)
        self.frame_top_right.pack(side=tk.RIGHT, anchor=tk.N)
        # Evolution (to)
        image = Image.open(sprites_path + "0.png").resize(sprite_size, Image.ANTIALIAS)
        self.image_evo_to = ImageTk.PhotoImage(image)
        self.label_evo_to = tk.Label(master=self.frame_top_right, image=self.image_evo_to, width=40, height=40, bg=background)
        self.label_evo_to.pack(side=tk.TOP, anchor=tk.W)
        # Buttons (for multiple "to" evolutions)
        self.image_button_evo_prev = ImageTk.PhotoImage(Image.open(icons_path + "icon-evo-to-prev.png").resize((10, 10), Image.ANTIALIAS))
        self.button_evo_to_prev = tk.Button(master=self.frame_top_right, image=self.image_button_evo_prev, bg=background, command=lambda: self.prev_evo_to())
        self.button_evo_to_prev.config(state=tk.DISABLED)
        self.image_button_evo_next = ImageTk.PhotoImage(Image.open(icons_path + "icon-evo-to-next.png").resize((10, 10), Image.ANTIALIAS))
        self.button_evo_to_next = tk.Button(master=self.frame_top_right, image=self.image_button_evo_next, bg=background, command=lambda: self.next_evo_to())
        self.button_evo_to_next.config(state=tk.DISABLED)
        self.button_evo_to_prev.pack(side=tk.LEFT, anchor=tk.N)
        self.button_evo_to_next.pack(side=tk.LEFT, anchor=tk.N)

        # Image
        image = Image.open(thumbnails_path + "0.png").resize((65, 65), Image.ANTIALIAS)
        self.thumbnail = ImageTk.PhotoImage(image)
        self.label_thumb = tk.Label(master=self.frame_top, image=self.thumbnail, width=65, height=65, bg=background)
        self.label_thumb.pack(side=tk.RIGHT, anchor=tk.N, fill=tk.BOTH)

        # Top-left
        self.frame_top_left = tk.Frame(master=self.frame_top, bg=background)
        self.frame_top_left.pack(side=tk.BOTTOM, anchor=tk.W)
        # Evolution (from)
        image = Image.open(sprites_path + "0.png").resize((40, 40), Image.ANTIALIAS)
        self.image_evo_from = ImageTk.PhotoImage(image)
        self.label_evo_from = tk.Label(master=self.frame_top_left, image=self.image_evo_from, width=40, height=40, bg=background)
        self.label_evo_from.pack(side=tk.TOP, anchor=tk.E)
        # Cry
        self.label_cry = tk.Label(master=self.frame_top_left, text="Cry:", bg=background)
        self.image_button_cry = ImageTk.PhotoImage(Image.open(icons_path + "icon-sound.png").resize((20, 20), Image.ANTIALIAS))
        self.button_cry = tk.Button(master=self.frame_top_left, image=self.image_button_cry, bg=background, activebackground=background, command=lambda: self.play_cry())
        self.label_cry.pack(side=tk.LEFT)
        self.button_cry.pack(side=tk.LEFT)

        # Settings & About (?)

        # Name
        self.frame_name = tk.Frame(master=self.frame_right, bg=background)
        self.frame_name.pack(side=tk.TOP)
        self.label_name = tk.Label(master=self.frame_name, text="Name: ", bg=background)
        self.entry_name_text = tk.StringVar()
        self.entry_name = tk.Entry(master=self.frame_name, width=11, bg=background, bd=0, highlightthickness=0, textvariable=self.entry_name_text)
        self.entry_name.config(readonlybackground=background, state="readonly")
        self.label_name.pack(side=tk.LEFT)
        self.entry_name.pack(side=tk.LEFT)

        # ID and Type(s)
        self.frame_id_types = tk.Frame(master=self.frame_right, bg=background)
        self.frame_id_types.pack()
        self.label_id = tk.Label(master=self.frame_id_types, text="ID: ", bg=background)
        self.entry_id = tk.Entry(master=self.frame_id_types, width=3, bg=background, bd=0, highlightthickness=0)
        self.button_id = tk.Button(master=self.frame_id_types, text="Search", bg=background, activebackground=background, command=lambda: self.load_pokemon(self.entry_id.get()))
        self.label_id.pack(side=tk.LEFT)
        self.entry_id.pack(side=tk.LEFT)
        self.button_id.pack(side=tk.LEFT)

        self.label_types = tk.Label(master=self.frame_id_types, text="Type(s): ", bg=background)
        self.entry_types_text = tk.StringVar()
        self.entry_types = tk.Entry(master=self.frame_id_types, textvariable=self.entry_types_text, width=18, bd=0, highlightthickness=0)
        self.entry_types.config(readonlybackground=background, state="readonly")
        self.label_types.pack(side=tk.LEFT)
        self.entry_types.pack(side=tk.LEFT)

        # description
        self.text_description = tk.Text(master=self.frame_right, height=4, bg=background, bd=0, highlightthickness=0)
        self.text_description.config(font=("Helvetica", 9, "normal"), state="disabled")
        self.text_description.pack()

        # Stats coordinates
        self.x1 = 2
        self.y1 = 4
        self.x2 = 50
        self.y2 = 16
        # HP
        self.frame_hp = tk.Frame(master=self.frame_right, width=240, bg=background)
        self.frame_hp.pack()
        self.label_hp = tk.Label(master=self.frame_hp, width=8, text="HP:", anchor=tk.W, bg=background)
        self.entry_hp_text = tk.StringVar()
        self.entry_hp = tk.Entry(master=self.frame_hp, width=3, textvariable=self.entry_hp_text, bd=0, highlightthickness=0)
        self.entry_hp.config(readonlybackground=background, state="readonly")
        self.canvas_hp = tk.Canvas(master=self.frame_hp, width=160, height=18, bg=background, highlightthickness=0)  # highlightthickness=0 to remove the white borders
        self.rect_hp = self.canvas_hp.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill="red")  # x1, y1, x2, y2
        self.label_hp.pack(side=tk.LEFT)
        self.entry_hp.pack(side=tk.LEFT)
        self.canvas_hp.pack(side=tk.LEFT)
        # Attack
        self.frame_attack = tk.Frame(master=self.frame_right, width=240, bg=background)
        self.frame_attack.pack()
        self.label_attack = tk.Label(master=self.frame_attack, width=8, text="Attack:", anchor=tk.W, bg=background)  # anchor=tk.W to justify the text
        self.entry_attack_text = tk.StringVar()
        self.entry_attack = tk.Entry(master=self.frame_attack, width=3, textvariable=self.entry_attack_text, bd=0, highlightthickness=0)
        self.entry_attack.config(readonlybackground=background, state="readonly")
        self.canvas_attack = tk.Canvas(master=self.frame_attack, width=160, height=18, bg=background, highlightthickness=0)
        self.rect_attack = self.canvas_attack.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill="red")
        self.label_attack.pack(side=tk.LEFT)
        self.entry_attack.pack(side=tk.LEFT)
        self.canvas_attack.pack(side=tk.LEFT)
        # Defense
        self.frame_defense = tk.Frame(master=self.frame_right, width=240, bg=background)
        self.frame_defense.pack()
        self.label_defense = tk.Label(master=self.frame_defense, width=8, text="Defense:", anchor=tk.W, bg=background)
        self.entry_defense_text = tk.StringVar()
        self.entry_defense = tk.Entry(master=self.frame_defense, width=3, textvariable=self.entry_defense_text, bd=0, highlightthickness=0)
        self.entry_defense.config(readonlybackground=background, state="readonly")
        self.canvas_defense = tk.Canvas(master=self.frame_defense, width=160, height=18, bg=background, highlightthickness=0)
        self.rect_defense = self.canvas_defense.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill="red")
        self.label_defense.pack(side=tk.LEFT)
        self.entry_defense.pack(side=tk.LEFT)
        self.canvas_defense.pack(side=tk.LEFT)
        # Sp. Atk
        self.frame_sp_atk = tk.Frame(master=self.frame_right, width=240, bg=background)
        self.frame_sp_atk.pack()
        self.label_sp_atk = tk.Label(master=self.frame_sp_atk, width=8, text="Sp. Atk:", anchor=tk.W, bg=background)
        self.entry_sp_atk_text = tk.StringVar()
        self.entry_sp_atk = tk.Entry(master=self.frame_sp_atk, width=3, textvariable=self.entry_sp_atk_text, bd=0, highlightthickness=0)
        self.entry_sp_atk.config(readonlybackground=background, state="readonly")
        self.canvas_sp_atk = tk.Canvas(master=self.frame_sp_atk, width=160, height=18, bg=background, highlightthickness=0)
        self.rect_sp_atk = self.canvas_sp_atk.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill="red")
        self.label_sp_atk.pack(side=tk.LEFT)
        self.entry_sp_atk.pack(side=tk.LEFT)
        self.canvas_sp_atk.pack(side=tk.LEFT)
        # Sp. Def
        self.frame_sp_def = tk.Frame(master=self.frame_right, width=240, bg=background)
        self.frame_sp_def.pack()
        self.label_sp_def = tk.Label(master=self.frame_sp_def, width=8, text="Sp. Def:", anchor=tk.W, bg=background)
        self.entry_sp_def_text = tk.StringVar()
        self.entry_sp_def = tk.Entry(master=self.frame_sp_def, width=3, textvariable=self.entry_sp_def_text, bd=0, highlightthickness=0)
        self.entry_sp_def.config(readonlybackground=background, state="readonly")
        self.canvas_sp_def = tk.Canvas(master=self.frame_sp_def, width=160, height=18, bg=background, highlightthickness=0)
        self.rect_sp_def = self.canvas_sp_def.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill="red")
        self.label_sp_def.pack(side=tk.LEFT)
        self.entry_sp_def.pack(side=tk.LEFT)
        self.canvas_sp_def.pack(side=tk.LEFT)
        # Speed
        self.frame_speed = tk.Frame(master=self.frame_right, width=240, bg=background)
        self.frame_speed.pack()
        self.label_speed = tk.Label(master=self.frame_speed, width=8, text="Speed:", anchor=tk.W, bg=background)
        self.entry_speed_text = tk.StringVar()
        self.entry_speed = tk.Entry(master=self.frame_speed, width=3, textvariable=self.entry_speed_text, bd=0, highlightthickness=0)
        self.entry_speed.config(readonlybackground=background, state="readonly")
        self.canvas_speed = tk.Canvas(master=self.frame_speed, width=160, height=18, bg=background, highlightthickness=0)
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
            print("Loaded pokemon with id: " + str(pkmn_id))
            self.loaded_pokemon = self.pokemon_repo.pokemon[pkmn_id]

            self.load_image()
            self.load_name()
            # set ID
            self.load_types()
            self.load_description()
            self.load_stats()
            self.load_evolutions()
        else:
            print("The ID must be an integer between 1 and 151 inclusive")

    # update image
    def load_image(self):
        path_image = thumbnails_path + str(self.loaded_pokemon.num) + ".png"
        image = Image.open(path_image).resize((50, 50), Image.ANTIALIAS)
        self.thumbnail = ImageTk.PhotoImage(image)
        self.label_thumb.configure(image=self.thumbnail)

    # update name
    def load_name(self):
        print("Name: " + self.loaded_pokemon.name)
        self.entry_name_text.set(self.loaded_pokemon.name)

    # update type(s)
    def load_types(self):
        types = self.loaded_pokemon.types[0]
        if len(self.loaded_pokemon.types) == 2:
            types += ", " + self.loaded_pokemon.types[1]
        self.entry_types_text.set(types)
        print("Type(s): " + types)

    # update description
    def load_description(self):
        print("Description: " + self.loaded_pokemon.description)
        self.text_description.config(state="normal")
        self.text_description.delete('1.0', tk.END)
        self.text_description.insert('1.0', self.loaded_pokemon.description)
        self.text_description.config(state="disabled")

    # update stats
    def load_stats(self):
        print("Stats:")
        s_hp = self.loaded_pokemon.stats["HP"]
        self.entry_hp_text.set(s_hp)
        self.canvas_hp.coords(self.rect_hp, self.x1, self.y1, s_hp / 2, self.y2)
        self.canvas_hp.itemconfig(self.rect_hp, fill=self.get_color(s_hp))
        s_atk = self.loaded_pokemon.stats["Attack"]
        self.entry_attack_text.set(s_atk)
        self.canvas_attack.coords(self.rect_hp, self.x1, self.y1, s_atk / 2, self.y2)
        self.canvas_attack.itemconfig(self.rect_attack, fill=self.get_color(s_atk))
        s_def = self.loaded_pokemon.stats["Defense"]
        self.entry_defense_text.set(s_def)
        self.canvas_defense.coords(self.rect_hp, self.x1, self.y1, s_def / 2, self.y2)
        self.canvas_defense.itemconfig(self.rect_defense, fill=self.get_color(s_def))
        s_sp_atk = self.loaded_pokemon.stats["Sp. Attack"]
        self.entry_sp_atk_text.set(s_sp_atk)
        self.canvas_sp_atk.coords(self.rect_hp, self.x1, self.y1, s_sp_atk / 2, self.y2)
        self.canvas_sp_atk.itemconfig(self.rect_sp_atk, fill=self.get_color(s_sp_atk))
        s_sp_def = self.loaded_pokemon.stats["Sp. Defense"]
        self.entry_sp_def_text.set(s_sp_def)
        self.canvas_sp_def.coords(self.rect_hp, self.x1, self.y1, s_sp_def / 2, self.y2)
        self.canvas_sp_def.itemconfig(self.rect_sp_def, fill=self.get_color(s_sp_def))
        s_speed = self.loaded_pokemon.stats["Speed"]
        self.entry_speed_text.set(s_speed)
        self.canvas_speed.coords(self.rect_hp, self.x1, self.y1, s_speed / 2, self.y2)
        self.canvas_speed.itemconfig(self.rect_speed, fill=self.get_color(s_speed))
        print("HP:\t\t\t" + str(s_hp) + "\nAttack:\t\t" + str(s_atk) + "\nDefense:\t" + str(s_def) + "\nSp. Atk:\t" +
              str(s_sp_atk) + "\nSp. Def:\t" + str(s_sp_def) + "\nSpeed:\t\t" + str(s_speed))

    # update evolutions
    def load_evolutions(self):
        # from
        evo_from = self.loaded_pokemon.evolutions["from"]
        if evo_from is not None:
            path_image = sprites_path + str(evo_from) + ".png"
        else:
            path_image = sprites_path + "0.png"
        self.image_evo_from = ImageTk.PhotoImage(Image.open(path_image).resize((40, 40), Image.ANTIALIAS))
        self.label_evo_from.configure(image=self.image_evo_from)

        # to
        evo_to = self.loaded_pokemon.evolutions["to"]
        self.button_evo_to_prev.config(state=tk.DISABLED)
        self.button_evo_to_next.config(state=tk.DISABLED)
        if evo_to is not None:
            if type(evo_to) is int:
                path_image = sprites_path + str(evo_to) + ".png"
            elif type(evo_to) is list:  # NB: some pokemon (Eevee) has more than a single evolution
                # add button to scroll evolutions
                self.button_evo_to_next.config(state=tk.NORMAL)
                self.evo_to_i = 0
                path_image = sprites_path + str(evo_to[0]) + ".png"
                self.image_evo_to = ImageTk.PhotoImage(Image.open(path_image).resize((40, 40), Image.ANTIALIAS))
                self.label_evo_to.configure(image=self.image_evo_to)
                return
        else:
            path_image = sprites_path + "0.png"
        self.image_evo_to = ImageTk.PhotoImage(Image.open(path_image).resize((40, 40), Image.ANTIALIAS))
        self.label_evo_to.configure(image=self.image_evo_to)

    # load previous "to" evolution
    def prev_evo_to(self):
        self.evo_to_i -= 1
        evo_to = self.pokemon_repo.pokemon[self.loaded_pokemon.num].evolutions["to"]
        print("Show previous evolution: " + str(evo_to[self.evo_to_i]))
        self.image_evo_to = ImageTk.PhotoImage(Image.open(sprites_path + str(evo_to[self.evo_to_i]) + ".png").resize((40, 40), Image.ANTIALIAS))
        self.label_evo_to.configure(image=self.image_evo_to)
        self.button_evo_to_next.config(state=tk.NORMAL)
        if self.evo_to_i == 0:
            self.button_evo_to_prev.config(state=tk.DISABLED)

    # load next "to" evolution
    def next_evo_to(self):
        self.evo_to_i += 1
        evo_to = self.pokemon_repo.pokemon[self.loaded_pokemon.num].evolutions["to"]
        print("Show next evolution: " + str(evo_to[self.evo_to_i]))
        self.image_evo_to = ImageTk.PhotoImage(Image.open(sprites_path + str(evo_to[self.evo_to_i]) + ".png").resize((40, 40), Image.ANTIALIAS))
        self.label_evo_to.configure(image=self.image_evo_to)
        self.button_evo_to_prev.config(state=tk.NORMAL)
        if self.evo_to_i + 1 == len(evo_to):
            self.button_evo_to_next.config(state=tk.DISABLED)

    # play cry
    def play_cry(self):
        if 1 <= self.loaded_pokemon.num <= 151:
            print("Play cry #" + str(self.loaded_pokemon.num))
            ps.playsound(cries_path + str(self.loaded_pokemon.num) + ".mp3")
        else:
            print("No pokemon has been loaded")

    # Show settings
    def show_settings(self):
        print("Settings")
        self.frame_right.pack_forget()

        # Meglio costruirlo in init e visualizzarlo poi
        # build settings frame
        self.frame_settings = tk.Frame(width=240, height=320, bg=background)
        self.frame_settings.pack(side=tk.RIGHT, fill=None, expand=False)
        self.frame_settings.pack_propagate(0)

        self.image_button_close = ImageTk.PhotoImage(Image.open(icons_path + "icon-close.png").resize((25, 25), Image.ANTIALIAS))
        self.button_close = tk.Button(master=self.frame_settings, image=self.image_button_close, bg=background, bd=0, highlightthickness=0, command=lambda: self.close_settings())
        self.button_close.pack(side=tk.TOP, anchor=tk.E)

        self.text_info = tk.Text(master=self.frame_settings, height=4, bg="blue", bd=0, highlightthickness=0)
        self.text_info.pack(side=tk.TOP, anchor=tk.E)
        self.text_info.insert('1.0', "App megafiga by Kary & Miky")

        # Show info
    def show_info(self):
        print("Info")
        self.frame_right.pack_forget()

        # Meglio costruirlo in init e visualizzarlo poi
        # build settings frame
        self.frame_info = tk.Frame(width=240, height=320, bg=background)
        self.frame_info.pack(side=tk.RIGHT, fill=None, expand=False)
        self.frame_info.pack_propagate(0)

        self.image_button_close = ImageTk.PhotoImage(Image.open(icons_path + "icon-close.png").resize((25, 25), Image.ANTIALIAS))
        self.button_close = tk.Button(master=self.frame_info, image=self.image_button_close, bg=background, command=lambda: self.close_info())
        self.button_close.pack(side=tk.TOP, anchor=tk.E)

    def close_settings(self):
        print("Close settings")
        self.frame_settings.pack_forget()

        self.frame_right.pack(side=tk.RIGHT, fill=None, expand=False)
        self.frame_right.pack_propagate(0)

    def close_info(self):
        print("Close info")
        self.frame_info.pack_forget()

        self.frame_right.pack(side=tk.RIGHT, fill=None, expand=False)
        self.frame_right.pack_propagate(0)

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