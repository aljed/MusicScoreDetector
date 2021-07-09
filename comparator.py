import glob
import os


files = glob.glob('E:\\Muzyka\\**', recursive=True)
windows = files.map(lambda f: os.path.basename(f))

files2 = glob.glob('E:\\Muzyka\\**', recursive=True)
samsung = files2.map(lambda f: os.path.basename(f))