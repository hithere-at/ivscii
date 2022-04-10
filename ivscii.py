# shebang

from os import listdir, makedirs, mkdir, remove
from urllib.request import urlopen, Request
from subprocess import Popen, DEVNULL
from argparse import ArgumentParser
from mimetypes import guess_type
from os.path import basename
from sys import argv, exit
from random import choice
from PIL import Image
from time import time
from re import search

def gen(letters: str, length: int) -> str:
	res = ""
	for _ in range(length): res += choice(letters)
	return res

CHARS = {1: "@%#*+=-:. ", 2: "@#$%?*+;:,,."}
CLEAR_WRAPPER = '''def draw(sleep_time, content):
	erase()
	addstr(content)
	sleep(sleep_time)
	refresh()

a = initscr()\n
'''

arg_parser = ArgumentParser(description="Convert video or image to ASCII art")
arg_parser.add_argument("-w", dest="width", help="change the width of the ASCII art, default value is 105", type=int, default=105, required=False)
arg_parser.add_argument("-he", dest="height_sub", help="change the height of the ASCII art, default value is 32 (fhe value does not define the literal height of the ASCII art)", type=int, default=32, required=False)
arg_parser.add_argument("-s", dest="sharpness", help="change the sharpness of the art, the lower the better, default value is 4", type=int, default=4, required=False)
arg_parser.add_argument("-m", dest="mode", help="change the draw mode, default value is 1", type=int, default=1, required=False)
arg_parser.add_argument("-o", dest="outfile", help="draw ASCII art to a file", type=str, default="", required=False)
arg_parser.add_argument("-a", dest="audio", help="turn on audio support for video art (very unstable), default value is 'no'", metavar="YES|NO", type=str, default="no", required=False)
arg_parser.add_argument("-t", dest="sec", help="set audio offset for audio support, default value is 2.8", type=float, default=2.8, required=False)
arg_parser.add_argument("-v", dest="fps_cap", help="add FPS cap to video art, default value is 'yes'", metavar="YES|NO", type=str, default="yes", required=False)
arg_parser.add_argument("-g", dest="gchars", help="change greyscale characters, default value is 'no'", metavar="YES|NO", type=str, default="no", required=False)
arg_parser.add_argument("--fps", dest="fps", help="change video frame rate, default value is 15", type=int, default=15, required=False)
arg_parser.add_argument("file|url", help="path to the video or image")

args = arg_parser.parse_args()
path = argv[len(argv) - 1]

