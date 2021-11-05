import tkinter as tk
from PIL import ImageTk, Image
from app.pokemon_repository import PokemonRepository
from app.pokemon import Pokemon
import cv2
import video_capture as vc
import time
# Sound
import pygame
# Classifier

# Screenshot
import pyautogui as pg

# tkinter utility: https://www.tcl.tk/man/tcl/TkCmd/entry.html#M9

app_name = "Poké-Pi-Dex"
version = "1.0 beta"
background = "grey"
background_dark = "#6a6a6a"
icons_path = "utilities/icons/"
thumbnails_path = "utilities/thumbnails/"
sprites_path = "utilities/sprites/"
cries_path = "utilities/cries (ogg)/"
sprite_size = (40, 40)

class App:
    def __init__(self, window, window_title, video_source=0):  # se non specificato viene preso il primo input video
        self.window = window
        self.window.title(window_title)
        self.window.geometry("480x320")
        self.fullscreen = tk.IntVar()
        self.fullscreen.set(1)
        self.window.attributes("-fullscreen", self.fullscreen.get())
        image = ImageTk.PhotoImage(file=icons_path + "icon-pokeball.png")
        self.window.tk.call("wm", "iconphoto", self.window._w, image)
        self.video_source = video_source
        
        # Sound init
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.init()
        pygame.mixer.init()
        # Channel init
        self.volume = 0.5
        self.channel = pygame.mixer.find_channel(True)
        self.channel.set_volume(self.volume)

        self.pokemon_repo = PokemonRepository("utilities/first_gen_pokedex.json")
        self.video = vc.VideoCapture(self.video_source)

        self.loaded_pokemon = Pokemon(0, "", "", {}, {}, "")
        self.evo_to_i = 0  # index of the multiple evolutions list

        # Menu
        self.frame_menu = tk.Frame(width=480, height=320, background="yellow")
        self.frame_menu.pack_propagate(0)
        self.canvas_background = tk.Canvas(master=self.frame_menu, width=480, height=320)
        self.canvas_background.pack()
        image = Image.open("menu-background.png").resize((480, 320), Image.ANTIALIAS)
        self.image_background = ImageTk.PhotoImage(image)
        self.canvas_background.create_image(0, 0, anchor=tk.NW, image=self.image_background)
        '''self.label_app_name = tk.Label(master=self.frame_menu, text=app_name, bg=background)
        self.label_app_name.config(font=("Helvetica", 24, "bold italic"))
        self.canvas_background.create_window(240, 0+80, anchor=tk.N, window=self.label_app_name)'''
        # self.label_app_name.pack(side=tk.TOP, pady=(80, 0))
        self.label_app_version = tk.Label(master=self.frame_menu, text="v" + version, width=10, bg="black", fg="grey")
        self.label_app_version.config(font=("Helvetica", 10, "italic bold"))
        self.canvas_background.create_window(197, 91, anchor=tk.N, window=self.label_app_version)
        # self.canvas_background.create_window(240, 80+52, anchor=tk.N, window=self.label_app_version)
        # self.label_app_version.pack(side=tk.TOP, pady=(0, 30))
        self.button_start = tk.Button(master=self.frame_menu, text="Start", width=15, bg=background, activebackground=background, command=lambda: self.show_app())
        self.canvas_background.create_window(197, 132+50, anchor=tk.N, window=self.button_start)
        # self.button_start.pack(side=tk.TOP, pady=(0, 10))
        self.button_quit = tk.Button(master=self.frame_menu, text="Quit", width=15, bg=background, activebackground=background, command=lambda: self.quit())
        self.canvas_background.create_window(197, 182+50, anchor=tk.N, window=self.button_quit)
        # self.button_quit.pack(side=tk.TOP)

        # Pokédex App
        self.frame_left = tk.Frame(width=240, height=320, background="lime")
        self.frame_left.pack_propagate(0)  # set the frame so that its children cannot control its size
        self.frame_right = tk.Frame(width=240, height=320, bg=background)
        self.frame_right.pack_propagate(0)

        # Left (video stream)
        self.canvas_video = tk.Canvas(master=self.frame_left, width=self.video.width/2, height=(self.video.height/2)-20, bg=background, highlightthickness=0)
        self.canvas_video.pack(side=tk.TOP)
        self.frame_video_controls = tk.Frame(master=self.frame_left, bg=background)
        self.frame_video_controls.pack(side=tk.TOP)

        self.button_search = tk.Button(master=self.frame_video_controls, text="Search", bg=background, activebackground=background, command=lambda: self.load_pokemon(self.entry_name_text.get()))
        self.button_search.pack(side=tk.LEFT, anchor=tk.CENTER, padx=(0, 10))
        self.button_screenshot = tk.Button(master=self.frame_video_controls, text="Screenshot", bg=background, activebackground=background, command=lambda: self.save_screenshot())
        self.button_screenshot.pack(side=tk.LEFT, anchor=tk.CENTER)

        # Right (pokedex info)
        self.frame_top = tk.Frame(master=self.frame_right, width=240, bg=background)
        self.frame_top.pack(side=tk.TOP)

        # Settings & Info
        # Fake button to space on the left (easter egg -> show blaziken <3)
        self.button_egg = tk.Button(master=self.frame_top, text=" ", bg=background, fg=background, bd=0, highlightthickness=0, command=lambda: self.load_pokemon('Blaziken'))
        self.button_egg.pack(side=tk.LEFT, anchor=tk.N)
        # Settings & info frame
        self.frame_settings_info = tk.Frame(master=self.frame_top, bg=background)
        self.frame_settings_info.pack(side=tk.RIGHT, anchor=tk.N, padx=(16, 0))
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
        self.button_evo_to_prev = tk.Button(master=self.frame_top_right, image=self.image_button_evo_prev, bg=background, command=lambda: self.show_prev_evo_to())
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

        # Name
        self.frame_name = tk.Frame(master=self.frame_right, bg=background)
        self.frame_name.pack(side=tk.TOP)
        self.label_name = tk.Label(master=self.frame_name, text="Name: ", bg=background)
        self.entry_name_text = tk.StringVar()
        self.entry_name = tk.Entry(master=self.frame_name, width=11, textvariable=self.entry_name_text, bg=background_dark, bd=0, highlightthickness=0)
        self.entry_name.config(readonlybackground=background_dark)
        self.label_name.pack(side=tk.LEFT)
        self.entry_name.pack(side=tk.LEFT)

        # ID and Type(s)
        self.frame_id_types = tk.Frame(master=self.frame_right, bg=background)
        self.frame_id_types.pack()
        self.label_id = tk.Label(master=self.frame_id_types, text="ID: ", bg=background)
        self.entry_id_text = tk.StringVar()
        self.entry_id = tk.Entry(master=self.frame_id_types, width=3, textvariable=self.entry_id_text, bg=background_dark, bd=0, highlightthickness=0)
        self.entry_id.config(readonlybackground=background_dark, state="readonly")
        self.label_id.pack(side=tk.LEFT)
        self.entry_id.pack(side=tk.LEFT)
        # Test: search button

        self.label_types = tk.Label(master=self.frame_id_types, text="Type(s): ", bg=background)
        self.entry_types_text = tk.StringVar()
        self.entry_types = tk.Entry(master=self.frame_id_types, textvariable=self.entry_types_text, width=18, bd=0, highlightthickness=0)
        self.entry_types.config(readonlybackground=background_dark, state="readonly")
        self.label_types.pack(side=tk.LEFT)
        self.entry_types.pack(side=tk.LEFT)

        # description
        self.text_description = tk.Text(master=self.frame_right, height=4, bg=background_dark, bd=0, highlightthickness=0)
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
        self.entry_hp.config(readonlybackground=background_dark, state="readonly")
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
        self.entry_attack.config(readonlybackground=background_dark, state="readonly")
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
        self.entry_defense.config(readonlybackground=background_dark, state="readonly")
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
        self.entry_sp_atk.config(readonlybackground=background_dark, state="readonly")
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
        self.entry_sp_def.config(readonlybackground=background_dark, state="readonly")
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
        self.entry_speed.config(readonlybackground=background_dark, state="readonly")
        self.canvas_speed = tk.Canvas(master=self.frame_speed, width=160, height=18, bg=background, highlightthickness=0)
        self.rect_speed = self.canvas_speed.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill="red")
        self.label_speed.pack(side=tk.LEFT)
        self.entry_speed.pack(side=tk.LEFT)
        self.canvas_speed.pack(side=tk.LEFT)

        # Settings
        self.frame_settings = tk.Frame(width=240, height=320, bg=background)
        self.frame_settings.pack_propagate(0)
        self.image_button_close_settings = ImageTk.PhotoImage(Image.open(icons_path + "icon-close.png").resize((25, 25), Image.ANTIALIAS))
        self.button_close = tk.Button(master=self.frame_settings, image=self.image_button_close_settings, bg=background, command=lambda: self.close_settings())
        self.button_close.pack(side=tk.TOP, anchor=tk.E)
        # Toggle Fullscreen
        self.frame_fullscreen = tk.Frame(master=self.frame_settings, bg=background)
        self.frame_fullscreen.pack(side=tk.TOP, pady=(50, 0))
        self.check_fullscreen = tk.Checkbutton(master=self.frame_fullscreen, variable=self.fullscreen, onvalue=1, offvalue=0, bg=background, bd=0, highlightthickness=0, fg="black")
        self.check_fullscreen.select() if self.fullscreen.get() == 1 else self.check_fullscreen.deselect()
        self.check_fullscreen.pack(side=tk.LEFT)
        self.label_fullscreen = tk.Label(master=self.frame_fullscreen, text="Fullscreen", bg=background)
        self.label_fullscreen.pack(side=tk.LEFT)
        # Volume
        self.frame_volume = tk.Frame(master=self.frame_settings, bg=background)
        self.frame_volume.pack(side=tk.TOP)
        self.label_volume = tk.Label(master=self.frame_volume, text="Volume: ", bg=background)
        self.label_volume.pack(side=tk.LEFT)
        self.scale_volume = tk.Scale(master=self.frame_volume, from_=0, to=100, tickinterval=100, orient=tk.HORIZONTAL, bg=background, bd=0, highlightthickness=0)
        self.scale_volume.set(50)
        self.scale_volume.pack(side=tk.LEFT)
        # Save/Cancel buttons
        self.button_save_settings = tk.Button(master=self.frame_settings, text="Save", bg=background, width=6, command=lambda: self.save_settings())
        self.button_save_settings.pack(side=tk.LEFT, anchor=tk.N, padx=(50, 5))
        self.button_cancel_settings = tk.Button(master=self.frame_settings, text="Cancel", bg=background, command=lambda: self.close_settings())
        self.button_cancel_settings.pack(side=tk.LEFT, anchor=tk.N, padx=5)

        # Info
        self.frame_info = tk.Frame(width=240, height=320, bg=background)
        self.frame_info.pack_propagate(0)
        self.image_button_close_info = ImageTk.PhotoImage(Image.open(icons_path + "icon-close.png").resize((25, 25), Image.ANTIALIAS))
        self.button_close = tk.Button(master=self.frame_info, image=self.image_button_close_info, bg=background, command=lambda: self.close_info())
        self.button_close.pack(side=tk.TOP, anchor=tk.E)
        self.text_info = tk.Text(master=self.frame_info, height=4, bg=background_dark, bd=0, highlightthickness=0)
        self.text_info.tag_configure('tag-center', justify='center')
        self.text_info.pack(side=tk.TOP, padx=10, pady=10)
        self.text_info.insert('end', "App megafiga by Miky & Kary\n", 'tag-center')
        self.text_info.insert('end', "Developed with ...", 'tag-center')

    def start(self):
        # Show the App Menu
        self.frame_menu.pack(anchor=tk.CENTER, fill=None, expand=False)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 1
        self.update()
        self.window.mainloop()

    def show_app(self):
        print("START POKÉDEX APP")
        self.frame_menu.pack_forget()
        self.frame_left.pack(side=tk.LEFT, fill=None, expand=False)
        self.frame_right.pack(side=tk.RIGHT, fill=None, expand=False)

    def update(self):
        ret, frame = self.video.get_frame()
        if ret:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame).resize((240, 240), Image.ANTIALIAS))
            self.canvas_video.create_image(120, 120, image=self.photo, anchor=tk.CENTER)  # this way the image is put at the center of the canvas

        self.window.after(self.delay, self.update)


    def load_pokemon(self, pkmn_id):
        try:
            pkmn_id = pkmn_id.capitalize()
            print("POKÉMON LOADED: " + pkmn_id)
            self.loaded_pokemon = self.pokemon_repo.pokemon[pkmn_id]

            self.load_image()
            self.load_name()
            self.load_id()
            self.load_types()
            self.load_description()
            self.load_stats()
            self.load_evolutions()
            self.load_cry()
        except KeyError:
            print("Pokémon not found.")

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

    # update ID
    def load_id(self):
        print("ID:" + str(self.loaded_pokemon.num))
        self.entry_id_text.set(str(self.loaded_pokemon.num))

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

    # update cry
    def load_cry(self):
        self.cry = pygame.mixer.Sound(cries_path + str(self.loaded_pokemon.num) + ".ogg")

    # show previous "to" evolution (e.g. Eevee multiple evolutions)
    def show_prev_evo_to(self):
        self.evo_to_i -= 1
        evo_to = self.pokemon_repo.pokemon[self.loaded_pokemon.name].evolutions["to"]
        print("Show previous evolution: " + str(evo_to[self.evo_to_i]))
        self.image_evo_to = ImageTk.PhotoImage(Image.open(sprites_path + str(evo_to[self.evo_to_i]) + ".png").resize((40, 40), Image.ANTIALIAS))
        self.label_evo_to.configure(image=self.image_evo_to)
        self.button_evo_to_next.config(state=tk.NORMAL)
        if self.evo_to_i == 0:
            self.button_evo_to_prev.config(state=tk.DISABLED)

    # show next "to" evolution (e.g. Eevee multiple evolutions)
    def next_evo_to(self):
        self.evo_to_i += 1
        evo_to = self.pokemon_repo.pokemon[self.loaded_pokemon.name].evolutions["to"]
        print("Show next evolution: " + str(evo_to[self.evo_to_i]))
        self.image_evo_to = ImageTk.PhotoImage(Image.open(sprites_path + str(evo_to[self.evo_to_i]) + ".png").resize((40, 40), Image.ANTIALIAS))
        self.label_evo_to.configure(image=self.image_evo_to)
        self.button_evo_to_prev.config(state=tk.NORMAL)
        if self.evo_to_i + 1 == len(evo_to):
            self.button_evo_to_next.config(state=tk.DISABLED)

    # Play cry
    def play_cry(self):
        if 1 <= self.loaded_pokemon.num <= 151 or self.loaded_pokemon.num == 257:
            print("PLAY CRY\nPokémon #" + str(self.loaded_pokemon.num) + " Volume: " + str(self.channel.get_volume()))
            self.channel.play(self.cry)
        else:
            print("No pokémon has been loaded")

    # Show settings
    def show_settings(self):
        print("SHOW SETTINGS")
        self.scale_volume.set(self.volume * 100)
        self.frame_right.pack_forget()
        self.frame_settings.pack(side=tk.RIGHT, fill=None, expand=False)

    # Show info
    def show_info(self):
        print("SHOW INFO")
        self.frame_right.pack_forget()
        self.frame_info.pack(side=tk.RIGHT, fill=None, expand=False)

    def close_settings(self):
        if self.window.attributes("-fullscreen") == 1:
            self.check_fullscreen.select()
            self.fullscreen.set(True)
        else:
            self.check_fullscreen.deselect()
            self.fullscreen.set(False)
        self.channel.set_volume(self.volume)
        self.frame_settings.pack_forget()
        self.frame_right.pack(side=tk.RIGHT, fill=None, expand=False)
        print("CLOSE SETTINGS\nFullscreen: " + str(bool(self.fullscreen.get())) + "\nVolume: " + str(self.volume))

    def save_settings(self):
        self.window.attributes("-fullscreen", self.fullscreen.get())
        self.volume = self.scale_volume.get() / 100
        self.channel.set_volume(self.volume)
        self.frame_settings.pack_forget()
        self.frame_right.pack(side=tk.RIGHT, fill=None, expand=False)
        print("SAVE SETTINGS\nFullscreen: " + str(bool(self.fullscreen.get())) + "\nVolume: " + str(self.volume))

    def close_info(self):
        print("CLOSE INFO")
        self.frame_info.pack_forget()
        self.frame_right.pack(side=tk.RIGHT, fill=None, expand=False)

    # get RGB color from stat
    def get_color(self, stat):
        if 0 <= stat < 25:
            return "#ff0000"
        elif 25 <= stat < 50:
            return "#ff5500"
        elif 50 <= stat < 75:
            return "#ffaa00"
        elif 75 <= stat < 100:
            return "#ffff00"
        elif 100 <= stat < 125:
            return "#7fff00"
        elif 125 <= stat < 150:
            return "#00ff00"
        elif 150 <= stat < 200:
            return "#00ff80"
        return "#00ffff"

    def save_video_snapshot(self):
        # Get a frame from the video source
        ret, frame = self.video.get_frame()
        if ret:
            cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def save_window_snapshot(self):
        print("Window snapshot")

    def save_screenshot(self):
        pg.screenshot("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg")

    def quit(self):
        print("QUIT")
        self.window.destroy()
        exit(0)

app = App(tk.Tk(), "pokédex")
app.start()
