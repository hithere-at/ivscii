# ivscii
A Python script to convert image or video into ASCII art. Basically replicating an image or video with some characters.

## Showcase
### Image
![](https://github.com/hithere-at/ivscii/blob/master/examples/komi_ascii.jpg)

### Video
![](https://github.com/hithere-at/ivscii/blob/master/examples/osu_lazer.gif)

## Requirements
1. [Python](https://www.python.org/downloads/) 3.5 or above
2. [FFmpeg](https://www.ffmpeg.org/download.html)
3. [mpv](https://mpv.io/installation/) (Linux only, Windows untested)

## Installation 

### Windows
1. Download and install Python from [here](https://www.python.org/downloads/)
2. Download and install FFmpeg from [here](https://www.ffmpeg.org/download.html)
3. Download the source code of this repository [here](https://github.com/hithere-at/ivscii/archive/refs/tags/v1.2.zip) and extract it somewhere on your drive
4. Open your command prompt and type in 
```
pip install Pillow
```

5. Run the `ivscii.py` by typing in `python ivscii.py` on your command prompt followed by the arguments that you want to fill, it looks something like this: 

```
python ivscii.py -m 2 -w 100 -e 20 pictures/cute.jpg
```


### Linux
1. Install Python using your package manager
2. Install FFmpeg using your package manager
3. Install ncurses using your paclage manager in case you dont have one installed
3. Install mpv using your package manager (if you plan to use the audio support)
4. Copy and paste this script below: 
```sh
pip install Pillow
pip install uni-curses
mv ivscii.py ivscii
sed -i 's| shebang|\!/usr/bin/env python|' ivscii
chmod +x ivscii
sudo cp ivscii /usr/local/bin/ivscii && cd ..
```

### Android (Termux)
Copy and paste this script below:
```sh
pkg install ncurses
pkg install python
pip install uni-curses
pip install Pillow
pkg install ffmpeg
pkg install git
git clone https://github.com/hithere-at/ivscii.git && cd ivscii
mv ivscii.py ivscii
sed -i 's| shebang|\!/data/data/com.termux/files/usr/bin/python|' ivscii
chmod +x ivscii
cp ivscii $PREFIX/bin/ivscii && cd ..
```
If you plan to use audio suppport, install mpv by doing:
```pkg install mpv```

## Usage
```
usage: ivscii [-h] [-w WIDTH] [-he HEIGHT_SUB] [-s SHARPNESS] [-m MODE] [-o OUTFILE]
              [-a YES|NO] [-t SEC] [-v YES|NO] [-g YES|NO] [--fps FPS]
              file|url

Convert video to ASCII art

positional arguments:
  file|url        path to the video or image

optional arguments:
  -h, --help      show this help message and exit
  -w WIDTH        change the width of the ASCII art, default value is 105
  -he HEIGHT_SUB  change the height of the ASCII art, default value is 32 (the
                  value does not define the literal height of the ASCII art)
  -s SHARPNESS    change the sharpness of the art, the lower the better, default
                  value is 4
  -m MODE         change the draw mode, default value is 1
  -o OUTFILE      draw ASCII art to a file
  -a YES|NO       turn on audio support for video art (very unstable), default
                  value is 'no'
  -t SEC          set audio offset for audio support, default value is 2.8
  -v YES|NO       add FPS cap to video art, default value is 'yes'
  -g YES|NO       change greyscale characters, default value is 'no'
  --fps FPS       change video frame rate, default value is 15
```

## Note
- `ivscii` audio support and shell interpreter for Windows is disbaled due to inavailability of Windows machine (i had to guess the step). Sorry for the inconvenience
- Basically, i dont write the image to ASCII converter, i only add video support with or without audio support, and make the width and height of the art can be changed
- For the love of god, PLEASE DO NOT MAKE ANY PULL REQUEST TO THIS REPOSITORY. Its too hard to clean the code, and if you make a code refactor pull request, you are an absolute madlad

## Credits
- educative.io [how to turn image to ASCII](https://www.educative.io/edpresso/how-to-generate-ascii-art-from-image-using-python)