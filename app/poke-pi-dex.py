import sys
import tkinter as tk
from tkinter import font
from tkinter import ttk
from PIL import ImageTk, Image
import cv2
import time
# Sound
import pygame
# Screenshot
import pyautogui as pg

from pokemon_repository import PokemonRepository
import video_capture as vc
from labels import load_labels
import settings
from image_rectifier import rectify_image
import pokemon_classifier_tflite as pc
'''try:
    from input import register_button
except ModuleNotFoundError:
    print("Buttons disabled")'''

# tkinter utility: https://www.tcl.tk/man/tcl/TkCmd/entry.html#M9

app_name = "Poké-Pi-Dex"
version = "1.0 beta"
res_width = 800
res_height = 600
image_size = (int(res_width/2), int(res_width/2))  # 240x240
icon_size = (int(res_width/19.2), int(res_width/19.2))  # 25x25
background = "grey"
background_dark = "#6a6a6a"
icons_path = "resources/icons/"
thumbnails_path = "resources/thumbnails/"
sprites_path = "resources/sprites/"
types_path = "resources/types/"
cries_path = "resources/cries (ogg)/"
sprite_size = (int(res_width/12), int(res_width/12))
labels = load_labels("resources/labels.json")
# Stats coordinates
x1 = int(res_width / 240)   # 2
y1 = int(res_height / 120)  # 4
x2 = int(res_width / 9.6)   # 50
y2 = int(res_height / 20)   # 16


