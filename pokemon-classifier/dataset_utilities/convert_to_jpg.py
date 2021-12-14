from pathlib import Path
import subprocess

cartella = Path('/home/user/PokemonData/')

for file in cartella.rglob("*"):
    if file.is_file():
        bello = subprocess.check_output(f"file {file}",shell=True)
        bello = str(bello).split(":")[1].split(",")[0].lower()
        if "jpeg" not in bello:
            print(file)
            subprocess.check_output(f'magick convert "{str(file)}" "{str(file)}"', shell=True)
            
