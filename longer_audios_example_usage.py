import whisper
from pydub import AudioSegment
import os
from tqdm import tqdm
#from pathlib import Path
# dependencies:
'''
$pip instsall tqdm  # for the progress bar
$pip install  ffmpeg      # for the audio processing and segmentation

'''
# ---------------------------------------- USER VARIABLES ----------------------------------------
# memo: the "r" before the strings needs to be kept, please do not remove unless you know what you are doing
model_to_use = "tiny.en"                                                                        # Specifies which Whisper model variant to load. It is used later when calling whisper.load_model().
audiopath = r"F:\Whisper Model\Test.m4a"                                                        # The path to the audio file that will be processed.
format = "m4a"                                                                                  # Indicates the format of the input audio file. This is passed to the audio loading function.
audio_chunks_output_dir = r"F:\Whisper Model\Testchunks"                                        # Directory where the audio chunks will be saved after splitting.
chunk_length_ms = 10*60*1000                                                                    # Defines the length (in milliseconds) of each audio chunk; here, it is set to 10 minutes.
chunk_export_format = "mp4"                                                                     # Determines the file format used when exporting the audio chunks.
chunk_export_codec = "aac"                                                                      # Sets the codec for exporting the audio chunks.
path_in_which_to_save_transcription_file = r"F:\Whisper Model"                                  # The directory where the final transcription text file will be saved.
transcription_filename = r"output.txt"                                                          # The name of the transcription output file.
audio_language = "en"                                                                           # The language code for the audio, which is passed to the model for proper transcription.
# END------------------------------------- USER VARIABLES -------------------------------------END

'''
Size 	Parameters 	English-only model 	Multilingual model 	Required VRAM 	Relative speed
tiny 	39 M 	        tiny.en 	        tiny 	            ~1 GB 	        ~10x
base 	74 M 	        base.en 	        base 	            ~1 GB 	        ~7x
small 	244 M 	        small.en 	        small 	            ~2 GB 	        ~4x
medium 	769 M 	        medium.en 	        medium 	            ~5 GB 	        ~2x
large 	1550 M 	        N/A 	            large 	            ~10 GB 	        1x
turbo 	809 M 	        N/A 	            turbo 	            ~6 GB 	        ~8x
'''

def cut_the_audio_into_chunks(audiopath:str, chunk_length_ms=10*60*1000, audio_chunks_output_dir=os.getcwd(), format="m4a", chunk_export_format="mp4", chunk_export_codec="aac")-> list[str]:
    """
    @param: audio_chunks_output_dir = the dir in wich to save the audio chunks, it defaults to the dir where the script is currently running.
    @return: a list of the sigle chunks directories 
    """
    print("enetered cut_the_audio_into_chunks function")
    print(f"audio_chunks_output_dir is {audio_chunks_output_dir}")
    import math
    
    # Load the audio file (pydub uses ffmpeg for handling various formats)
    audio = AudioSegment.from_file(audiopath, format = format)
    print("audio file loaded")
    
    # Calculate total number of chunks based on audio length
    total_length_ms = len(audio)
    num_chunks = math.ceil(total_length_ms / chunk_length_ms)
    print(f"Got {num_chunks} audio chuncks across a total lenght of {total_length_ms}\n")
    
    # Create the output directory if it doesn't exist
    if not os.path.exists(audio_chunks_output_dir):
        os.makedirs(audio_chunks_output_dir)
        print(f"Created new directory {audio_chunks_output_dir}\n")
    
    list_of_audio_chunks_filenames = []
    for i in range(num_chunks):
        print(f"{i}):")
        
        out_transcription_filename = os.path.join(audio_chunks_output_dir, f"chunk_{i+1}.{chunk_export_format}")
        print(f"out_transcription_filename will be {out_transcription_filename}")
        
        # Check if the file already exists, if so skip the export
        if os.path.exists(out_transcription_filename):
            print(f"{out_transcription_filename} already exists. Skipping export...")
        else:
            start_ms = i * chunk_length_ms
            print(f"start_ms = {start_ms}")
            end_ms = start_ms + chunk_length_ms
            print(f"end_ms = {end_ms}")
            
            # Slice the audio for the current chunk
            chunk = audio[start_ms:end_ms]
            print("created chunk")
            
            # Export the chunk directly to file
            chunk.export(out_transcription_filename, format=chunk_export_format, codec=chunk_export_codec)
            print(f"Exported {out_transcription_filename}\n")
    
        # Append the transcription_filename to the list either way
        list_of_audio_chunks_filenames.append(out_transcription_filename)
    
    return list_of_audio_chunks_filenames

