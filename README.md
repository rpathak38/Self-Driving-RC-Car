# Self-Driving-RC-Car
A GitHub repository with all code and schematics necessary to create a self-driving RC car (classical CV).

![Demo](https://snipboard.io/bsSdV7.jpg)

## Getting Started
All code and schematics required to construct the car can be found in this github repository. You will simply need an RC car with proportional steering abilities to begin the conversion to self-driving.

### Prerequisites
In order to run the self driving car project, you will need an installation of Python along with the ability to upload C code to your Arduino. 
The Arduino ide can be downloaded from [here][https://www.arduino.cc/en/software]. Follow the commands below in your favorite shell to acquire the necessary packages.
```
pip install opencv-python
pip install numpy
pip install pyserial
```

### Downloading
Use the command below in your favorite shell in order to download and test Simple along with the demo video.
```
git clone "https://github.com/rpathak38/Self-Driving-RC-Car.git"
```

### Running
Code can be run in either of two modes: SSH or Autonomous. In order to run in SSH mode, you must first SSH into the Raspberry Pi and run ```serial_comm.py```.
To instead run in autonomous mode, simply run the ```main.py``` file like below. The car will begin to navigate based on the lane lines it detects.

## Built With
[OpenCV](https://github.com/opencv/opencv) -- An Open Source Machine Vision Library

[Numpy](https://github.com/numpy/numpy) -- A fundamental package needed for scientific computing with Python.

[Pyserial](https://github.com/pyserial/pyserial) -- Serial communication package for arduino/Pi communication

## License
This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/rpathak38/Simple_Lane_Detection/blob/master/LICENSE) file for details.
