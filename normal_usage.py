import whisper
from pathlib import Path
'''
Size 	Parameters 	English-only model 	Multilingual model 	Required VRAM 	Relative speed
tiny 	39 M 	        tiny.en 	        tiny 	            ~1 GB 	        ~10x
base 	74 M 	        base.en 	        base 	            ~1 GB 	        ~7x
small 	244 M 	        small.en 	        small 	            ~2 GB 	        ~4x
medium 	769 M 	        medium.en 	        medium 	            ~5 GB 	        ~2x
large 	1550 M 	        N/A 	            large 	            ~10 GB 	        1x
turbo 	809 M 	        N/A 	            turbo 	            ~6 GB 	        ~8x
'''

model = whisper.load_model("base")
audiopath = Path('audiopath')
result = model.transcribe(audiopath)
print(result["text"])

filename = "file.txt"
try:
    with open(filename, "x") as f:
        f.write(result["text"])
except FileExistsError:
    print(f"ERROR: {filename} File Already exists.\n")