<div align="center">
  
  [![made-with-python][made-with-phyton-shield]][made-with-phyton-url]
  [![made-with-Markdown][made-with-markdown-shield]][made-with-markdown-url]
  [![Open Source Love png1][open-source-shield]][open-source-url]
  [![GPLv3 license][license-shield]][license-url]
  [![Raspberry Pi][raspberry-shield]][raspberry-url]
  [![Keras][keras-shield]][keras-url]
  [![TensorFlow][tensorflow-shield]][tensorflow-url]
  [![Open CV][opencv-shield]][opencv-url]
  [![nVIDIA][nvidia-shield]][nvidia-url]
  <br/>
  [![Open In Collab][open-collab-shield]][open-collab-url]
  [![Downloads][downloads-shield]][downloads-url]
  [![Contributors][contributors-shield]][contributors-url]
  [![Forks][forks-shield]][forks-url]
  [![Stargazers][stars-shield]][stars-url]
  [![Issues][issues-shield]][issues-url]
  
  <img src="https://github.com/TryKatChup/Poke-Pi-Dex/blob/main/gfx/logo.png"/>
  
  <h1> Poké-Pi-Dex</h1>
  
  Progetto basato su Deep Learning per Computer Vision per poké weeb nostalgici, creato da <a href="https://github.com/TryKatChup">Karina Chichifoi</a> e <a href="https://github.com/mikyll">Michele Righi</a>.<br/>
  Abbiamo ricreato il clone di un Pokédex, che riconosce immagini di Pokémon della prima generazione, sfruttando una Rete Neurale Convoluzionale. È stato sviluppato per eseguire su un Raspberry Pi4 con display LCD, PiCamera ed altri componenti collegati. Il case è fatto di cartoncino riciclato. 🌱
<br/><br/>
  <a href="https://github.com/TryKatChup/Poke-Pi-Dex/blob/main/README.md#-poké-pi-dex">English</a>
  ·
  <a href="">Documentazione</a>
  ·
  <a href="https://github.com/TryKatChup/Poke-Pi-Dex/blob/main/Relazione.pdf">Relazione</a>
  ·
  <a href="https://github.com/TryKatChup/Poke-Pi-Dex/blob/main/docs/Presentation/Poké-Pi-Dex_IT.pdf">Presentazione</a>
  ·
  <a href="https://github.com/mikyll/UnityDOTS-Thesis/issues">Richiedi una Feature|Segnala un Bug</a>
<br/><br/>
<img src="https://github.com/TryKatChup/Poke-Pi-Dex/blob/main/gfx/aaaaaaaaa.png"/>
</div>

<details open="open">
  <summary><h2 style="display: inline-block">Indice</h2></summary>
  <ol>
    <li><a href="#demo">Demo</a></li>
    <li><a href="#funzionalità">Funzionalità</a></li>
    <li><a href="#panoramica-completa">Panoramica Completa</a></li>
    <li><a href="#utilizzo">Utilizzo</a>
      <ul>
        <li><a href="#prerequisiti">Prerequisiti</a></li>
        <li><a href="#installazione">Installazione</a></li>
      </ul>
    </li>
    <li><a href="#strumenti">Strumenti</a></li>
    <li><a href="#risorse">Risorse</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#licenza">Licenza</a></li>
    <li><a href="#contatti">Contatti</a></li>
    <!-- <li><a href="#ringraziamenti">Ringraziamenti</a></li>
    <li><a href="#meme">Memotty</a></li> -->
  </ol>
</details>

## Demo
See our demo on YouTube! https://www.youtube.com/watch?v=6A07DGlRxg4 <!-- TO-DO -->

<div align="center">
  <img src="https://github.com/TryKatChup/Poke-Pi-Dex/blob/main/gfx/demo.png" width=50%/>
</div>

## Funzionalità
TODO

## Panoramica Completa
Check link a roba scritta da Kary

## Utilizzo
To use the application follow these steps:

### Prerequisiti
- conda
TO-DO
<!-- - OS:
- Python version
- Python packages
  - for Raspberry usage: -->

### Installazione
#### Windows
1. Scarica l'[ultima versione](https://github.com/TryKatChup/Poke-Pi-Dex/releases/latest)
2. Estrai lo zip
3. Crea il virtual environment:
  ```bash
  conda env create -f environment.yml
  ```
