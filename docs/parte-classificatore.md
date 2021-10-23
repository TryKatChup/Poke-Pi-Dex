# Classificazione di immagini

L'obiettivo del _Pokédex_ è di riconoscere i _Pokémon_ e fornire le loro descrizioni e statistiche.
Per questo scopo è stato implementato un classificatore di immagini.

## Specifiche del classificatore finale

Rete con Keras con architettura standard.

Per il dataset abbiamo scaricato da kaggle delle foto opportunamente tagliate e tutte con lo stesso aspect ratio.

Ciacun pokemon è rappresentato da una cartella, contenente le immagini prese dalle carte, dal cartone, da fanart, peluche, giochi. 

Alla fine abbiamo preso ciascuna cartella contenente le immagini di uno specifico pokemon e preso da ciascuna le immagini per training set, val set e test set, in proporzione 80/10/10

- Rete convoluzionale con MaxPooling, ReLU, batchNorm 
- Parte di classificazione con livelli Densi full connected

Per ovviare ai pochi sample:

- rotazioni e flip randomici
- regularization usando drop-out nel classificatore, un livello in più che previene overfitting
La tecnica di dropout consiste nell'ignorare casualmente alcuni set di neuroni
Li ho usati perché la rete overfittava dopo poche epoche, senza miglioramenti particolari di accuracy


3 livelli convoluzionali, 2 densi, 2048 neuroni, 150 classi

early stopping di Keras per capire quante epoche ci volessero per ottenere il modello ottimale

Risultati ottenuti:

Oltre il 90% (ben ~ 99.7%) di accuracy sul validation set 



## Tentativi non andati a buon fine

Fully connected classifier vs global average pooling

- quest'ultima è andata male (media su ogni canale, 256 x 1). Perché? BOH
- Con il flatten avevamo 50176 x 1 (28x28x64)
- sempre flatten: ~103 milioni di parametri nel primo fully connected layer, nel secondo layer erano ~ 307 mila
- Inizialmente ho provato con 1024 neuroni, ma erano pochi e le performance erano peggiori.
- ELU vs ReLU, andava peggio ELU
- 5 livelli convoluzionali, ma andava male. Forse è perché abbiamo troppi pochi dati, quindi la complessità della rete deve essere minima.
