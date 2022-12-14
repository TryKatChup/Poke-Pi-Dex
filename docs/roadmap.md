Kary:

- [ ] Fare una funzione in più sul repo che faccia andare la rete nuova dell'attività progettuale
- [ ] Committare i file che ho usato per il dataset (script bash per cambiare numero di immagini per classe e python per i conversione in .jpg)
- [x] Migliorare la mini rete vecchia (v3: più immagini, rispetto alle 50 per classe) (fatto con 55 immagini per classe)

- [x] ottimizzazione rete (quantizzazione + prova immagine con tf.lite)
**Data Augmentation (usare API STATELESS tf.keras):**
- [x] Random flip
- [x] Random rotation
- [x] ~~Random brightness~~ (in keras it has strange artifacts, so it should not be used)
- [x] Random contrast   
- [x] riallenare rete con foto tagliate + regolazione luminosità


Miky
- [x] fixare spazio tra i due frame nella gui
- [x] aggiungere pulsante per tornare al menu principale al posto di info
- [x] aggiungere controllo per non far aggiornare il video quando si è nel menù (o non aprire nemmeno la camera)
- [x] reset pokémon (servirà quando non viene riconosciuto un pokémon per più di qualche secondo(?))
- [x] aggiungere colori diversi o immagini per i vari tipi
- [x] scelta della lingua
- [x] aggiungere descrizioni in lingua differente (IT)
- [x] registrare per ciascuna descrizione in Inglese la traccia audio letta da un bot (https://www.youtube.com/watch?v=rjlOJjX-6Ug) Bot: [Text To Speech Online](http://texttospeechrobot.com/) + [PKMN DB](https://pokemondb.net/pokedex/blastoise), [Pronunciation](https://www.dailydot.com/parsec/pokemon-name-pronunciation-guide/)
- [x] opzione nelle impostazioni per abilitare la lettura automatica della descrizione del pokémon quando viene riconosciuto
- [x] impostazioni persistenti
- [x] usare bottoni
- [ ] usare analogico
- [x] debug mode (piccolo terminale di output se si fa una sequenza di tasti o se si avvia l'app con il parametro -d)
- [ ] opzione per attivare/disattivare input tramite bottoni+analogico (NB: quando usiamo il touch è meglio nascondere il puntatore del mouse)
- [ ] aumentare volume di tutti gli mp3 delle descrizioni
- [ ] finire doc progetto e aggiungere parti nella relazione
- [ ] aggiungere sezione con ringraziamenti e crediti
- [ ] provare a realizzare un OPAMP con Fede
- [ ] bottoncino play/stop nella descrizione per riprodurre la voce che legge la descrizione
- [ ] modello case 3D
- [ ] implementare toggle per flip immagine
- [ ] refactor stats: usare un unico canvas
- [ ] extra con piccole sprite che girano per lo schermo tipo i quadrati
- [ ] easter egg per Umbreon

Entrambi:
- [x] ritagliare foto pokémon (Kary dispari, Miky pari) e aggiungerne di nuove
  - [dataset](https://liveunibo-my.sharepoint.com/personal/karina_chichifoi_studio_unibo_it/_layouts/15/onedrive.aspx?isAscending=false&id=%2Fpersonal%2Fkarina%5Fchichifoi%5Fstudio%5Funibo%5Fit%2FDocuments%2FPok%C3%A9dex%2Fdataset&sortField=Modified) (NB: *Old* sono quelle vecchie già presenti nel dataset, ma che sono state controllate e sistemate; *New* sono quelle nuove scaricate, sistemate e aggiunte)
  - per le immagini nuove cercare: <nome_pokémon> fanart, drawings, anime, 3d model, plush, action figure, carte ([sito utile](https://pkmncards.com/card))
- [ ] rettificazione picamera

<!-- Mi raccomando aggiornare il numero di pokémon rimasti 🥝-->
Pokémon tagliati:

- [x] Bulbasaur
- [x] Ivysaur
- [x] Venusaur
- [x] Charmander
- [x] Charmeleon
- [x] Charizard
- [x] Squirtle
- [x] Wartortle
- [x] Blastoise
- [x] Caterpie
- [x] Metapod
- [x] Butterfree
- [x] Weedle
- [x] Kakuna
- [x] Beedrill
- [x] Pidgey
- [x] Pidgeotto
- [x] Pidgeot
- [x] Rattata
- [x] Raticate
- [x] Spearow
- [x] Fearow
- [x] Ekans
- [x] Arbok
- [x] Pikachu
- [x] Raichu
- [x] Sandshrew
- [x] Sandslash
- [x] Nidoran♀
- [x] Nidorina
- [x] Nidoqueen
- [x] Nidoran♂
- [x] Nidorino
- [x] Nidoking
- [x] Clefairy
- [x] Clefable
- [x] Vulpix
- [x] Ninetales
- [x] Jigglypuff
- [x] Wigglytuff
- [x] Zubat
- [x] Golbat
- [x] Oddish
- [x] Gloom
- [x] Vileplume
- [x] Paras
- [x] Parasect
- [x] Venonat
- [x] Venomoth
- [x] Diglett
- [x] Dugtrio
- [x] Meowth
- [x] Persian
- [x] Psyduck
- [x] Golduck
- [x] Mankey
- [x] Primeape
- [x] Growlithe
- [x] Arcanine
- [x] Poliwag
- [x] Poliwhirl
- [x] Poliwrath
- [x] Abra
- [x] Kadabra
- [x] Alakazam
- [x] Machop
- [x] Machoke
- [x] Machamp
- [x] Bellsprout
- [x] Weepinbell
- [x] Victreebel
- [x] Tentacool
- [x] Tentacruel
- [x] Geodude
- [x] Graveler
- [x] Golem
- [x] Ponyta
- [x] Rapidash
- [x] Slowpoke
- [x] Slowbro
- [x] Magnemite
- [x] Magneton
- [x] Farfetch’d
- [x] Doduo
- [x] Dodrio
- [x] Seel
- [x] Dewgong
- [x] Grimer
- [x] Muk
- [x] Shellder
- [x] Cloyster
- [x] Gastly
- [x] Haunter
- [x] Gengar
- [x] Onix
- [x] Drowzee
- [x] Hypno
- [x] Krabby
- [x] Kingler
- [x] Voltorb
- [x] Electrode
- [x] Exeggcute
- [x] Exeggutor
- [x] Cubone
- [x] Marowak
- [x] Hitmonlee
- [x] Hitmonchan
- [x] Lickitung
- [x] Koffing
- [x] Weezing
- [x] Rhyhorn
- [x] Rhydon
- [x] Chansey
- [x] Tangela
- [x] Kangaskhan
- [x] Horsea
- [x] Seadra
- [x] Goldeen
- [x] Seaking
- [x] Staryu
- [x] Starmie
- [x] Mr. Mime
- [x] Scyther
- [x] Jynx
- [x] Electabuzz
- [x] Magmar
- [x] Pinsir
- [x] Tauros
- [x] Magikarp
- [x] Gyarados
- [x] Lapras
- [x] Ditto
- [x] Eevee
- [x] Vaporeon
- [x] Jolteon
- [x] Flareon
- [x] Porygon
- [x] Omanyte
- [x] Omastar
- [x] Kabuto
- [x] Kabutops
- [x] Aerodactyl
- [x] Snorlax
- [x] Articuno
- [x] Zapdos
- [x] Moltres
- [x] Dratini
- [x] Dragonair
- [x] Dragonite
- [x] Mewtwo
- [x] Mew

NO

Modelli: tabella riassuntiva

| Modello | Train Loss  | Val Loss  | Test Loss  | Train accuracy  | Val accuracy  | Test accuracy  | Tempo di Training | Dimensione |
|---|---|---|---|---|---|---|---|---|
| Resnet152   | 0.2914  | 0.1288  | 0.107  | 93.54  | 96.72  | 97.171  | 38' 38"  | 223.9 MB  |
| MobileNetV2  | 0.5433  | 0.2815  | 0.224  | 87%  | 93.52%  | 94.509 %  | 7' 53"  | non ricordo |
| MobileNetV3 large  | 0.6595  | 0.3366  | 0.299  | 82.83%  | 91.75%  | 91.015%  | 6' 55"  | ci guardo  |