class App:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        self.window.geometry(str(res_width) + "x" + str(res_height))
        image = ImageTk.PhotoImage(file=icons_path + "icon-pokeball.png")
        self.window.tk.call("wm", "iconphoto", self.window._w, image)
        self.window.configure(bg=background)
        # Video Source
        self.video = None
        self.update_video = False

        # Settings Loading
        self.settings = settings.Settings(window, "resources/.settings.json")
        self.settings.load_from_file()
        self.window.attributes("-fullscreen", self.settings.fullscreen.get())

        # Parameters Check
        if 2 <= len(sys.argv) <= 3 and sys.argv[1] == "-d":
            try:
                if 2 <= int(sys.argv[2]) <= 10:
                    self.settings.debug_mode = int(sys.argv[2])
            except ValueError and IndexError:
                self.settings.debug_mode = 5
            print("Debug mode: ON (" + str(self.settings.debug_mode) + ")")
        else:
            print("Debug mode: OFF")

        # Sound init
        pygame.mixer.pre_init(44100, -16, 1, 4096)  # default freq: 44100, but on the raspberry it causes a fastidious high pitched noise
        pygame.init()
        pygame.mixer.init()
        # Channel init
        self.mono_channel = pygame.mixer.find_channel(True)
        self.mono_channel.set_volume(self.settings.volume)

        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(family="Helvetica", size=int(res_width/40))

        # Repository Loading
        self.pokemon_repo = PokemonRepository("resources/first_gen_pokedex.json")
        self.loaded_pokemon = None
        self.evo_to_i = 0  # index of the multiple evolutions list

        # Menu
        self.frame_menu = tk.Frame(width=res_width, height=res_height, background=background)
        self.frame_menu.pack_propagate(0)
        self.canvas_background = tk.Canvas(master=self.frame_menu, width=res_width, height=res_height, highlightbackground=background, highlightthickness=1)
        self.canvas_background.pack()
        image = Image.open("resources/images/menu-background.png").resize((res_width, res_height), Image.ANTIALIAS)
        self.image_background = ImageTk.PhotoImage(image)
        self.canvas_background.create_image(0, 0, anchor=tk.NW, image=self.image_background)
        self.label_app_version = tk.Label(master=self.frame_menu, text="v" + version, width=10, bg="black", fg="grey")
        self.label_app_version.config(font=("Helvetica", int(res_width/48), "italic bold"))
        self.canvas_background.create_window(int(res_width/2.436), int(res_height/3.516), anchor=tk.N, window=self.label_app_version)  # (197, 91)
        self.text_start = tk.StringVar()
        self.text_start.set(labels["start"][self.settings.language])
        self.button_start = tk.Button(master=self.frame_menu, textvar=self.text_start, width=15, bg=background, activebackground=background, command=lambda: self.show_app())
        self.canvas_background.create_window(int(res_width/2.436), int(res_height/1.758), anchor=tk.N, window=self.button_start)  # 197, 132+50
        self.text_quit = tk.StringVar()
        self.text_quit.set(labels["quit"][self.settings.language])
        self.button_quit = tk.Button(master=self.frame_menu, textvar=self.text_quit, width=15, bg=background, activebackground=background, command=lambda: self.quit())
        self.canvas_background.create_window(int(res_width/2.436), int(res_height/1.379), anchor=tk.N, window=self.button_quit)  # 197, 182+50
        self.image_button_info = ImageTk.PhotoImage(Image.open(icons_path + "icon-info.png").resize((icon_size), Image.ANTIALIAS))  # 25, 25
        self.button_info = tk.Button(master=self.frame_menu, image=self.image_button_info, bg=background, command=lambda: self.show_info())
        self.canvas_background.create_window(int(res_width/1.490), int(res_height/1.221), anchor=tk.N, window=self.button_info)  # 322, 232+30

        # Info
        self.frame_info = tk.Frame(master=self.frame_menu, width=int(res_width/1.528), height=int(res_height/1.333), bg=background)  # 314, 240
        self.frame_info.pack_propagate(0)
        self.image_button_close = ImageTk.PhotoImage(Image.open(icons_path + "icon-close.png").resize(icon_size, Image.ANTIALIAS))
        self.button_close = tk.Button(master=self.frame_info, image=self.image_button_close, bg=background, command=lambda: self.close_info())
        self.button_close.pack(side=tk.TOP, anchor=tk.E, padx=(0, 2), pady=(2, 0))
        self.label_info_name = tk.Label(master=self.frame_info, text=app_name+" v"+version, bg=background_dark, font=("Helvetica", int(res_width/48), "bold"))
        self.label_info_name.pack(side=tk.TOP, anchor=tk.CENTER, pady=(0, int(res_width/48)))
        self.text_info_description = tk.Text(master=self.frame_info, height=3, bg=background_dark, bd=0, highlightthickness=0, font=("Helvetica", int(res_width / 60), "normal"))
        self.text_info_description.tag_configure('tag-center', justify='center')
        self.text_info_description.pack(side=tk.TOP, anchor=tk.CENTER, padx=(int(res_width/48), int(res_width/48)), pady=(0, int(res_width/48)))
        self.text_info_description.insert('1.0', labels["info"][self.settings.language], 'tag-center')
        self.text_info_description.config(state="disabled")
        self.frame_info_images = tk.Frame(master=self.frame_info, bg=background)
        self.frame_info_images.pack(side=tk.TOP, padx=(int(res_width/48), int(res_width/48)), fill=tk.X)
        # Kary
        self.frame_image_kary = tk.Frame(master=self.frame_info_images, bg=background)
        self.frame_image_kary.pack(side=tk.LEFT)
        img_size = (int(res_width / 7.385), int(res_width / 7.385))
        self.image_kary = ImageTk.PhotoImage(Image.open("resources/images/kary.png").resize(img_size, Image.ANTIALIAS))
        self.label_info_image_kary = tk.Label(master=self.frame_image_kary, image=self.image_kary, bg=background)
        self.label_info_image_kary.pack(side=tk.TOP, anchor=tk.CENTER)
        self.label_info_kary = tk.Label(master=self.frame_image_kary, text="Karina Chichifoi", bg=background_dark, font=("Helvetica", int(res_width/60), "normal"))
        self.label_info_kary.pack(side=tk.TOP, anchor=tk.CENTER)
        self.label_info_kary = tk.Label(master=self.frame_image_kary, text="Unibo MSc Student", bg=background_dark, font=("Helvetica", int(res_width/60), "normal"))
        self.label_info_kary.pack(side=tk.TOP, anchor=tk.CENTER)
        # Miky
        self.frame_image_miky = tk.Frame(master=self.frame_info_images, bg=background)
        self.frame_image_miky.pack(side=tk.RIGHT)
        self.image_miky = ImageTk.PhotoImage(Image.open("resources/images/miky.png").resize(img_size, Image.ANTIALIAS))
        self.label_info_image_miky = tk.Label(master=self.frame_image_miky, image=self.image_miky, bg=background)
        self.label_info_image_miky.pack(side=tk.TOP, anchor=tk.CENTER)
        self.label_info_miky = tk.Label(master=self.frame_image_miky, text="Michele Righi", bg=background_dark, font=("Helvetica", int(res_width / 60), "normal"))
        self.label_info_miky.pack(side=tk.TOP, anchor=tk.CENTER)
        self.label_info_miky = tk.Label(master=self.frame_image_miky, text="Unibo MSc Student", bg=background_dark, font=("Helvetica", int(res_width/60), "normal"))
        self.label_info_miky.pack(side=tk.TOP, anchor=tk.CENTER)
        self.window_info = None

        # Pokédex App
        self.frame_left = tk.Frame(width=(res_width/2)-1, height=res_height, bg=background)
        self.frame_left.pack_propagate(0)  # set the frame so that its children cannot control its size
        self.frame_right = tk.Frame(width=(res_width/2)-1, height=res_height, bg=background)
        self.frame_right.pack_propagate(0)

        # Left (video stream)
        self.entry_prediction_text = tk.StringVar()
        self.entry_prediction = tk.Entry(master=self.frame_left, width=20, textvar=self.entry_prediction_text, bg=background, fg=background_dark, bd=0, highlightthickness=0, font=default_font)
        self.entry_prediction.config(readonlybackground=background, state="readonly")
        self.entry_prediction.pack(side=tk.TOP, pady=(int(res_height/32), int(res_height/160)))

        self.canvas_video = tk.Canvas(master=self.frame_left, width=res_width/2, height=res_width/2, bg=background, highlightbackground=background, highlightthickness=1)
        self.canvas_video.pack(side=tk.TOP)

        self.frame_video_controls = tk.Frame(master=self.frame_left, bg=background)
        self.frame_video_controls.pack(side=tk.TOP, pady=(int(res_height/160), 0))
        self.text_search = tk.StringVar()
        self.text_search.set(labels["search"][self.settings.language])
        self.button_search = tk.Button(master=self.frame_video_controls, textvar=self.text_search, width=10, bg=background, activebackground=background, command=lambda: self.search())  # self.load_pokemon(self.entry_name_text.get())
        self.button_search.pack(side=tk.LEFT, anchor=tk.CENTER, padx=(0, int(res_width/48)))
        self.text_screenshot = tk.StringVar()
        self.text_screenshot.set(labels["screenshot"][self.settings.language])
        self.button_screenshot = tk.Button(master=self.frame_video_controls, textvar=self.text_screenshot, width=10, bg=background, activebackground=background, command=lambda: self.save_screenshot())
        self.button_screenshot.pack(side=tk.LEFT, anchor=tk.CENTER)

        # Right (Pokémon details)
        # Top
        self.frame_top = tk.Frame(master=self.frame_right, width=res_width/2, bg=background)
        self.frame_top.pack(side=tk.TOP, fill=tk.X)

        # Top-left:
        self.frame_top_left = tk.Frame(master=self.frame_top, width=int(res_width/5.517), height=int(res_height/4.923), bg=background)  # 87, 65
        self.frame_top_left.pack(side=tk.LEFT, anchor=tk.N)
        # Top-left up (pre-evolution)
        self.frame_top_left_upper = tk.Frame(master=self.frame_top_left, bg=background)
        self.frame_top_left_upper.pack(side=tk.TOP, anchor=tk.E)
        # Easter Egg: loads Blaziken, even if it's not in the first gen
        self.button_egg = tk.Button(master=self.frame_top_left_upper, width=2, bg=background, fg=background, bd=0, highlightthickness=0, command=lambda: self.load_pokemon('Blaziken'))
        self.button_egg.pack(side=tk.LEFT, anchor=tk.N)
        # Evolution (from)
        img_size = (int(res_width/12), int(res_width/12))
        image = Image.open(sprites_path + "0.png").resize(img_size, Image.ANTIALIAS)
        self.image_evo_from = ImageTk.PhotoImage(image)
        self.label_evo_from = tk.Label(master=self.frame_top_left_upper, image=self.image_evo_from, bg=background)
        self.label_evo_from.pack(side=tk.RIGHT, anchor=tk.N, padx=(int(res_width/20), 0))

        # Cry
        self.frame_cry = tk.Frame(master=self.frame_top_left, width=int(res_width/5.517), bg=background)
        self.frame_cry.pack(side=tk.BOTTOM, anchor=tk.W)
        self.text_cry = tk.StringVar()
        self.text_cry.set(labels["cry"][self.settings.language])
        self.label_cry = tk.Label(master=self.frame_cry, textvar=self.text_cry, bg=background)
        self.label_cry.pack(side=tk.LEFT)
        img_size = (int(res_width/24), int(res_width/24))
        self.image_button_cry = ImageTk.PhotoImage(Image.open(icons_path + "icon-sound.png").resize(img_size, Image.ANTIALIAS))
        self.button_cry = tk.Button(master=self.frame_cry, image=self.image_button_cry, bg=background, activebackground=background, command=lambda: self.play_cry())
        self.button_cry.pack(side=tk.LEFT)

        # Image (Top Center)
        img_size = (int(res_width/7.385), int(res_width/7.385))
        image = Image.open(thumbnails_path + "0.png").resize(img_size, Image.ANTIALIAS)
        self.thumbnail = ImageTk.PhotoImage(image)
        self.label_thumb = tk.Label(master=self.frame_top, image=self.thumbnail, bg=background)
        self.label_thumb.pack(side=tk.LEFT, anchor=tk.N, fill=tk.BOTH)

        # Top Right:
        self.frame_top_right = tk.Frame(master=self.frame_top, width=int(res_width/5.517), bg=background)
        self.frame_top_right.pack(side=tk.LEFT, fill=tk.X, anchor=tk.N)
        # Evolution (to)
        image = Image.open(sprites_path + "0.png").resize(sprite_size, Image.ANTIALIAS)
        self.image_evo_to = ImageTk.PhotoImage(image)
        self.label_evo_to = tk.Label(master=self.frame_top_right, image=self.image_evo_to, width=int(res_width/12), height=int(res_width/12), bg=background)
        self.label_evo_to.pack(side=tk.TOP, anchor=tk.W)
        # Buttons (for multiple "to" evolutions)
        img_size = (int(res_width/48), int(res_width/48))
        self.image_button_evo_prev = ImageTk.PhotoImage(Image.open(icons_path + "icon-evo-to-prev.png").resize(img_size, Image.ANTIALIAS))
        self.button_evo_to_prev = tk.Button(master=self.frame_top_right, image=self.image_button_evo_prev, bg=background, command=lambda: self.show_prev_evo_to())
        self.button_evo_to_prev.config(state=tk.DISABLED)
        self.button_evo_to_prev.pack(side=tk.LEFT, anchor=tk.N)
        self.image_button_evo_next = ImageTk.PhotoImage(Image.open(icons_path + "icon-evo-to-next.png").resize(img_size, Image.ANTIALIAS))
        self.button_evo_to_next = tk.Button(master=self.frame_top_right, image=self.image_button_evo_next, bg=background, command=lambda: self.next_evo_to())
        self.button_evo_to_next.config(state=tk.DISABLED)
        self.button_evo_to_next.pack(side=tk.LEFT, anchor=tk.N)

        # Settings & Back
        self.frame_settings_back = tk.Frame(master=self.frame_top, bg=background)
        self.frame_settings_back.pack(side=tk.RIGHT, anchor=tk.N, padx=(10, 2), pady=(1, 0))
        self.image_button_settings = ImageTk.PhotoImage(Image.open(icons_path + "icon-settings.png").resize(icon_size, Image.ANTIALIAS))
        self.button_settings = tk.Button(master=self.frame_settings_back, image=self.image_button_settings, bg=background, command=lambda: self.show_settings())
        self.button_settings.pack(side=tk.TOP, anchor=tk.E, padx=(0, 2), pady=(2, 0))
        self.image_button_back = ImageTk.PhotoImage(Image.open(icons_path + "icon-back.png").resize(icon_size, Image.ANTIALIAS))
        self.button_back = tk.Button(master=self.frame_settings_back, image=self.image_button_back, bg=background, command=lambda: self.show_menu())
        self.button_back.pack(side=tk.TOP, anchor=tk.E, padx=(0, 2), pady=(2, 0))

        # Name
        self.frame_name = tk.Frame(master=self.frame_right, bg=background)
        self.frame_name.pack(side=tk.TOP, pady=(int(res_height/80), int(res_height/80)))
        self.text_name = tk.StringVar()
        self.text_name.set(labels["name"][self.settings.language])
        self.label_name = tk.Label(master=self.frame_name, textvar=self.text_name, bg=background)
        self.label_name.pack(side=tk.LEFT)
        self.entry_name_text = tk.StringVar()
        self.entry_name = tk.Entry(master=self.frame_name, width=11, textvariable=self.entry_name_text, font=default_font, bg=background_dark, bd=0, highlightthickness=0)
        self.entry_name.config(readonlybackground=background_dark, state="readonly")
        self.entry_name.pack(side=tk.LEFT)

        # ID and Type(s)
        self.frame_id_types = tk.Frame(master=self.frame_right, bg=background)
        self.frame_id_types.pack(side=tk.TOP, pady=(0, int(res_height/80)))
        self.label_id = tk.Label(master=self.frame_id_types, text="ID: ", bg=background)
        self.label_id.pack(side=tk.LEFT)
        self.entry_id_text = tk.StringVar()
        self.entry_id = tk.Entry(master=self.frame_id_types, width=3, textvariable=self.entry_id_text, font=default_font, bg=background_dark, bd=0, highlightthickness=0)
        self.entry_id.config(readonlybackground=background_dark, state="readonly")
        self.entry_id.pack(side=tk.LEFT)
        self.text_types = tk.StringVar()
        self.text_types.set(labels["types"][self.settings.language])
        self.label_types = tk.Label(master=self.frame_id_types, textvar=self.text_types, bg=background)
        self.label_types.pack(side=tk.LEFT)
        '''self.entry_types_text = tk.StringVar()
        self.entry_types = tk.Entry(master=self.frame_id_types, textvariable=self.entry_types_text, width=18, bd=0, highlightthickness=0)'''
        self.canvas_types = tk.Canvas(master=self.frame_id_types, width=res_width/2, height=int(res_height/14.28), bg=background, highlightthickness=0)
        img_size = (int(res_width/9.38), int(res_height/14.28))
        image = Image.open(types_path + "Unknown_en.png").resize(img_size, Image.ANTIALIAS)
        self.image_type1 = ImageTk.PhotoImage(image)
        self.canvas_image_type1 = self.canvas_types.create_image(0, 0, anchor=tk.NW, image=self.image_type1)
        image = Image.open(types_path + "/Unknown_en.png").resize(img_size, Image.ANTIALIAS)
        self.image_type2 = ImageTk.PhotoImage(image)
        self.canvas_image_type2 = self.canvas_types.create_image(int(res_width/8.5), 0, anchor=tk.NW, image=self.image_type2)
        self.canvas_types.pack(side=tk.LEFT)

        # Description
        self.text_description = tk.Text(master=self.frame_right, height=5, bg=background_dark, bd=0, highlightthickness=0)
        self.text_description.config(font=("Helvetica", int(res_width/48), "normal"), state="disabled")
        self.text_description.pack(side=tk.TOP, pady=(0, int(res_height/80)), padx=(0, 5))

        # HP
        self.frame_hp = tk.Frame(master=self.frame_right, width=res_width/2, bg=background)
        self.frame_hp.pack(side=tk.TOP)
        self.text_hp = tk.StringVar(value=labels["hp"][self.settings.language])
        self.label_hp = tk.Label(master=self.frame_hp, width=8, textvar=self.text_hp, anchor=tk.W, bg=background)
        self.entry_hp_text = tk.StringVar()
        self.entry_hp = tk.Entry(master=self.frame_hp, width=3, textvariable=self.entry_hp_text, bd=0, highlightthickness=0, font=default_font)
        self.entry_hp.config(readonlybackground=background_dark, state="readonly")
        self.canvas_hp = tk.Canvas(master=self.frame_hp, width=int(res_width/3), height=int(res_height/17.78), bg=background, highlightthickness=0)  # highlightthickness=0 to remove the white borders
        self.rect_hp = self.canvas_hp.create_rectangle(x1, y1, x2, y2, fill="red")  # x1, y1, x2, y2
        self.label_hp.pack(side=tk.LEFT)
        self.entry_hp.pack(side=tk.LEFT)
        self.canvas_hp.pack(side=tk.LEFT)
        # Attack
        self.frame_attack = tk.Frame(master=self.frame_right, width=res_width/2, bg=background)
        self.frame_attack.pack(side=tk.TOP)
        self.text_atk = tk.StringVar(value=labels["attack"][self.settings.language])
        self.label_attack = tk.Label(master=self.frame_attack, width=8, textvar=self.text_atk, anchor=tk.W, bg=background)  # anchor=tk.W to justify the text
        self.entry_attack_text = tk.StringVar()
        self.entry_attack = tk.Entry(master=self.frame_attack, width=3, textvariable=self.entry_attack_text, bd=0, highlightthickness=0, font=default_font)
        self.entry_attack.config(readonlybackground=background_dark, state="readonly")
        self.canvas_attack = tk.Canvas(master=self.frame_attack, width=int(res_width/3), height=int(res_height/17.78), bg=background, highlightthickness=0)
        self.rect_attack = self.canvas_attack.create_rectangle(x1, y1, x2, y2, fill="red")
        self.label_attack.pack(side=tk.LEFT)
        self.entry_attack.pack(side=tk.LEFT)
        self.canvas_attack.pack(side=tk.LEFT)
        # Defense
        self.frame_defense = tk.Frame(master=self.frame_right, width=res_width/2, bg=background)
        self.frame_defense.pack(side=tk.TOP)
        self.text_def = tk.StringVar(value=labels["defense"][self.settings.language])
        self.label_defense = tk.Label(master=self.frame_defense, width=8, textvar=self.text_def, anchor=tk.W, bg=background)
        self.entry_defense_text = tk.StringVar()
        self.entry_defense = tk.Entry(master=self.frame_defense, width=3, textvariable=self.entry_defense_text, bd=0, highlightthickness=0, font=default_font)
        self.entry_defense.config(readonlybackground=background_dark, state="readonly")
        self.canvas_defense = tk.Canvas(master=self.frame_defense, width=int(res_width/3), height=int(res_height/17.78), bg=background, highlightthickness=0)
        self.rect_defense = self.canvas_defense.create_rectangle(x1, y1, x2, y2, fill="red")
        self.label_defense.pack(side=tk.LEFT)
        self.entry_defense.pack(side=tk.LEFT)
        self.canvas_defense.pack(side=tk.LEFT)
        # Sp. Atk
        self.frame_sp_atk = tk.Frame(master=self.frame_right, width=res_width/2, bg=background)
        self.frame_sp_atk.pack(side=tk.TOP)
        self.text_spatk = tk.StringVar(value=labels["sp. atk"][self.settings.language])
        self.label_sp_atk = tk.Label(master=self.frame_sp_atk, width=8, textvar=self.text_spatk, anchor=tk.W, bg=background)
        self.entry_sp_atk_text = tk.StringVar()
        self.entry_sp_atk = tk.Entry(master=self.frame_sp_atk, width=3, textvariable=self.entry_sp_atk_text, bd=0, highlightthickness=0, font=default_font)
        self.entry_sp_atk.config(readonlybackground=background_dark, state="readonly")
        self.canvas_sp_atk = tk.Canvas(master=self.frame_sp_atk, width=int(res_width/3), height=int(res_height/17.78), bg=background, highlightthickness=0)
        self.rect_sp_atk = self.canvas_sp_atk.create_rectangle(x1, y1, x2, y2, fill="red")
        self.label_sp_atk.pack(side=tk.LEFT)
        self.entry_sp_atk.pack(side=tk.LEFT)
        self.canvas_sp_atk.pack(side=tk.LEFT)
        # Sp. Def
        self.frame_sp_def = tk.Frame(master=self.frame_right, width=res_width/2, bg=background)
        self.frame_sp_def.pack(side=tk.TOP)
        self.text_spdef = tk.StringVar(value=labels["sp. def"][self.settings.language])
        self.label_sp_def = tk.Label(master=self.frame_sp_def, width=8, textvar=self.text_spdef, anchor=tk.W, bg=background)
        self.entry_sp_def_text = tk.StringVar()
        self.entry_sp_def = tk.Entry(master=self.frame_sp_def, width=3, textvariable=self.entry_sp_def_text, bd=0, highlightthickness=0, font=default_font)
        self.entry_sp_def.config(readonlybackground=background_dark, state="readonly")
        self.canvas_sp_def = tk.Canvas(master=self.frame_sp_def, width=int(res_width/3), height=int(res_height/17.78), bg=background, highlightthickness=0)
        self.rect_sp_def = self.canvas_sp_def.create_rectangle(x1, y1, x2, y2, fill="red")
        self.label_sp_def.pack(side=tk.LEFT)
        self.entry_sp_def.pack(side=tk.LEFT)
        self.canvas_sp_def.pack(side=tk.LEFT)
        # Speed
        self.frame_speed = tk.Frame(master=self.frame_right, width=res_width/2, bg=background)
        self.frame_speed.pack(side=tk.TOP)
        self.text_speed = tk.StringVar(value=labels["speed"][self.settings.language])
        self.label_speed = tk.Label(master=self.frame_speed, width=8, textvar=self.text_speed, anchor=tk.W, bg=background)
        self.entry_speed_text = tk.StringVar()
        self.entry_speed = tk.Entry(master=self.frame_speed, width=3, textvariable=self.entry_speed_text, bd=0, highlightthickness=0, font=default_font)
        self.entry_speed.config(readonlybackground=background_dark, state="readonly")
        self.canvas_speed = tk.Canvas(master=self.frame_speed, width=int(res_width/3), height=int(res_height/17.78), bg=background, highlightthickness=0)
        self.rect_speed = self.canvas_speed.create_rectangle(x1, y1, x2, y2, fill="red")
        self.label_speed.pack(side=tk.LEFT)
        self.entry_speed.pack(side=tk.LEFT)
        self.canvas_speed.pack(side=tk.LEFT)

        # Settings
        self.frame_settings = tk.Frame(width=res_width/2, height=res_height, bg=background)
        self.frame_settings.pack_propagate(0)
        self.button_close = tk.Button(master=self.frame_settings, image=self.image_button_close, bg=background, command=lambda: self.close_settings())
        self.button_close.pack(side=tk.TOP, anchor=tk.E, padx=(0, 2), pady=(2, 0))
        self.text_settings = tk.StringVar(value=labels["settings"][self.settings.language])
        self.frame_label_settings = tk.Frame(self.frame_settings, width=res_width/2, bg=background)
        self.frame_label_settings.pack(side=tk.TOP, fill=tk.X)
        self.image_button_empty = ImageTk.PhotoImage(Image.open(icons_path + "icon-empty.png").resize(icon_size, Image.ANTIALIAS))
        self.button_label_settings = tk.Button(master=self.frame_label_settings, image=self.image_button_empty, bg=background, fg=background, bd=0, highlightthickness=0)
        self.button_label_settings.pack(side=tk.LEFT)
        self.button_label_settings.config(state=tk.DISABLED)
        self.label_settings = tk.Label(master=self.frame_label_settings, textvar=self.text_settings, bg=background)
        self.label_settings.config(font=("Helvetica", int(res_width/30), "bold italic"))
        self.label_settings.pack(side=tk.LEFT)
        self.image_button_debug = ImageTk.PhotoImage(Image.open(icons_path + "icon-bug.png").resize(icon_size, Image.ANTIALIAS))
        self.button_debug = tk.Button(master=self.frame_label_settings, image=self.image_button_debug, bg=background, command=lambda: self.debug_counter())
        self.button_debug.pack(side=tk.RIGHT, padx=(0, 2), pady=(2, 0))

        # Language Picker
        self.frame_language = tk.Frame(master=self.frame_settings, width=res_width/2, bg=background)
        self.frame_language.pack(side=tk.TOP, anchor=tk.W, fill=tk.X, pady=(5, 0), padx=(10, 0))
        self.text_language = tk.StringVar(value=labels["language"][self.settings.language])
        self.label_language = tk.Label(master=self.frame_language, textvar=self.text_language, width=12, anchor=tk.W, bg=background)
        self.label_language.pack(side=tk.LEFT)
        self.combobox_language_text = tk.StringVar()
        self.combobox_language = ttk.Combobox(master=self.frame_language, state="readonly", textvariable=self.combobox_language_text, values=list(labels["languages"].keys()), width=9, font=default_font)
        self.combobox_language.current(0)
        self.combobox_language.pack(side=tk.RIGHT, padx=(0, 10))
        self.combobox_language.bind("<<ComboboxSelected>>", lambda e: self.frame_language.focus())  # just for aesthetics
        # Toggle Fullscreen
        self.frame_fullscreen = tk.Frame(master=self.frame_settings, width=res_width/2, bg=background)
        self.frame_fullscreen.pack(side=tk.TOP, anchor=tk.W, fill=tk.X, pady=(5, 0), padx=(10, 0))
        self.check_fullscreen = tk.Checkbutton(master=self.frame_fullscreen, variable=self.settings.fullscreen, onvalue=1, offvalue=0, bg=background, bd=0, highlightthickness=0, fg="black")
        self.text_fullscreen = tk.StringVar(value=labels["full screen"][self.settings.language])
        self.label_fullscreen = tk.Label(master=self.frame_fullscreen, textvar=self.text_fullscreen, width=12, anchor=tk.W, bg=background)
        self.label_fullscreen.pack(side=tk.LEFT)
        self.check_fullscreen.select() if self.settings.fullscreen.get() == 1 else self.check_fullscreen.deselect()
        self.check_fullscreen.pack(side=tk.RIGHT, padx=(0, 10))
        # Toggle Description Voice
        self.var_descr_voice = tk.IntVar(value=self.settings.descr_voice)
        self.frame_descr_voice = tk.Frame(master=self.frame_settings, width=res_width / 2, bg=background)
        self.frame_descr_voice.pack(side=tk.TOP, anchor=tk.W, fill=tk.X, pady=(5, 0), padx=(10, 0))
        self.check_descr_voice = tk.Checkbutton(master=self.frame_descr_voice, variable=self.var_descr_voice, onvalue=1, offvalue=0, bg=background, bd=0, highlightthickness=0, fg="black")
        self.text_descr_voice = tk.StringVar(value=labels["descr voice"][self.settings.language])
        self.label_descr_voice = tk.Label(master=self.frame_descr_voice, textvar=self.text_descr_voice, width=12, anchor=tk.W, bg=background)
        self.label_descr_voice.pack(side=tk.LEFT)
        self.check_descr_voice.select() if self.var_descr_voice.get() == 1 else self.check_descr_voice.deselect()
        self.check_descr_voice.pack(side=tk.RIGHT, padx=(0, 10))
        # Toggle Flip Image
        self.frame_flip = tk.Frame(master=self.frame_settings, width=res_width/2, bg=background)
        self.frame_flip.pack(side=tk.TOP, anchor=tk.W, fill=tk.X, pady=(5, 0), padx=(10, 0))
        self.check_flip = tk.Checkbutton(master=self.frame_flip, onvalue=1, offvalue=0, bg=background, bd=0, highlightthickness=0, fg="black")
        self.text_flip = tk.StringVar(value=labels["flip image"][self.settings.language])
        self.label_flip = tk.Label(master=self.frame_flip, textvar=self.text_flip, width=12, anchor=tk.W, bg=background)
        self.label_flip.pack(side=tk.LEFT)
        # self.check_flip.select() if self.settings.fullscreen.get() == 1 else self.check_fullscreen.deselect()
        self.check_flip.pack(side=tk.RIGHT, padx=(0, 10))
        # Volume
        self.frame_volume = tk.Frame(master=self.frame_settings, width=res_width/2, bg=background)
        self.frame_volume.pack(side=tk.TOP, anchor=tk.W, fill=tk.X, pady=(5, 0), padx=(10, 0))
        self.text_volume = tk.StringVar(value=labels["volume"][self.settings.language])
        self.label_volume = tk.Label(master=self.frame_volume, textvar=self.text_volume, width=12, anchor=tk.W, bg=background)
        self.label_volume.pack(side=tk.LEFT)
        self.scale_volume = tk.Scale(master=self.frame_volume, from_=0, to=100, tickinterval=100, orient=tk.HORIZONTAL, bg=background, bd=0, highlightthickness=0)
        self.scale_volume.set(50)
        self.scale_volume.pack(side=tk.RIGHT, padx=(0, 10))
        # Save/Cancel buttons
        self.frame_settings_controls = tk.Frame(master=self.frame_settings, width=res_width/2, bg=background)
        self.frame_settings_controls.pack(side=tk.BOTTOM, pady=(0, 10))
        self.text_save = tk.StringVar(value=labels["save"][self.settings.language])
        self.button_save_settings = tk.Button(master=self.frame_settings_controls, textvar=self.text_save, bg=background, width=6, command=lambda: self.save_settings())
        self.button_save_settings.pack(side=tk.LEFT, anchor=tk.CENTER)
        self.text_cancel = tk.StringVar(value=labels["cancel"][self.settings.language])
        self.button_cancel_settings = tk.Button(master=self.frame_settings_controls, textvar=self.text_cancel, bg=background, command=lambda: self.close_settings())
        self.button_cancel_settings.pack(side=tk.LEFT, anchor=tk.CENTER, padx=10)

        # Debug Mode
        self.frame_debug = tk.Frame(width=res_width/2, height=res_height, bg=background)
        self.frame_debug.pack_propagate(0)
        self.button_close_debug = tk.Button(master=self.frame_debug, image=self.image_button_close, bg=background, command=lambda: self.close_debug_mode())
        self.button_close_debug.pack(side=tk.TOP, anchor=tk.E)
        self.text_debug_headers = tk.Text(master=self.frame_debug, height=1, width=24, bg="black", fg="white", bd=0, highlightthickness=0)
        self.text_debug_headers.insert('1.0', "#  Pokémon\t\t%")
        fixed_font = ("TkFixedFont", 14, "normal")
        self.text_debug_headers.config(font=fixed_font, state="disabled")
        self.text_debug_headers.pack(side=tk.TOP)
        self.text_debug = tk.Text(master=self.frame_debug, height=int(res_height/22.86), width=24, bg="black", fg="white", bd=0, highlightthickness=0)
        self.text_debug.config(font=fixed_font, state="disabled")
        self.text_debug.pack(side=tk.TOP)

    def start(self):
        # Show the App Menu
        self.show_menu()
        self.video = vc.VideoCapture()
        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 1
        self.update()
        self.window.mainloop()

    def show_menu(self):
        self.mono_channel.stop()
        self.frame_info.pack_forget()
        self.frame_left.pack_forget()
        self.frame_right.pack_forget()
        self.frame_settings.pack_forget()
        if self.video:
            self.video.close()
        self.update_video = False
        print("SHOW MENU")
        self.frame_menu.pack(anchor=tk.CENTER, fill=None, expand=False)

    def show_info(self):
        print("SHOW INFO")
        self.window_info = self.canvas_background.create_window(int(res_width/2.437), int(res_height/8), anchor=tk.N, window=self.frame_info)  # 157+40, 40
        self.button_start.config(state=tk.DISABLED)
        self.button_quit.config(state=tk.DISABLED)
        self.button_info.config(state=tk.DISABLED)

    def close_info(self):
        print("CLOSE INFO")
        self.canvas_background.delete(self.window_info)
        self.button_start.config(state=tk.NORMAL)
        self.button_quit.config(state=tk.NORMAL)
        self.button_info.config(state=tk.NORMAL)

    def show_app(self):
        self.frame_menu.pack_forget()
        self.frame_info.pack_forget()
        self.frame_settings.pack_forget()
        self.frame_debug.pack_forget()
        self.video.open()
        self.update_video = True
        self.frame_left.pack(side=tk.LEFT, fill=None, expand=False, padx=(0, 1))
        self.reset_pokemon()
        if self.settings.debug_mode != 0:
            print("START POKÉDEX APP (DEBUG)")
            self.frame_debug.pack(side=tk.RIGHT, fill=None, expand=False, padx=(1, 0))
            return
        print("START POKÉDEX APP")
        self.frame_right.pack(side=tk.RIGHT, fill=None, expand=False, padx=(1, 0))

    def show_debug_mode(self):
        self.frame_right.pack_forget()
        self.frame_settings.pack_forget()
        print("SHOW DEBUG")
        self.frame_debug.pack(side=tk.RIGHT, fill=None, expand=False, padx=(1, 0))

    def close_debug_mode(self):
        self.settings.debug_mode = 0
        self.text_debug.config(state=tk.NORMAL)
        self.text_debug.delete('1.0', tk.END)
        self.text_debug.config(state=tk.DISABLED)
        self.frame_debug.pack_forget()
        print("CLOSE DEBUG")
        self.frame_right.pack(side=tk.RIGHT, fill=None, expand=False, padx=(1, 0))

    def update(self):
        if self.update_video:
            ret, frame = self.video.get_frame()
            if ret:
                # .transpose(Image.FLIP_LEFT_RIGHT) to flip the image
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame).resize(image_size, Image.ANTIALIAS))
                self.canvas_video.create_image(res_width/4, res_width/4, image=self.photo, anchor=tk.CENTER)
        self.window.after(self.delay, self.update)

    def reset_pokemon(self):
        print("RESET POKÉMON DETAILS")
        self.loaded_pokemon = None
        img_size = (int(res_width / 7.385), int(res_width / 7.385))
        self.thumbnail = ImageTk.PhotoImage(Image.open(thumbnails_path + "0.png").resize(img_size, Image.ANTIALIAS))
        self.label_thumb.configure(image=self.thumbnail)
        self.entry_name_text.set("")
        self.entry_id_text.set("")
        img_size = (int(res_width / 9.38), int(res_height / 14.28))
        self.image_type1 = ImageTk.PhotoImage(Image.open(types_path + "Empty_en.png").resize(img_size, Image.ANTIALIAS))
        self.canvas_types.itemconfig(self.canvas_image_type1, image=self.image_type1)
        self.image_type2 = ImageTk.PhotoImage(Image.open(types_path + "Empty_en.png").resize(img_size, Image.ANTIALIAS))
        self.canvas_types.itemconfig(self.canvas_image_type2, image=self.image_type2)
        self.text_description.config(state="normal")
        self.text_description.delete('1.0', tk.END)
        self.text_description.config(state="disabled")
        self.entry_hp_text.set("")
        self.canvas_hp.coords(self.rect_hp, x1, y1, int(res_width/96), y2)
        self.canvas_hp.itemconfig(self.rect_hp, fill=self.get_stat_color(0))
        self.entry_attack_text.set("")
        self.canvas_attack.coords(self.rect_hp, x1, y1, int(res_width/96), y2)
        self.canvas_attack.itemconfig(self.rect_attack, fill=self.get_stat_color(0))
        self.entry_defense_text.set("")
        self.canvas_defense.coords(self.rect_hp, x1, y1, int(res_width/96), y2)
        self.canvas_defense.itemconfig(self.rect_defense, fill=self.get_stat_color(0))
        self.entry_sp_atk_text.set("")
        self.canvas_sp_atk.coords(self.rect_hp, x1, y1, int(res_width/96), y2)
        self.canvas_sp_atk.itemconfig(self.rect_sp_atk, fill=self.get_stat_color(0))
        self.entry_sp_def_text.set("")
        self.canvas_sp_def.coords(self.rect_hp, x1, y1, int(res_width/96), y2)
        self.canvas_sp_def.itemconfig(self.rect_sp_def, fill=self.get_stat_color(0))
        self.entry_speed_text.set("")
        self.canvas_speed.coords(self.rect_hp, x1, y1, int(res_width/96), y2)
        self.canvas_speed.itemconfig(self.rect_speed, fill=self.get_stat_color(0))
        self.image_evo_to = ImageTk.PhotoImage(Image.open(sprites_path + "0.png").resize(sprite_size, Image.ANTIALIAS))
        self.label_evo_to.configure(image=self.image_evo_to)
        self.image_evo_from = ImageTk.PhotoImage(Image.open(sprites_path + "0.png").resize(sprite_size, Image.ANTIALIAS))
        self.label_evo_from.configure(image=self.image_evo_from)
        self.entry_prediction_text.set("")

    def search(self):
        ret, frame = self.video.get_frame()
        if ret:
            cv2.imwrite("frame.jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            frame = rectify_image(frame)
            cv2.imwrite("frame_undistorted.jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            # if debug mode is enabled write first N (= settings.debug_mode) predictions
            if self.settings.debug_mode != 0:
                result = pc.predict_top_n_pokemon("frame_undistorted.jpg", self.settings.debug_mode)
                result_str = ""
                for i in range(0, self.settings.debug_mode):
                    result_str += str(i+1) + "> " + str(result[0][i]) + "\t"
                    if len(str(result[0][i])) < 9:
                        result_str += "\t"
                    else:
                        result_str += " \t"
                    result_str += str(result[1][i])[:6] + "\n"
                result_str += labels["time"][self.settings.language] + time.strftime("%H:%M:%S") + "\n\n"
                self.text_debug.config(state="normal")
                self.text_debug.insert(tk.END, result_str)
                self.text_debug.see(tk.END)
                self.text_debug.config(state="disabled")
                print(result_str)
                return
            # if not in debug mode
            (pkmn, confidence) = pc.predict_top_n_pokemon("frame_undistorted.jpg", 1)
            pkmn = str(pkmn)[2:-2]
            confidence = str(confidence)[1:-1]
            # self.entry_prediction_text.set(pkmn + ": " + confidence)
            self.load_pokemon(pkmn)
    
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
            if self.settings.descr_voice:
                self.play_description()
        except KeyError:
            self.loaded_pokemon = None
            print("Pokémon not found.")

    # update image
    def load_image(self):
        path_image = thumbnails_path + str(self.loaded_pokemon.num) + ".png"
        img_size = (int(res_width / 7.385), int(res_width / 7.385))
        image = Image.open(path_image).resize(img_size, Image.ANTIALIAS)
        self.thumbnail = ImageTk.PhotoImage(image)
        self.label_thumb.configure(image=self.thumbnail)

    # update name
    def load_name(self):
        print("Name: " + self.loaded_pokemon.name)
        self.entry_name_text.set(self.loaded_pokemon.name)

    # update ID
    def load_id(self):
        print("ID: " + str(self.loaded_pokemon.num))
        self.entry_id_text.set(str(self.loaded_pokemon.num))

    # update type(s)
    def load_types(self):
        types = self.loaded_pokemon.types[0]
        path_image = types_path + self.loaded_pokemon.types[0] + "_" + self.settings.language + ".png"
        img_size = (int(res_width/9.38), int(res_height/14.28))
        image = Image.open(path_image).resize(img_size, Image.ANTIALIAS)
        self.image_type1 = ImageTk.PhotoImage(image)
        self.canvas_types.itemconfig(self.canvas_image_type1, image=self.image_type1)
        if len(self.loaded_pokemon.types) == 2:
            types += ", " + self.loaded_pokemon.types[1]
            path_image = types_path + self.loaded_pokemon.types[1] + "_" + self.settings.language + ".png"
            image = Image.open(path_image).resize(img_size, Image.ANTIALIAS)
            self.image_type2 = ImageTk.PhotoImage(image)
            self.canvas_types.itemconfig(self.canvas_image_type2, image=self.image_type2)
        else:
            path_image = types_path + "Empty_en.png"
            image = Image.open(path_image).resize(img_size, Image.ANTIALIAS)
            self.image_type2 = ImageTk.PhotoImage(image)
            self.canvas_types.itemconfig(self.canvas_image_type2, image=self.image_type2)
        # self.entry_types_text.set(types)
        print("Type(s): " + types)

    # update description
    def load_description(self):
        print("Description: " + self.loaded_pokemon.description[self.settings.language])
        self.text_description.config(state="normal")
        self.text_description.delete('1.0', tk.END)
        self.text_description.insert('1.0', self.loaded_pokemon.description[self.settings.language])
        self.text_description.config(state="disabled")

    # update stats
    def load_stats(self):
        print("Stats:")
        s_hp = self.loaded_pokemon.stats["HP"]
        self.entry_hp_text.set(s_hp)
        self.canvas_hp.coords(self.rect_hp, x1, y1, s_hp / 2, y2)
        self.canvas_hp.itemconfig(self.rect_hp, fill=self.get_stat_color(s_hp))
        s_atk = self.loaded_pokemon.stats["Attack"]
        self.entry_attack_text.set(s_atk)
        self.canvas_attack.coords(self.rect_hp, x1, y1, s_atk / 2, y2)
        self.canvas_attack.itemconfig(self.rect_attack, fill=self.get_stat_color(s_atk))
        s_def = self.loaded_pokemon.stats["Defense"]
        self.entry_defense_text.set(s_def)
        self.canvas_defense.coords(self.rect_hp, x1, y1, s_def / 2, y2)
        self.canvas_defense.itemconfig(self.rect_defense, fill=self.get_stat_color(s_def))
        s_sp_atk = self.loaded_pokemon.stats["Sp. Attack"]
        self.entry_sp_atk_text.set(s_sp_atk)
        self.canvas_sp_atk.coords(self.rect_hp, x1, y1, s_sp_atk / 2, y2)
        self.canvas_sp_atk.itemconfig(self.rect_sp_atk, fill=self.get_stat_color(s_sp_atk))
        s_sp_def = self.loaded_pokemon.stats["Sp. Defense"]
        self.entry_sp_def_text.set(s_sp_def)
        self.canvas_sp_def.coords(self.rect_hp, x1, y1, s_sp_def / 2, y2)
        self.canvas_sp_def.itemconfig(self.rect_sp_def, fill=self.get_stat_color(s_sp_def))
        s_speed = self.loaded_pokemon.stats["Speed"]
        self.entry_speed_text.set(s_speed)
        self.canvas_speed.coords(self.rect_hp, x1, y1, s_speed / 2, y2)
        self.canvas_speed.itemconfig(self.rect_speed, fill=self.get_stat_color(s_speed))
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
        self.image_evo_from = ImageTk.PhotoImage(Image.open(path_image).resize(sprite_size, Image.ANTIALIAS))
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
                self.image_evo_to = ImageTk.PhotoImage(Image.open(path_image).resize(sprite_size, Image.ANTIALIAS))
                self.label_evo_to.configure(image=self.image_evo_to)
                return
        else:
            path_image = sprites_path + "0.png"
        self.image_evo_to = ImageTk.PhotoImage(Image.open(path_image).resize(sprite_size, Image.ANTIALIAS))
        self.label_evo_to.configure(image=self.image_evo_to)

    # show previous "to" evolution (e.g. Eevee multiple evolutions)
    def show_prev_evo_to(self):
        self.evo_to_i -= 1
        evo_to = self.pokemon_repo.pokemon[self.loaded_pokemon.name].evolutions["to"]
        print("Show previous evolution: " + str(evo_to[self.evo_to_i]))
        self.image_evo_to = ImageTk.PhotoImage(Image.open(sprites_path + str(evo_to[self.evo_to_i]) + ".png").resize(sprite_size, Image.ANTIALIAS))
        self.label_evo_to.configure(image=self.image_evo_to)
        self.button_evo_to_next.config(state=tk.NORMAL)
        if self.evo_to_i == 0:
            self.button_evo_to_prev.config(state=tk.DISABLED)

    # show next "to" evolution (e.g. Eevee multiple evolutions)
    def next_evo_to(self):
        self.evo_to_i += 1
        evo_to = self.pokemon_repo.pokemon[self.loaded_pokemon.name].evolutions["to"]
        print("Show next evolution: " + str(evo_to[self.evo_to_i]))
        self.image_evo_to = ImageTk.PhotoImage(Image.open(sprites_path + str(evo_to[self.evo_to_i]) + ".png").resize(sprite_size, Image.ANTIALIAS))
        self.label_evo_to.configure(image=self.image_evo_to)
        self.button_evo_to_prev.config(state=tk.NORMAL)
        if self.evo_to_i + 1 == len(evo_to):
            self.button_evo_to_next.config(state=tk.DISABLED)

    # update cry
    def load_cry(self):
        self.cry = pygame.mixer.Sound(cries_path + str(self.loaded_pokemon.num) + ".ogg")

    def play_cry(self):
        if self.loaded_pokemon:
            print("PLAY CRY\nPokémon #" + str(self.loaded_pokemon.num) + " Volume: " + str(self.mono_channel.get_volume()))
            self.mono_channel.play(self.cry)
        else:
            print("No pokémon has been loaded")

    def play_description(self):
        if self.loaded_pokemon:
            print("READ DESCRIPTION\nPokémon #" + str(self.loaded_pokemon.num) + " Volume: " + str(self.mono_channel.get_volume()))
            self.mono_channel.play(pygame.mixer.Sound("resources/descriptions_" + self.settings.language + "/" + str(self.loaded_pokemon.num) + ".mp3"))
        else:
            print("No pokémon has been loaded")

    def show_settings(self):
        self.mono_channel.stop()
        self.button_search.config(state=tk.DISABLED)
        # self.button_screenshot.config(state=tk.DISABLED)
        self.combobox_language.selection_clear()
        self.scale_volume.set(self.settings.volume * 100)
        self.frame_right.pack_forget()
        print("SHOW SETTINGS")
        self.frame_settings.pack(side=tk.RIGHT)

    def close_settings(self):
        self.settings.debug_mode = 0
        self.button_debug.config(state=tk.NORMAL)
        self.button_search.config(state=tk.NORMAL)
        for lang in labels["languages"].keys():
            if lang == self.settings.language:
                self.combobox_language_text.set(lang)
        if self.window.attributes("-fullscreen") == 1:
            self.check_fullscreen.select()
            self.settings.fullscreen.set(True)
        else:
            self.check_fullscreen.deselect()
            self.settings.fullscreen.set(False)
        self.var_descr_voice.set(self.settings.descr_voice)
        self.mono_channel.set_volume(self.settings.volume)
        self.frame_settings.pack_forget()
        self.frame_right.pack(side=tk.RIGHT, fill=None, expand=False)
        print("CLOSE SETTINGS\nFullscreen: " + str(bool(self.settings.fullscreen.get())) + "\nVolume: " + str(self.settings.volume))

    def update_language(self):
        self.text_start.set(labels["start"][self.settings.language])
        self.text_quit.set(labels["quit"][self.settings.language])
        self.text_info_description.config(state="normal")
        self.text_info_description.delete('1.0', tk.END)
        self.text_info_description.insert('1.0', labels["info"][self.settings.language], 'tag-center')
        self.text_info_description.config(state="disabled")
        self.text_search.set(labels["search"][self.settings.language])
        self.text_screenshot.set(labels["screenshot"][self.settings.language])
        self.text_cry.set(labels["cry"][self.settings.language])
        self.text_name.set(labels["name"][self.settings.language])
        self.text_types.set(labels["types"][self.settings.language])
        self.text_hp.set(labels["hp"][self.settings.language])
        self.text_atk.set(labels["attack"][self.settings.language])
        self.text_def.set(labels["defense"][self.settings.language])
        self.text_spatk.set(labels["sp. atk"][self.settings.language])
        self.text_spdef.set(labels["sp. def"][self.settings.language])
        self.text_speed.set(labels["speed"][self.settings.language])
        self.text_settings.set(labels["settings"][self.settings.language])
        self.text_language.set(labels["language"][self.settings.language])
        self.text_fullscreen.set(labels["full screen"][self.settings.language])
        self.text_descr_voice.set(labels["descr voice"][self.settings.language])
        self.text_flip.set(labels["flip image"][self.settings.language])
        self.text_volume.set(labels["volume"][self.settings.language])
        self.text_save.set(labels["save"][self.settings.language])
        self.text_cancel.set(labels["cancel"][self.settings.language])
        if self.loaded_pokemon:
            self.load_types()
            self.load_description()

    def save_settings(self):
        self.button_search.config(state=tk.NORMAL)
        self.settings.language = labels["languages"][self.combobox_language_text.get()]
        self.settings.save_settings(self.combobox_language_text.get(), self.settings.fullscreen.get(), 1, self.var_descr_voice.get(), 0, self.scale_volume.get() / 100)
        self.window.attributes("-fullscreen", self.settings.fullscreen.get())
        self.update_language()
        self.mono_channel.set_volume(self.settings.volume)
        self.frame_settings.pack_forget()
        self.button_debug.config(state=tk.NORMAL)
        if 2 <= self.settings.debug_mode <= 10:
            self.reset_pokemon()
            self.show_debug_mode()
        else:
            self.frame_right.pack(side=tk.RIGHT, fill=None, expand=False)
        print("SAVE SETTINGS\nLanguage: " + self.settings.language + "\nFullscreen: " + str(bool(self.settings.fullscreen.get())) + "\nVolume: " + str(self.settings.volume))

    def debug_counter(self):
        if self.settings.debug_mode == 9:
            self.button_debug.config(state=tk.DISABLED)
        self.settings.debug_mode += 1

    # get RGB color from stat
    def get_stat_color(self, stat):
        if 0 <= stat < int(res_width/19.2):     # 25
            return "#ff0000"
        elif 25 <= stat < int(res_width/9.6):   # 50
            return "#ff5500"
        elif 50 <= stat < int(res_width/6.4):   # 75
            return "#ffaa00"
        elif 75 <= stat < int(res_width/4.8):   # 100
            return "#ffff00"
        elif 100 <= stat < int(res_width/3.84): # 125
            return "#7fff00"
        elif 125 <= stat < int(res_width/3.2):  # 150
            return "#00ff00"
        elif 150 <= stat < int(res_width/2.4):  # 200
            return "#00ff80"
        return "#00ffff"

    def get_type_color(self, type: str):
        if type.lower() == "fire":
            return "#ff0000"

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


# Poké-Pi-Dex App
if __name__ == "__main__":
    app = App(tk.Tk(), "pokédex")
    app.start()