# shebang

from os import name, listdir, makedirs, mkdir, remove
from urllib.request import urlopen, Request
from subprocess import Popen, PIPE, DEVNULL
from argparse import ArgumentParser
from mimetypes import guess_type
from os.path import basename
from random import choice
from PIL import Image
from time import time
from re import search
from sys import argv

def gen(letters: str, length: int) -> str:
	res = ""
	for _ in range(length): res += choice(letters)
	return res

CHARS = {1: "@%#*+=-:. ", 2: "@#$%?*+;:,,."}
CLEAR_WRAPPER = '''def clear():
	if name == "nt":
		Popen("cls").wait()

	else:
		Popen("clear").wait()\n
'''

arg_parser = ArgumentParser(description="Convert video to ASCII art")
arg_parser.add_argument("-w", dest="width", help="change the width of the ASCII art, default value is 105 (the value does not define the literal width of the art)", type=int, default=105, required=False)
arg_parser.add_argument("-e", dest="height", help="change the height of the ASCII art, default value is 32 (fhe value does not define the literal height of the ASCII art)", type=int, default=32, required=False)
arg_parser.add_argument("-s", dest="sharpness", help="change the sharpness of the art, the lower the better, default value is 4", type=int, default=4, required=False)
arg_parser.add_argument("-m", dest="mode", help="change the draw mode, default value is 1", type=int, default=1, required=False)
arg_parser.add_argument("-o", dest="outfile", help="draw ASCII art to a file", type=str, default="", required=False)
arg_parser.add_argument("-a", dest="audio", help="turn on audio support for video art (very unstable), default value is 'no'", metavar="YES|NO", type=str, default="no", required=False)
arg_parser.add_argument("-t", dest="sec", help="set audio offset for audio support, default value is 2.8", type=float, default=2.8, required=False)
arg_parser.add_argument("-u", dest="type", help="specify which interpreter to be used to render the ASCII art, default value is 'python'", type=str, default="python", required=False)
arg_parser.add_argument("-v", dest="vsync", help="add VSync to video art, this fix the problems of some ASCII art playing on double the speed. default value is 'yes'", metavar="YES|NO", type=str, default="yes", required=False)
arg_parser.add_argument("-g", dest="gchars", help = "change greyscale characters, default value is 'no'", metavar="YES|NO", type=str, default="no", required=False)
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
	quit()

else:
	type = type[0].split('/')[0]

	if type not in ["image", "video"]:
		print("\033[1;31mMedia: Unknown type\033[0m")
		quit()

arg_width = args.width
arg_height = args.height
audio = args.audio

if audio not in ["yes", "no"]:
	print("\033[1;31mAudio: Unknown option\033[0m")
	quit()

sec = args.sec
vsync = args.vsync

if vsync not in ["yes", "no"]:
	print("\033[1;31mVSync: Unknown option\033[0m")
	quit()

sharp = 26 + args.sharpness
out = args.outfile
xchars = args.gchars

if xchars == "yes":
	chars_idx = 2

elif xchars == "no":
	chars_idx = 1

else:
	print("\033[1;31mGreyscale characters: Unknown type\033[0m")
	quit()

interpreter = args.type

if interpreter == "shell" and name == "nt":
	print("\033[1;31mShell interpreter is not available on Windows currently, reverting to python\033[0m")
	interpreter = "python"

if interpreter not in ["python", "shell"]:
	print("\033[1;31mInterpreter: Unknown type\033[0m")
	quit()

mode = args.mode

if type == "video":
	if interpreter == "shell":
		if out == "":
			out = "out.sh"

	if interpreter == "python":
		if out == "":
			out = "out.py"

if mode == 2:
	GREYSCALE_CHARS = CHARS.get(chars_idx)[::-1]

elif mode == 1:
	GREYSCALE_CHARS = CHARS.get(chars_idx)

else:
	print("\033[1;31mMode: Unknown type\033[0m")
	quit()

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

	except IndexError: print("\033[1;31mAn error has occured. Cannot find character that matched with the pixel data. Try reducing the sharpness\033[0m"); quit()

	return ascii_str