# ---------------------------------------- Verify if the directories given by the user are valid ----------------------------------------
if os.path.exists(audiopath):
    print(f"File found: os.path.exists(audiopath) = {os.path.exists(audiopath)}\n")
else:
    print(f"File not found: os.path.exists(audiopath) = {os.path.exists(audiopath)}\n")
    exit(1)
if os.path.exists(audio_chunks_output_dir):
    print(f"Dir found: os.path.exists(audio_chunks_output_dir) = {os.path.exists(audio_chunks_output_dir)}\n")
else:
    print(f"Dir not found: os.path.exists(audio_chunks_output_dir) = {os.path.exists(audio_chunks_output_dir)}\n")
    exit(1)
if os.path.exists(path_in_which_to_save_transcription_file):
    print(f"File found: os.path.exists(path_in_which_to_save_transcription_file) = {os.path.exists(path_in_which_to_save_transcription_file)}\n")
else:
    print(f"File not found: os.path.exists(path_in_which_to_save_transcription_file) = {os.path.exists(path_in_which_to_save_transcription_file)}\n")
    exit(1)
# END------------------------------------- Verify if the directories given by the user are valid -------------------------------------END

# ---------------------------------------- Transcribe the chunks ----------------------------------------
# the list of single audio chunks to transcribe
list_of_audio_chunks_filenames = cut_the_audio_into_chunks(audiopath, chunk_length_ms, audio_chunks_output_dir, format, chunk_export_format, chunk_export_codec)

model = whisper.load_model(model_to_use)
result_list = []
total_files = len(list_of_audio_chunks_filenames)

for index, chunk_filename in enumerate(tqdm(list_of_audio_chunks_filenames, total=total_files, desc="Processing files", unit="file"), start=1):
    result = model.transcribe(chunk_filename, language=audio_language)
    transcription_text = result["text"]
    result_list.append(transcription_text)                  # this part is not necessary if we want the whole dictionary of results and not just the text.
    print(transcription_text)
    # print(f"Audio {index} out of {total_files} processed.") the use of this print is redundant since we now use tqdm's progress bar.
# END------------------------------------- Transcribe the chunks -------------------------------------END

# ---------------------------------------- WRITE THE DOCUMENT ----------------------------------------
joined_result = "\n".join(result_list)

# Define file paths
filepath = os.path.join(path_in_which_to_save_transcription_file, transcription_filename)
backup_filepath = os.path.join(path_in_which_to_save_transcription_file, "transcribe_temp.txt")

# Write the file (or backup if it already exists)
try:
    with open(filepath, "x", encoding="utf-8") as f:
        f.write(joined_result)
    print(f"file was saved as {filepath}")
except FileExistsError:
    print(f"ERROR: {transcription_filename} File Already exists.")
    print("Creating backup 'transcribe_temp.txt' file")
    with open(backup_filepath, "w", encoding="utf-8") as f:
        f.write(joined_result)
    print(f"file was saved as {backup_filepath}")
# END------------------------------------- WRITE THE DOCUMENT -------------------------------------END
# ---------------------------------------- VERIFY DOCUMENT ----------------------------------------
# Verification function
def verify_file(file_path, expected_content):
    """Return True if the file exists and its content matches the expected content."""
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            file_content = f.read()
        return file_content == expected_content
    return False

# Ask user if they want to verify the document before proceeding
verify_choice = input("Do you want to verify the document before proceeding? (Y/N): ").strip().lower()

if verify_choice == "y":
    if verify_file(filepath, joined_result):
        print(f"{transcription_filename} saved correctly in {path_in_which_to_save_transcription_file}.")
    elif verify_file(backup_filepath, joined_result):
        print("Backup file 'transcribe_temp.txt' saved correctly.")
    else:
        print("Error: The file was not saved correctly.")
        # If verification fails, ask the user to choose a fallback option
        option = input("Would you like to choose another location (C) or print the output in the terminal (P)? (C/P): ").strip().lower()
        if option == "c":
            new_folder = input("Please enter the new folder path: ").strip()
            new_filepath = os.path.join(new_folder, transcription_filename)
            try:
                with open(new_filepath, "x", encoding="utf-8") as f:
                    f.write(joined_result)
                print(f"Document saved to {new_filepath}.")
            except Exception as e:
                print(f"Failed to save file in the new location: {e}")
        elif option == "p":
            print("Printing output to terminal:")
            print(joined_result)
        else:
            print("Invalid option. press enter to print output in terminal:")
            _ = input()
            print(joined_result)
else:
    print("Skipping verification.")
# END------------------------------------- VERIFY DOCUMENT -------------------------------------END


