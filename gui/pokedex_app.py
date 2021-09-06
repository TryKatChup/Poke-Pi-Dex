import tkinter as tk
from PIL import ImageTk, Image
from pokemon_repository import PokemonRepository

class App:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        self.window.geometry("480x320")
        self.pokemon_repo = PokemonRepository("utilities/first_gen_pokedex.json")

        '''self.frame_left = tk.Frame()
        self.frame_left.pack(side=tk.LEFT)
        self.frame_right = tk.Frame(side=tk.RIGHT)'''

        image = Image.open("utilities/thumbnails/0.png").resize((50, 50), Image.ANTIALIAS)
        self.thumbnail = ImageTk.PhotoImage(image)
        self.label_image = tk.Label(image=self.thumbnail, width=50, height=50)
        self.label_image.pack(side="top", fill="both")

        self.frame_name = tk.Frame()
        self.frame_name.pack()
        self.label_name = tk.Label(master=self.frame_name, text="Name: ")
        self.entry_name_text = tk.StringVar()
        self.entry_name = tk.Entry(master=self.frame_name, textvariable=self.entry_name_text)
        self.entry_name.config(state="readonly")
        self.label_name.pack(side=tk.LEFT)
        self.entry_name.pack(side=tk.LEFT)

        self.frame_id_types = tk.Frame()
        self.frame_id_types.pack()
        self.label_id = tk.Label(master=self.frame_id_types, text="ID: ")
        self.entry_id = tk.Entry(master=self.frame_id_types, width=3)
        self.button_id = tk.Button(master=self.frame_id_types, text="Search", command=lambda: self.load_pokemon(self.entry_id.get()))
        self.label_id.pack(side=tk.LEFT)
        self.entry_id.pack(side=tk.LEFT)
        self.button_id.pack(side=tk.LEFT)

        self.label_types = tk.Label(master=self.frame_id_types, text="Type(s): ")
        self.entry_types_text = tk.StringVar()
        self.entry_types = tk.Entry(master=self.frame_id_types, textvariable=self.entry_types_text)
        self.entry_types.config(state="readonly")
        self.label_types.pack(side=tk.LEFT)
        self.entry_types.pack(side=tk.LEFT)

        '''self.frame_evolutions = tk.Frame()
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

        self.label_description = tk.Label(text="Description: ")
        self.text_description = tk.Text()
        self.text_description.config(state="disabled")
        self.label_description.pack()
        self.text_description.pack()

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
            print("The id must be an integer between 1 and 151 inclusive")
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
            #self.load_evolutions(pokemon)
            self.load_cry(pokemon)

    # update image
    def load_image(self, pkmn):
        path_image = "utilities/thumbnails/" + str(pkmn.num) + ".png"
        image = Image.open(path_image).resize((50, 50), Image.ANTIALIAS)
        self.thumbnail = ImageTk.PhotoImage(image)
        self.label_image.configure(image=self.thumbnail)

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

    # update evolutions
    '''def load_evolutions(self, pkmn):
        self.entry_evolutions_from_text.set("")
        self.entry_evolutions_to_text.set("")
        evo_from = pkmn.evolutions["from"]
        if evo_from is not None:
            self.entry_evolutions_from_text.set(self.pokemon_repo.pokemon[evo_from].name)
        evo_to = pkmn.evolutions["to"]
        if evo_to is not None:
            self.entry_evolutions_to_text.set(self.pokemon_repo.pokemon[evo_to].name)'''

    # update cry
    def load_cry(self, pkmn):
        print("load cry")


app = App(tk.Tk(), "pokedex")
app.run()