if "https://" in path or "http://" in path:
	print("\033[1;33mDownloading file\033[0m")
	headers = Request(path, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
	og_path = path
	med_bin = urlopen(headers).read()
	path = basename(path)
	with open(path, "wb") as file: file.write(med_bin)

else:
	og_path = path # Fix the problem with undefined "og_path" variable

type = guess_type("./" + path)

if type[0] is None:
	print("\033[1;31mFile format: Unknown type\033[0m")
	exit()

else:
	type = type[0].split('/')[0]

	if type not in ["image", "video"]:
		print("\033[1;31mMedia: Unknown type\033[0m")
		exit()

arg_width = args.width
arg_height = args.height_sub
audio = args.audio
fps = args.fps

if fps > 35: print("\033[1;31mFrane rate cannot go over 35 in order to provide compatibility across devices\033[0m")

if audio not in ["yes", "no"]:
	print("\033[1;31mAudio: Unknown option\033[0m")
	exit()

sec = args.sec
fps_cap = args.fps_cap

if fps_cap not in ["yes", "no"]:
	print("\033[1;31mFrame cap: Unknown option\033[0m")
	exit()

sharp = 26 + args.sharpness
out = args.outfile
xchars = args.gchars

if xchars == "yes":
	chars_idx = 2

elif xchars == "no":
	chars_idx = 1

else:
	print("\033[1;31mGreyscale characters: Unknown type\033[0m")
	exit()

mode = args.mode

if type == "video":
	if out == "":
		out = "out.py"

if mode == 2:
	GREYSCALE_CHARS = CHARS.get(chars_idx)[::-1]

elif mode == 1:
	GREYSCALE_CHARS = CHARS.get(chars_idx)

else:
	print("\033[1;31mMode: Unknown type\033[0m")
	exit()

def resize(img):
	nwidth = arg_width
	width, height = img.size
	ratio = width / height
	nheight = int(ratio * nwidth) - arg_height
	return img.resize((nwidth, nheight))

def grayscale(img): return img.convert('L')

def px_to_as(img): # Pixels to ASCII
	img_pixels = img.getdata()
	ascii_str = ""

	try:
		for x in img_pixels: ascii_str += GREYSCALE_CHARS[x // sharp]

	except IndexError: print("\033[1;31mAn error has occured. Cannot find character that matched with the pixel data. Try reducing the sharpness\033[0m"); exit()

	return ascii_str

if type == "video":
	frame_dir = gen("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_", 6)

	makedirs("./viddata/" + frame_dir + "/frames")

	if audio == "no" and fps_cap == "yes":
		with open(out, "w") as file:
			file.write("from subprocess import Popen\nfrom time import sleep\nfrom unicurses import initscr, addstr, erase, refresh, endwin\n\n" + CLEAR_WRAPPER)

	elif audio == "no" and fps_cap == "no":
		with open(out, "w") as file:
			file.write("from subprocess import Popen\nfrom unicurses import initscr, addstr, erase, refresh, endwin\nfrom time import sleep\n\n" + CLEAR_WRAPPER)

	print("\033[1;33mExtracting frames from source video\033[0m")
	Popen(["ffmpeg", "-i", path, "-filter:v", "fps=" + str(fps), "viddata/" + frame_dir + "/frames/%d.jpg"], stdout=DEVNULL, stderr=DEVNULL).wait()

	if audio == "yes":
		mkdir("./viddata/" + frame_dir + "/audio")
		print("\033[1;33mExtracting audio from the source video\033[0m")
		Popen(["ffmpeg", "-i", path, "-map", "0:a", "viddata/" + frame_dir + "/audio/out.mp3"], stdout=DEVNULL, stderr=DEVNULL).wait()

		with open(out, "w") as f:
			f.write('''from subprocess import Popen, DEVNULL
from unicurses import initscr, addstr, erase, refresh, endwin
from time import sleep

{0}
Popen(["mpv", "viddata/{1}/audio/out.mp3"], stdout=DEVNULL, stderr=DEVNULL)
sleep({2})\n
'''.format(CLEAR_WRAPPER, frame_dir, sec))

	frames = listdir("./viddata/" + frame_dir + "/frames")
	frame_nums = len(frames)

	if "https://" in og_path or "http://" in og_path: remove(path)
	if fps_cap == "yes": frametime = 1 / fps

	print("\033[1;33mGenerating ASCII art\033[0m")

	for y, z in enumerate(frames, 1):
		image = Image.open("viddata/" + frame_dir + "/frames/" + z)
		image = resize(image)
		gray_img = grayscale(image)
		ascii = px_to_as(gray_img)
		ascii_img = ""

		for x in range(0, len(ascii), gray_img.width): ascii_img += ascii[x:x+gray_img.width] + '\n'

		if fps_cap == "no":
			with open(out, "a") as file:
				file.write('''draw(0.0, """
{0}""")\n
'''.format(ascii_img))

		elif fps_cap == "yes":
			with open(out, "a") as file:
				file.write('''draw({0}, """
{1}""")\n
'''.format(frametime, ascii_img))

		print("\033[1;32mFrame " + str(y) + "/" + str(frame_nums) + " has been rendered\033[0m\r", end="")

		with open(out, "a") as file:
			file.write("endwin()\n")

	print("\n", end="")
	print("\n\033[1;32mArt has been stored on \"" + out + "\"\033[0m")

else:
	print("\033[1;33mGenerating ASCII art\033[0m")
	image = Image.open(path)
	if "https://" in og_path or "http://" in og_path: remove(path)
	image = resize(image)
	gray_img = grayscale(image)
	ascii = px_to_as(gray_img)
	ascii_img = ""

	for x in range(0, len(ascii), gray_img.width): ascii_img += ascii[x:x+gray_img.width] + '\n'

	print(ascii_img)

	if out != "":
		with open(out, "w") as file:
			file.write(ascii_img)

		print("\n\033[1;32mArt has been stored on \"" + out + "\"\033[0m")
