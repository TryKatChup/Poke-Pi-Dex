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
  
  Our Deep Learning for Computer Vision related project for nostalgic poké weebs (Sistemi Digitali, University of Bologna).<br/>
We recreated a Pokédex clone, which recognizes pictures of Pokémon from the first generation, using a Convolutional Neural Network. It's built on Raspberry Pi4 with LCD display, PiCamera, speaker and some other components attached. The case is made of cardboard. 🌱
<img src="https://github.com/TryKatChup/Poke-Pi-Dex/blob/main/gfx/aaaaaaaaa.png"/>
</div>

<details open="closed">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <!--<li><a href="#demo">Demo</a></li>-->
    <li><a href="#features">Features</a></li>
    <li><a href="#full-overview">Full Overview</a></li>
    <li><a href="#usage">Usage</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#tools">Tools</a></li>
    <li><a href="#resources">Resources</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contacts">Contacts</a></li>
    <!-- <li><a href="#acknowledgements">Acknowledgements</a></li>
    <li><a href="#meme">Memotty</a></li> -->
  </ol>
</details>

<!--## Demo
See our demo on YouTube! https://www.youtube.com/watch?v=6A07DGlRxg4 <!-- TO-DO -->

<!--<div align="center">
  <img src="https://github.com/TryKatChup/Poke-Pi-Dex/blob/main/gfx/demo.png" width=50%/>
</div>-->

## Features
- Main menu with functionalities and `About` panel.
- Pokémon-image acquisition from app.
- Pokémon prediction of captured pic, with an excellent accuracy, using a Convolutional Neural Network.
- Different objects recognition, such as cards, plushies, figures.
- Pokémon info (name, id, types, description and stats) and the previous and following evolution stages of Pokémon recognized.
- Audio description of the predicted Pokémon.
- Play Pokémon cry.
- `Settings` view where users can edit parameters, such as language (English and Italian), fullscreen, volume.
- Debug mode to check the values of the prediction.
- Easter egg, try and find it!

## Full Overview
TO-DO

## Usage
To use the application follow these steps:
TO-DO
### Prerequisites
TO-DO
<!-- - OS:
- Python version
- Python packages
  - for Raspberry usage: -->

### Installation
TO-DO
<!-- - clone the repo or download the latest release -->

<h2><a href="https://www.youtube.com/watch?v=Y7JG63IuaWs">Tool</a>s</h2>

- [PyCharm](https://www.jetbrains.com/pycharm/)
- [Anaconda](https://www.anaconda.com/)
- [Docker](https://www.docker.com/)
- [Jupyter Notebook](https://jupyter.org/)
- [Sketchup browser](https://app.sketchup.com/)

## Resources
- Pokémon data:
  - [Old Dataset](https://www.kaggle.com/thedagger/pokemon-generation-one)
  - [Our New Dataset](https://www.kaggle.com/unexpectedscepticism/11945-pokmon-from-first-gen)
  - [Details](https://github.com/fanzeyi/pokemon.json)
  - [Cry audio files]()
  - [Description audio files](http://texttospeechrobot.com/)
- [Camera calibration with OpenCV](https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html)
- [Tensorflow-lite inference](https://www.tensorflow.org/lite/guide/inference)
- [Tensorflow-lite conversion](https://www.tensorflow.org/lite/convert)
- [Tensorflow-lite post-training quantization](https://www.tensorflow.org/lite/performance/post_training_quantization)

## Roadmap
- [x] Dataset
  - [x] find a decent dataset for the neural network
  - [x] fix (cut pictures) and extend it
- [x] Classifier
  - [x] CNN with 3 conv layers and 2 FC layers
  - [x] data augmentation (random flip, rotation, contrast, ~~brightness~~)
  - [x] try dropout
  - [x] try batch norm
  - [x] loss and accuracy graphs
  - [x] test real life pics
  - [x] improve old CNN
- [x] Application
  - [x] Pokémon repository
    - [x] find .json file and load it into a dictionary
    - [x] check and fix it
    - [x] create Pokémon class
  - [x] video input
    - [x] create a separate class
    - [x] make a function that can take a frame from the picamera (to test)
    - [x] display the image inside a canvas
  - [x] GUI structure
    - [x] create a main menu
    - [x] create an about panel
    - [x] create a main app view divided in 2 (left-side for video input, right-side for Pokémon details)
    - [x] create a settings panel
  - [x] button to get the current frame
  - [x] labels and entry for the Pokémon details (stats with dynamic bars and different colors)
  - [x] add buttons to scroll between multiple evolutions (example: Eevee has different evolutions)
  - [x] change the "type(s)" entry (from text to image)
  - [x] button to play cry
    - [x] collect cry audio files
  - [x] description voice reading
    - [x] collect description audio files with a bot
  - [x] different language update
  - [x] debug mode
- [ ] Raspberry Setup
  - [x] buy components
     - [x] LDC display
     - [x] PiCamera
     - [x] power supply (powerbank)
     - [x] speaker
     - [x] push buttons
     - [x] type-C elbow adapter
     - [x] A/D converter (ADS1115)
   - [ ] integrate components
     - [x] LCD display
     - [x] PiCamera
     - [x] power supply
     - [x] speaker
     - [x] buttons
     - [ ] analog joystick
   - [x] prepare OS (disable password, enable interfaces, ...)
- [x] App Deployment
  - [x] prepare environment (install python3 and required packages)
  - [x] clone the repo
  - [x] test the app
- [x] Case Prototype
  - [x] project
  - [x] cardboard cutout
  - [x] painting
- [x] Report
  - [x] setup a LaTeX document
  - [x] draft a possible subdivision into chapters
  - [x] write the report
- [ ] Presentation
- [ ] Demo Video <!--building, test and different implementation parts-->
- [ ] Extra & Future Developments
  - [ ] use a more comples neural network with the new dataset
  - [ ] use new form of data augmentation
  - [ ] add an amplifier to speaker
  - [ ] insert one or more white LEDs near the camera lens
  - [ ] add settings option to enable/disable the video freezing after taking a picture
  - [ ] finish the 3D model and print it
  - [ ] extend the Pokédex to the following Pokémon generations
  - [ ] porting of the application to mobile systems (Android, iOS)

## License
Distributed under the GPLv3 License. See [`LICENSE`](https://github.com/TryKatChup/Poke-Pi-Dex/blob/main/LICENSE) for more information.

## Contacts
* [TryKatChup](https://www.linkedin.com/in/karina-chichifoi/?locale=en_US)
* [Mikyll](https://www.linkedin.com/in/michele-righi/?locale=en_US)

<!-- ## Acknowledgements -->


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
