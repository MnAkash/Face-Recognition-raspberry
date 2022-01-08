You have to install dlib first.

Installing dlib:

Step #1: Update swap file size, boot options, and memory split:

sudo nano /etc/dphys-swapfile

Scroll down to the configuration which reads: CONF_SWAPSIZE=100 -> CONF_SWAPSIZE=1024

And then update it to use 1024MB rather than 100MB:

After you have updated the /etc/dphys-swapfile file, run the following two commands to restart the swap service:

sudo /etc/init.d/dphys-swapfile stop
sudo /etc/init.d/dphys-swapfile start

Change your boot options
To accomplish this, execute:

sudo raspi-config

Restart your Raspberry Pi
Upon exiting, raspi-config will ask if you would like to reboot your system.

Go ahead and reboot, then we can move on with the rest of the install tutorial

Step #2: Install dlib prerequisites
The dlib library requires four prerequisites:

Boost Boost.Python CMake X11 These can all be installed via the following commands:

 sudo apt-get update
 sudo apt-get install build-essential cmake
 sudo apt-get install libgtk-3-dev
 sudo apt-get install libboost-all-dev
Step #3: Access your Python virtual environment (if you are using them)
Using Python’s virtualenv and virtualenvwrapper libraries, we can create separate Python environments for each project we are working on — this is considered a best practice when developing software in the Python programming language.

If you would like to install dlib into a pre-existing Python, virtual environment, use the workon command:

While this command will create a Python 3 virtual environment named py3_dlib : mkvirtualenv py3_dlib -p python3

Step #4: Use pip to install dlib with Python bindings
I'm using python3

pip3 install numpy
pip3 install scipy
pip3 install scikit-image
pip3 install dlib
Step #5: Test out your dlib install
python3
Python 3.6.9 (default, Nov  7 2019, 10:44:02) 
[GCC 8.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import dlib
>>>
Step #6: Reset your swap file size, boot options, and memory split
Important — before you walk away from your machine, be sure to reset your swap file size to 100MB

Reference: https://www.pyimagesearch.com/2017/05/01/install-dlib-raspberry-pi/

If cmake is needed:

go to: https://cmake.org/download/

download latest version of cmake for linux
extract the tar file and build the exe file
then again try:
pip install dlib