4. Esegui l'applicazione:
  ```bash
  python poke-pi-dex.py
  ```

<!-- - clone the repo or download the latest release -->

## Roadmap
- [x] Dataset
  - [x] trovare un dataset adatto per la rete neurale
  - [x] sistemarlo (ritagliare le immagini) ed estenderlo
- [x] Classificatore
  - [x] CNN con 3 layer convoluzionali e 2 layer FC
  - [x] data augmentation (specchiamento, rotazione, contrasto e ~~luminosità~~ randomici)
  - [x] provare dropout
  - [x] provare batch norm
  - [x] grafici loss e accuracy
  - [x] test con immagini reali
  - [x] miglirare la vecchia CNN
- [x] Applicazione
  - [x] Repository Pokémon
    - [x] trovare un file .json e caricarlo in un dizionario
    - [x] controllarlo e sistemarlo
    - [x] creare una classe Pokémon
  - [x] input video
    - [x] creare una classe separata
    - [x] creare una funzione che permette di ottenere un frame dalla PiCamera (e fare i test)
    - [x] visualizzare l'immagine all'interno di un canvas
  - [x] struttura GUI
    - [x] creare un menu principale
    - [x] creare un pannello delle informazioni sull'app
    - [x] creare una schermata per il Pokédex, divisa in 2 parti (sinistra per il video input, destra per i dettagli del Pokémon)
    - [x] creare una vista per le impostazioni
  - [x] bottone per ottenere il frame corrente
  - [x] etichette ed entry per i dettagli del Pokémon (statistiche con barre dinamiche e di colori differenti)
  - [x] aggiungere bottoni per scorrere fra le evoluzioni successive (ad esempio: Eevee ha diverse evoluzioni possibili)
  - [x] cambiare la entry del "tipo/i" (da testo a immagine)
  - [x] aggiungere bottone per riprodurre il verso
    - [x] raccogliere i file audio dei versi
  - [x] aggiungere la lettura della descrizione
    - [x] ottenere i file audio delle descrizioni utilizzando un bot di lettura
  - [x] realizzare l'aggiornamento per lingue differenti
  - [x] rendere le impostazioni persistenti <!-- aggiungerlo a quello in inglese)
  - [x] modalità debug
- [ ] Setup Raspberry
  - [x] comprare i componenti
     - [x] display LCD
     - [x] PiCamera
     - [x] batteria (powerbank)
     - [x] speaker
     - [x] bottoni
     - [x] adattatore type-C a gomito
     - [x] convertitore A/D (ADS1115)
   - [ ] integrare i componenti
     - [x] display LCD
     - [x] PiCamera
     - [x] batteria
     - [x] speaker
     - [x] bottoni
     - [ ] joystick analogico
   - [x] preparare il SO (disabilitare password, abilitare le interfacce, risolvere le dipendenze, ...)
- [x] Deployment dell'app
  - [x] preparare l'ambiente (installare python3 e i package necessari)
  - [x] clonare la repo
  - [x] test dell'applicazione
- [x] Prorotipo del case ~50h
  - [x] progetto tecnico
  - [x] ritagliare il cartoncino ed incollare le parti
  - [x] verniciatura ad acrilico
- [x] Relazione
  - [x] impostare il documento in LaTeX
  - [x] abbozzare una possibile suddivisione in capitoli
  - [x] scrivere il report
- [ ] Presentazione
- [ ] Demo Video <!--building, test and different implementation parts-->
- [ ] Extra & Sviluppi Futuri
  - [ ] usare una rete neurale più complessa con il nuovo dataset
  - [ ] usare nuove forme di data augmentation
  - [ ] aggiungere un amplificatore allo speaker
  - [ ] inserire uno o più Led vicino all'obiettivo della PiCamera
  - [ ] aggiungere un'opzione alle impostazioni per abilitare/disabilitare il congelamento del video dopo aver scattato la foto
  - [ ] finire il modello 3D del case e stamparlo
  - [ ] estendere il Pokédex alle generazioni seguenti
  - [ ] fare il porting su mobile (Android. iOS)

