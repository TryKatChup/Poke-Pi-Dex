import json
import tkinter as tk

languages = {'en', 'it'}


class Settings:
    def __init__(self, window, filename):
        self.filename = filename

        self.debug_mode = 0
        self.language = 'en'
        self.fullscreen = tk.IntVar(value=1)
        self.touch_controls = tk.IntVar(value=1)
        self.descr_voice = 1
        self.flip_image = tk.IntVar(value=0)
        self.volume = 0.5
        # load from file
        self.load_from_file()

    def reset_settings(self):
        result = {
            "language": self.language,
            "fullscreen": self.fullscreen.get(),
            "touch_controls": self.touch_controls.get(),
            "descr_voice": self.descr_voice,
            "flip_image": self.flip_image.get(),
            "volume": self.volume
        }
        return result

    def load_from_file(self):
        in_settings = {}
        try:
            in_file = open(self.filename, "r", encoding="utf-8")
            in_settings = json.load(in_file)
            if languages.__contains__(in_settings["language"]):
                self.language = in_settings["language"]
            if in_settings["fullscreen"] in range(0, 1):
                self.fullscreen.set(in_settings["fullscreen"])
            if in_settings["touch_controls"] == 0 or in_settings["touch_controls"] == 1:
                self.touch_controls.set(in_settings["touch_controls"])
            if in_settings["descr_voice"] == 0 or in_settings["descr_voice"] == 1:
                self.descr_voice = in_settings["descr_voice"]
            if in_settings["flip_image"] == 0 or in_settings["flip_image"] == 1:
                self.flip_image.set(in_settings["flip_image"])
            if 0.0 <= in_settings["volume"] <= 1.0:
                self.volume = in_settings["volume"]
            in_file.close()
        except TypeError or KeyError:
            with open(self.filename, "w", encoding="utf-8") as out_file:
                json.dump(self.reset_settings(), out_file, indent=2, ensure_ascii=False)
                out_file.close()
        except json.JSONDecodeError:
            with open(self.filename, "w", encoding="utf-8") as out_file:
                json.dump(self.reset_settings(), out_file, indent=2, ensure_ascii=False)
                out_file.close()
        except FileNotFoundError:
            with open(self.filename, "x", encoding="utf-8") as out_file:
                json.dump(self.reset_settings(), out_file, indent=2, ensure_ascii=False)
                out_file.close()

    def save_settings(self, language, fullscreen, touch_controls, descr_voice, flip_image, volume):
        try:
            if languages.__contains__(language):
                self.language = language
            if fullscreen == 0 or fullscreen == 1:
                self.fullscreen.set(fullscreen)
            if touch_controls == 0 or touch_controls == 1:
                self.touch_controls.set(touch_controls)
            if descr_voice == 0 or descr_voice == 1:
                self.descr_voice = descr_voice
            if flip_image == 0 or flip_image == 1:
                self.flip_image.set(flip_image)
            if 0.0 <= volume <= 100.0:
                self.volume = volume
        except TypeError:
            return -1
        # save on file
        out_settings = {
            "language": self.language,
            "fullscreen": self.fullscreen.get(),
            "touch_controls": self.touch_controls.get(),
            "descr_voice": self.descr_voice,
            "flip_image": self.flip_image.get(),
            "volume": self.volume
        }

        with open(self.filename, "w", encoding="utf-8") as out_file:
            json.dump(out_settings, out_file, indent=2, ensure_ascii=False)
            out_file.close()

'''
# Test
tmp = Settings(tk.Tk())
tmp.load_from_file()

#print(tmp.save_settings("en", 1, 0, 0, 1, 0))
print(tmp.language + ", " + str(tmp.fullscreen.get()) + ", " + str(tmp.touch_controls.get()) + ", " + str(tmp.descr_voice) + ", " + str(tmp.flip_image.get()) + ", " + str(tmp.volume))
'''
