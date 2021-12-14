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
  
  <h1> Pokémon CV Revival</h1>
</div>

Our computer vision related project for nostalgic poke weebs (Sistemi digitali, Unibo).

<details open="closed">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li><a href="#demo">Demo</a></li>
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

## Demo
See our demo on YouTube! https://www.youtube.com/watch?v=6A07DGlRxg4 <!-- TO-DO -->

<div align="center">
  <img src="https://github.com/TryKatChup/Poke-Pi-Dex/blob/main/gfx/demo.png" width=50%/>
</div>

## Features
The application has the following features:
- it has a main menu showing controls and about panel;
- the Pokédex view shows a video stream from the camera;
- the user can take a picture of a Pokémon from the video stream;
- the app can make a prediction of the said picture, recognizing the Pokémon inside it with an excellent accuracy, by using a CNN;
- the classifier can recognize different objects such as cards, plushies, figures;
- the app shows the Pokémon info (name, id, types, description and stats) and the previous and following evolution stages of the Pokémon recognized;
- the app reads the description of the Pokémon as soon as the prediction happen;
- the app allows the user to play the Pokémon cry;
- the app has a settings view where the user can edit parameters such as language (English and Italian), fullscreen, volume;
- the has a debug mode to check the values of the prediction;
- the has an easter egg, try and find it!

## Full Overview
Check link a roba scritta da Kary

## Usage
To use the application follow these steps:

### Prerequisites
TO-DO
<!-- - OS:
- Python version
- Python packages
  - for Raspberry usage: -->

### Installation
TO-DO
<!-- - clone the repo or download the latest release -->


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
- [x] Case Prototype ~50h
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

<h2><a href="https://www.youtube.com/watch?v=Y7JG63IuaWs">Tool</a>s</h2>

- [PyCharm](https://www.jetbrains.com/pycharm/)
- [Anaconda](https://www.anaconda.com/)
- [Jupyter Notebook](https://jupyter.org/)
- [Sketchup browser](https://app.sketchup.com/)

## Resources
- Pokémon data:
  - [dataset](https://www.kaggle.com/thedagger/pokemon-generation-one)
  - [details](https://github.com/fanzeyi/pokemon.json)
  - [cry audio files]()
  - [description audio files](http://texttospeechrobot.com/)
- [Camera calibration with OpenCV](https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html)
- [Tensorflow-lite inference](https://www.tensorflow.org/lite/guide/inference)
- [Tensorflow-lite conversion](https://www.tensorflow.org/lite/convert)
- [Tensorflow-lite post-training quantization](https://www.tensorflow.org/lite/performance/post_training_quantization)

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
