
import os
import subprocess
from urllib.parse import quote

list_sentence = [
    # input sentences you want it read by Ms.google

    'ABCDEFG',
    'HIJKLMN',
    'OPQRSTUV',
    'WXYZ'

]

# establish normal speed file

for sentence in list_sentence:
    encode_url = quote(sentence)

    cmd = [
        'curl',
        '-X',
        'GET',
        f'https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl=zh-TW&q={encode_url}',
        '-o',
        f'./sound/normal/{sentence}_Normal.mp3'
    ]
    sen_output = subprocess.run(cmd)
    if sen_output.returncode == 0:
        print(f'Nice！[{sentence}]Download Completed')
    else:
        print(f'Oops！[{sentence}]Download Failed')


# Speed up audio file

for sentence in list_sentence:
    encode_url = quote(sentence)
    cmd2 = [
        './ffmpeg',
        '-i',
        f'./sound/normal/{sentence}_Normal.mp3',
        '-filter:a',
        'atempo=2.0',
        f'./sound/speed_up/{sentence}_2xSpeed.mp3'
    ]

    sen_output2 = subprocess.run(cmd2)
    if sen_output2.returncode == 0:
        print(f'[{sentence}] Convert Completed')
    else:
        print(f'[{sentence}] Convert Failed')


# combine audio file

input_dir = "./sound/speed_up"  # can change to normal
output_file = './sound/combined/combinedAudio_2xSpeed.mp3'


input_files = []
for f in os.listdir(input_dir):
    if f.endswith('.mp3'):
        input_files.append(f)


# sort files based on their modified time
input_files.sort(key=lambda x: os.path.getmtime(os.path.join(input_dir, x)))


# concat:file1|file2|file3
cmd3 = [
    'ffmpeg',
    '-i',
    f'concat:{ "|".join([f"./sound/speed_up/{f}" for f in input_files]) }',
    '-c', 'copy',
    output_file
]

subprocess.run(cmd3)