## Strumenti
- [PyCharm](https://www.jetbrains.com/pycharm/)
- [Anaconda](https://www.anaconda.com/)
- [Jupyter Notebook](https://jupyter.org/)
- [Sketchup browser](https://app.sketchup.com/)

## Risorse
- dati Pokémon:
  - [dataset](https://www.kaggle.com/thedagger/pokemon-generation-one)
  - [dettagli](https://github.com/fanzeyi/pokemon.json)
  - [file audio dei versi]()
  - [file audio delle descrizioni](http://texttospeechrobot.com/)
- [Calibrazione camera con OpenCV](https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html)
- [Inferenza con Tensorflow-lite](https://www.tensorflow.org/lite/guide/inference)
- [Conversione con Tensorflow-lite](https://www.tensorflow.org/lite/convert)
- [Quantizzazione post-allenamento con Tensorflow-lite](https://www.tensorflow.org/lite/performance/post_training_quantization)

## Licenza
Distribuito sotto Licenza GPLv3. Vedi [`LICENSE`](https://github.com/TryKatChup/Poke-Pi-Dex/blob/main/LICENSE) per ulteriori informazioni.

## Contatti
* [TryKatChup](https://www.linkedin.com/in/karina-chichifoi/?locale=en_US)
* [Mikyll](https://www.linkedin.com/in/michele-righi/?locale=en_US)

<!-- ## Ringraziamenti -->

<!-- ## Meme -->


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[ask-me-anything-shield]: https://img.shields.io/badge/Ask%20me-anything-1abc9c.svg
[ask-me-anything-url]: https://github.com/TryKatChup/Poke-Pi-Dex/issues
[open-collab-shield]: https://colab.research.google.com/assets/colab-badge.svg
[open-collab-url]: https://github.com/TryKatChup/Poke-Pi-Dex/issues
[made-with-phyton-shield]: https://img.shields.io/badge/Made%20with-Python-14354C.svg
[made-with-phyton-url]: https://www.python.org/
[made-with-markdown-shield]: https://img.shields.io/badge/Made%20with-Markdown-1f425f.svg
[made-with-markdown-url]: http://commonmark.org
[open-source-shield]: https://badges.frapsoft.com/os/v1/open-source.png?v=103
[open-source-url]: https://github.com/ellerbrock/open-source-badges/
[license-shield]: https://img.shields.io/badge/License-GPLv3-blue.svg
[license-url]: http://perso.crans.org/besson/LICENSE.html
[raspberry-shield]: https://img.shields.io/badge/-RaspberryPi-C51A4A?&logo=Raspberry-Pi
[raspberry-url]: https://www.raspberrypi.org/
[keras-shield]: https://img.shields.io/badge/Keras-%23D00000.svg?logo=Keras&logoColor=white
[keras-url]: https://keras.io/
[tensorflow-shield]: https://img.shields.io/badge/TensorFlow-%23FF6F00.svg?logo=TensorFlow&logoColor=white
[tensorflow-url]: https://www.tensorflow.org/
[opencv-shield]: https://img.shields.io/badge/opencv-%23white.svg?logo=opencv&logoColor=white
[opencv-url]: https://opencv.org/
[nvidia-shield]: https://img.shields.io/badge/nVIDIA-%2376B900.svg?logo=nVIDIA&logoColor=white
[nvidia-url]: https://www.nvidia.com/

[downloads-shield]: https://img.shields.io/github/downloads/TryKatChup/Poke-Pi-Dex/total
[downloads-url]: https://github.com/TryKatChup/Poke-Pi-Dex/releases/latest
[contributors-shield]: https://img.shields.io/github/contributors/TryKatChup/Poke-Pi-Dex
[contributors-url]: https://github.com/TryKatChup/Poke-Pi-Dex/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/TryKatChup/Poke-Pi-Dex
[forks-url]: https://github.com/TryKatChup/Poke-Pi-Dex/network/members
[stars-shield]: https://img.shields.io/github/stars/TryKatChup/Poke-Pi-Dex
[stars-url]: https://github.com/TryKatChup/Poke-Pi-Dex/stargazers
[issues-shield]: https://img.shields.io/github/issues/TryKatChup/Poke-Pi-Dex
[issues-url]: https://github.com/mikyll/TryKatChup/Poke-Pi-Dex/issues
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?logo=linkedin&colorB=0077B5
[linkedin-url]: https://www.linkedin.com/in/michele-righi/?locale=en_US