if type == "video":
	frame_dir = gen("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_", 6)

	makedirs("./viddata/" + frame_dir + "/frames")

	if vsync == "yes":
		ffmpeg_raw_o = Popen(["ffmpeg", "-i", path], stdout=PIPE, stderr=PIPE).communicate()
		decoded_out = ffmpeg_raw_o[1].decode()
		fps = search("([0-9]+) tbr", decoded_out).group(1)

		if int(fps) > 32:
			mkdir("./viddata/" + frame_dir + "/video")

			if "/" in path:
				out_fname = basename(path)

			else:
				out_fname = path

			vid_out_path = "viddata/" + frame_dir + "/video/" + path
			Popen(["ffmpeg", "-i", path, "-filter:v", "-fps=30", "viddata/" + frame_dir + "/video/" + out_fname], stdout=DEVNULL, stderr=DEVNULL).wait()
			path = vid_out_path

	if interpreter == "python":
		if audio == "no" and vsync == "yes":
			with open(out, "w") as file:
				file.write("from subprocess import Popen\nfrom time import sleep, time\nfrom os import name\n\n" + CLEAR_WRAPPER)

		elif audio == "no" and vsync == "no":
			with open(out, "w") as file:
				file.write("from subprocess import Popen\nfrom os import name\n\n" + CLEAR_WRAPPER)

	print("\033[1;33mExtracting frames from source video\033[0m")
	Popen(["ffmpeg", "-i", path, "viddata/" + frame_dir + "/frames/%d.jpg"], stdout=DEVNULL, stderr=DEVNULL).wait()

	if audio == "yes":
		mkdir("./viddata/" + frame_dir + "/audio")
		print("\033[1;33mExtracting audio from the source video\033[0m")
		Popen(["ffmpeg", "-i", path, "-map", "0:a", "viddata/" + frame_dir + "/audio/out.mp3"], stdout=DEVNULL, stderr=DEVNULL).wait()

		if interpreter == "shell":
			with open(out, "w") as f:
				f.write("mpv viddata/{0}/audio/out.mp3 > /dev/null 2>&1 &\nsleep {1}\n\n".format(frame_dir, sec))

		elif interpreter == "python":
			with open(out, "w") as f:
				f.write('''from subprocess import Popen, DEVNULL
from os import name
from time import sleep

{0}
Popen(["mpv", "viddata/{1}/audio/out.mp3"], stdout=DEVNULL, stderr=DEVNULL)
sleep({2})\n
'''.format(CLEAR_WRAPPER, frame_dir, sec))

	frames = listdir("./viddata/" + frame_dir + "/frames")
	frame_nums = len(frames)

	if "https://" in og_path or "http://" in og_path: remove(path)

	if vsync == "yes":
		print("\033[1;33mCalculating average time to clear terminal screen\033[0m")

		tcls_data = []

		for i in range(frame_nums):
			tcls_pre = time()
			Popen("clear", stdout=DEVNULL).wait()
			tcls_post = time()
			tcls_delta = tcls_post - tcls_pre
			tcls_data.append(tcls_delta)
			print("\033[1;32mRetry " + str(i + 1) + "/" + str(frame_nums) + "\033[0m\r", end="")

		tcls_avg = 0.033 - (sum(tcls_data) / frame_nums)

	print("\n", end="")
	print("\033[1;33mGenerating ASCII art\033[0m")

	for y, z in enumerate(frames, 1):
		image = Image.open("viddata/" + frame_dir + "/frames/" + z)
		image = resize(image)
		gray_img = grayscale(image)
		ascii = px_to_as(gray_img)
		ascii_img = ""

		for x in range(0, len(ascii), gray_img.width): ascii_img += ascii[x:x+gray_img.width] + '\n'

		if interpreter == "shell":
			if vsync == "no":
				with open(out, "a") as file:
					file.write('''echo "
{0}"
clear\n
'''.format(ascii_img))

			elif vsync == "yes":
				with open(out, "a") as file:
					file.write('''echo "
{0}"
sleep {1}
clear\n
'''.format(ascii_img, tcls_avg))

		elif interpreter == "python":
			if vsync == "no":
				with open(out, "a") as file:
					file.write('''print("""
{0}""")
clear()\n
'''.format(ascii_img))

			elif vsync == "yes":
				with open(out, "a") as file:
					file.write('''print("""
{0}""")
sleep({1})
clear()\n
'''.format(ascii_img, tcls_avg))

		print("\033[1;32mFrame " + str(y) + "/" + str(frame_nums) + " has been rendered\033[0m\r", end="")

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
