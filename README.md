
# OpenAI Whisper Speech-to-Text Transcription on Low-End Graphics Cards

This repository provides a solution to run the OpenAI Whisper model on GPUs with less than 3GB of VRAM. By leveraging system RAM as shared memory, you can load and transcribe larger audio files—even if your GPU does not meet the recommended VRAM specifications.

## Overview

When using AI models like Whisper, VRAM (the dedicated memory of your graphics card) is typically used for both the model and the audio data. Although the Whisper model itself can run on low-end hardware by utilizing shared memory (i.e., system RAM), most transcription errors arise not from the model’s size but from the way audio files are handled. In particular, loading large audio files can quickly exceed VRAM limits and cause errors.

## How It Works

- **Shared Memory Usage:**  
  While the ideal scenario is to use a GPU with high VRAM, one can overcome VRAM constraints by using shared memory. This shared memory is essentially a portion of your system RAM that the GPU can access when its own memory is insufficient. Note that this method may be slower compared to using dedicated VRAM, but it makes running larger models feasible on low-end GPUs.

- **Handling Large Audio Files:**  
  The primary challenge is the Python library’s handling of audio files. Loading a very large audio file can overwhelm your available VRAM, leading to transcription errors. A simple yet effective solution is to split your audio into smaller segments and transcribe each piece individually. This approach not only avoids memory overload but also improves the reliability of the transcription process.

## Checking Your Shared Memory

Knowing how much shared memory (system RAM) you have is crucial for understanding your system’s capacity to compensate for limited VRAM. Here are some ways to check shared memory on different platforms:

- **Linux:**  
  Use commands like `free -h` or inspect `/proc/meminfo` to see your total system RAM.  
  Example:  
  ```bash
  free -h
  ```
  
- **Windows:**  
  Open the Task Manager (Ctrl + Shift + Esc), and check the “Performance” tab for memory details. Alternatively, use the “System Information” tool by typing `msinfo32` in the Run dialog.
  
- **macOS:**  
  Open “Activity Monitor” from the Applications > Utilities folder, and view the “Memory” tab to check your system’s RAM.

## What to expect

By applying these techniques, I successfully ran the most demanding Whisper model—the large version—on a graphics card with just 3GB of VRAM. This repository is a small but effective project aimed at helping others facing similar hardware limitations to transcribe larger audio files without errors.

# Prerequisites
Of course, you'll need to have the wisper model installed in order to run this program!
---
- That would also mean that you'll need a python evironment whit the following packets:
  - Whisper (of course)
  - pytorch torchvision torchaudio pytorch-cuda -c pytorch -c nvidia
  - ffmpeg
  - 
 
If you have any doubts, you can also follow [this guide](https://www.gpu-mart.com/blog/install-whisper-ai-on-windows) which walks you trough using miniconda in order to set up a virtual environment for your project.

# Configuration Variables 
The only thing that you'll need to edit in order to interact with the project is the `USER VARIABLES` section. In order to edit those just be sure to follow the instructions below.
This is the snippet of code that defines the main configuration variables for the project:

```python
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
```

## Variable Breakdown

- **model_to_use**  
  - **Purpose:** Specifies the Whisper model variant (in this case, `"tiny.en"`) that will be loaded for transcription.  
  - **Usage:** Passed as an argument to `whisper.load_model(model_to_use)` when initializing the model.

- **audiopath**  
  - **Purpose:** Provides the absolute path to the audio file you wish to transcribe.  
  - **Usage:** Used by the function `cut_the_audio_into_chunks()` to load the audio file using pydub.

- **format**  
  - **Purpose:** Defines the format of the input audio file (e.g., `"m4a"`).  
  - **Usage:** When loading the audio in `AudioSegment.from_file(audiopath, format=format)`, this variable ensures that pydub correctly interprets the file format.

- **audio_chunks_output_dir**  
  - **Purpose:** Specifies the directory where the audio chunks will be saved after splitting the main audio file.  
  - **Usage:**  
    - Verified at the start to ensure the directory exists.  
    - Used inside `cut_the_audio_into_chunks()` to write each audio chunk.

- **chunk_length_ms**  
  - **Purpose:** Sets the desired length for each audio chunk in milliseconds (10 minutes in this case).  
  - **Usage:**  
    - Determines how many chunks will be created by calculating the total duration of the audio file divided by this value.  
    - Defines the slice of the audio in the loop within `cut_the_audio_into_chunks()`.

- **chunk_export_format**  
  - **Purpose:** Specifies the file format for the exported audio chunks (e.g., `"mp4"`).  
  - **Usage:** Passed as a parameter to the `chunk.export()` method in `cut_the_audio_into_chunks()`.

- **chunk_export_codec**  
  - **Purpose:** Defines the codec (e.g., `"aac"`) used to export the audio chunks.  
  - **Usage:** Also provided to the `chunk.export()` function, ensuring the audio is encoded properly.

- **path_in_which_to_save_transcription_file**  
  - **Purpose:** Indicates the directory where the final transcription output file will be saved.  
  - **Usage:** This path is combined with `transcription_filename` to create the full file path for writing the transcription results.

- **transcription_filename**  
  - **Purpose:** The name of the file that will contain the full transcription text.  
  - **Usage:** Used to construct the final output path by joining it with `path_in_which_to_save_transcription_file`.

- **audio_language**  
  - **Purpose:** Indicates the language of the audio, ensuring that the Whisper model transcribes the audio correctly (e.g., `"en"` for English).  
  - **Usage:** Passed as a parameter to the `model.transcribe()` function when processing each audio chunk.

# Code breakdown
This is a teeny tiny micro project. (less than 200 lines long!), it should be fairly easy to edit to your liking. If you are looking to make some touches to the code, then you could find useful this mini-documentation.

---
## `cut_the_audio_into_chunks` function.

### Summary

- **Input:** An audio file and parameters defining how to split it.
- **Process:**  
  - Loads the audio file.  
  - Computes the total number of chunks based on the desired chunk length.  
  - Ensures the output directory exists.  
  - Iterates through the audio, slicing it into chunks and exporting each one.
- **Output:** Returns a list of file paths for the exported audio chunks.

### Function Signature and Purpose

```python
def cut_the_audio_into_chunks(audiopath:str, 
                              chunk_length_ms=10*60*1000, 
                              audio_chunks_output_dir=os.getcwd(), 
                              format="m4a", 
                              chunk_export_format="mp4", 
                              chunk_export_codec="aac") -> list[str]:
```

- **Purpose:**  
  Splits a long audio file into smaller chunks of a specified duration and saves each chunk as a separate file.
  
- **Parameters:**  
  - `audiopath`: The file path to the input audio file.  
  - `chunk_length_ms`: Duration of each chunk in milliseconds (default is 10 minutes).  
  - `audio_chunks_output_dir`: Directory where the audio chunks will be saved (default is the current working directory).  
  - `format`: Format of the input audio file (e.g., `"m4a"`).  
  - `chunk_export_format`: Format used when exporting each audio chunk (e.g., `"mp4"`).  
  - `chunk_export_codec`: Codec for encoding the exported audio chunks (e.g., `"aac"`).

- **Return:**  
  A list of file paths where each file corresponds to an exported audio chunk.

---

### Step-by-Step Code Breakdown

1. **Initial Debug Statements and Import:**

   ```python
   print("enetered cut_the_audio_into_chunks function")
   print(f"audio_chunks_output_dir is {audio_chunks_output_dir}")
   import math
   ```
   - **Debugging:** Prints messages to indicate the function has started and shows the output directory.
   - **Import:** Loads the `math` module (used later to round up the number of chunks).

2. **Loading the Audio File:**

   ```python
   audio = AudioSegment.from_file(audiopath, format=format)
   print("audio file loaded")
   ```
   - **Action:** Uses `AudioSegment.from_file` (from the pydub library) to load the audio file at `audiopath` with the specified format.
   - **Note:** This step requires that ffmpeg is installed, as pydub relies on it to handle various audio formats.

3. **Calculating the Number of Chunks:**

   ```python
   total_length_ms = len(audio)
   num_chunks = math.ceil(total_length_ms / chunk_length_ms)
   print(f"Got {num_chunks} audio chuncks across a total lenght of {total_length_ms}\n")
   ```
   - **Total Duration:** `total_length_ms` gets the total duration of the audio in milliseconds.
   - **Chunk Calculation:** Divides the total length by `chunk_length_ms` and rounds up using `math.ceil` to determine how many chunks are needed.
   - **Debugging:** Prints the number of chunks and total length for transparency.

4. **Ensuring the Output Directory Exists:**

   ```python
   if not os.path.exists(audio_chunks_output_dir):
       os.makedirs(audio_chunks_output_dir)
       print(f"Created new directory {audio_chunks_output_dir}\n")
   ```
   - **Check Directory:** Verifies whether `audio_chunks_output_dir` exists.
   - **Create Directory:** If it does not exist, the directory is created using `os.makedirs`.
   - **Debugging:** Informs the user if a new directory was created.

5. **Processing and Exporting Each Chunk:**

   ```python
   list_of_audio_chunks_filenames = []
   for i in range(num_chunks):
       print(f"{i}):")
       
       out_transcription_filename = os.path.join(audio_chunks_output_dir, f"chunk_{i+1}.{chunk_export_format}")
       print(f"out_transcription_filename will be {out_transcription_filename}")
       
       if os.path.exists(out_transcription_filename):
           print(f"{out_transcription_filename} already exists. Skipping export...")
       else:
           start_ms = i * chunk_length_ms
           print(f"start_ms = {start_ms}")
           end_ms = start_ms + chunk_length_ms
           print(f"end_ms = {end_ms}")
           
           chunk = audio[start_ms:end_ms]
           print("created chunk")
           
           chunk.export(out_transcription_filename, format=chunk_export_format, codec=chunk_export_codec)
           print(f"Exported {out_transcription_filename}\n")
       
       list_of_audio_chunks_filenames.append(out_transcription_filename)
   ```
   - **Initialization:**  
     - An empty list `list_of_audio_chunks_filenames` is created to store the file paths of the exported chunks.
   - **Loop Through Chunks:**  
     - Iterates from `i = 0` to `num_chunks - 1`.
     - **Filename Creation:** Constructs the output filename using the output directory and a naming convention (`chunk_{i+1}`) with the desired export format.
     - **File Existence Check:**  
       - If the file already exists, it skips the export to avoid redundancy.
       - If not, the function calculates:
         - **Start Time:** `start_ms = i * chunk_length_ms`
         - **End Time:** `end_ms = start_ms + chunk_length_ms`
       - **Slicing the Audio:**  
         - Extracts the segment of the audio corresponding to the current chunk using slicing (`audio[start_ms:end_ms]`).
       - **Exporting the Chunk:**  
         - Saves the chunk to `out_transcription_filename` using the specified export format and codec.
     - **Recording:**  
       - Regardless of whether the chunk was exported or already existed, its filename is appended to the `list_of_audio_chunks_filenames` list.

6. **Return the List of Chunks:**

   ```python
   return list_of_audio_chunks_filenames
   ```
   - **Outcome:** Returns a list containing the file paths for all audio chunks. This list can be used later for transcription or further processing.

---
## Initial Directories checks

```python
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
```

This code snippet performs a series of checks to ensure that the necessary file paths and directories exist before the program proceeds. Here's what each part does:
- **Audio File Check:**  
  It verifies whether the audio file specified by `audiopath` exists.  
  - If the file is found, it prints a confirmation message.
  - If not, it prints an error message and exits the program with an error code (`exit(1)`).

- **Audio Chunks Directory Check:**  
  It checks if the directory where the audio chunks are to be saved (`audio_chunks_output_dir`) exists.
  - If the directory is found, a confirmation message is printed.
  - If not, it prints an error message and stops execution.

- **Transcription File Directory Check:**  
  Similarly, it validates the existence of the directory where the final transcription file will be stored (`path_in_which_to_save_transcription_file`).
  - A success message is printed if found.
  - Otherwise, it prints an error and terminates the program.

## "Transcribe the Chunks" code block

### Summary

- **Initialization:**  
  The code starts by splitting the audio into chunks and loading the Whisper model.
- **Processing:**  
  It iterates over each audio chunk, transcribes them using the model, extracts the text, and saves the result.
- **Output:**  
  The transcribed texts are collected in `result_list` and printed to the console for review.

---

### Code Breakdown: Transcribe the Chunks

```python
# the list of single audio chunks to transcribe
list_of_audio_chunks_filenames = cut_the_audio_into_chunks(audiopath, chunk_length_ms, audio_chunks_output_dir, format, chunk_export_format, chunk_export_codec)
```

- **Purpose:**  
  Calls the `cut_the_audio_into_chunks` function with the provided configuration variables.
- **What it does:**  
  - Splits the original audio file into smaller chunks based on the defined `chunk_length_ms`.
  - Saves these chunks in the specified `audio_chunks_output_dir`.
  - Returns a list of file paths (`list_of_audio_chunks_filenames`) where each file corresponds to an exported audio chunk.

---

```python
model = whisper.load_model(model_to_use)
```

- **Purpose:**  
  Loads the Whisper model that will be used for transcription.
- **What it does:**  
  - Uses `whisper.load_model()` with `model_to_use` (e.g., `"tiny.en"`) to initialize and load the chosen model into memory.

---

```python
result_list = []
total_files = len(list_of_audio_chunks_filenames)
```

- **Purpose:**  
  Prepares variables for the transcription process.
- **What it does:**  
  - Initializes an empty list, `result_list`, to store the transcription text from each audio chunk.
  - Computes the total number of audio chunks (`total_files`) by getting the length of the `list_of_audio_chunks_filenames` list.

---

```python
for index, chunk_filename in enumerate(tqdm(list_of_audio_chunks_filenames, total=total_files, desc="Processing files", unit="file"), start=1):
```

- **Purpose:**  
  Iterates over each audio chunk for transcription.
- **What it does:**  
  - Uses `enumerate` to loop through the list of chunk filenames.
  - Wraps the iterable with `tqdm` to provide a progress bar, which shows the current progress, total number of files, and a description ("Processing files").
  - `start=1` makes the count start from 1 for readability.

---

```python
    result = model.transcribe(chunk_filename, language=audio_language)
```

- **Purpose:**  
  Transcribes the audio content of the current chunk.
- **What it does:**  
  - Calls the `transcribe` method of the loaded model.
  - Passes the current chunk's filename (`chunk_filename`) and the `audio_language` (e.g., `"en"`) to ensure the model transcribes in the correct language.
  - Returns a dictionary (`result`) containing transcription details (e.g., the transcribed text).

---

```python
    transcription_text = result["text"]
```

- **Purpose:**  
  Extracts the actual transcription text from the result.
- **What it does:**  
  - Accesses the `"text"` key in the `result` dictionary to retrieve only the transcription text, ignoring any additional metadata.

---

```python
    result_list.append(transcription_text)  # this part is not necessary if we want the whole dictionary of results and not just the text.
```

- **Purpose:**  
  Saves the transcription text for later use.
- **What it does:**  
  - Appends the extracted transcription text to the `result_list`.
  - Note: If full details of the transcription are needed, you could store the entire `result` dictionary instead.

---

```python
    print(transcription_text)
```

- **Purpose:**  
  Provides immediate feedback on the transcription.
- **What it does:**  
  - Prints the transcription text for the current chunk to the terminal, which helps in debugging and verifying that the transcription process is working.

---

```python
    # print(f"Audio {index} out of {total_files} processed.") the use of this print is redundant since we now use tqdm's progress bar.
```

- **Purpose:**  
  Indicates a previously used debug print statement.
- **What it does:**  
  - This line is commented out because the progress bar from `tqdm` already provides a visual update on the progress, making this print statement unnecessary.

---

## Write the Document code block

### Summary

- **Joining Transcriptions:**  
  The `joined_result` variable consolidates all transcribed text segments into one string with newline separators.
- **Defining File Paths:**  
  Two file paths are established—one for the main output and another as a backup—to ensure no data is lost if the main file exists.
- **Writing the Document:**  
  - The code attempts to create the main transcription file.  
  - If the file already exists, a backup file is generated instead to preserve the output.

---

### Code Breakdown: Write the Document

```python
joined_result = "\n".join(result_list)
```

- **Purpose:**  
  Combines all individual transcriptions into one single string.
- **What it does:**  
  - Joins all items from `result_list` (each containing a transcription segment) into a single string.
  - Inserts a newline (`\n`) between each segment, ensuring that each chunk appears on its own line.

---

```python
# Define file paths
filepath = os.path.join(path_in_which_to_save_transcription_file, transcription_filename)
backup_filepath = os.path.join(path_in_which_to_save_transcription_file, "transcribe_temp.txt")
```

- **Purpose:**  
  Sets up the paths where the final transcription document and a backup file will be saved.
- **What it does:**  
  - **`filepath`:**  
    - Combines the directory path (`path_in_which_to_save_transcription_file`) with the desired filename (`transcription_filename`) to create the full file path for the main transcription file.
  - **`backup_filepath`:**  
    - Creates an alternative path in the same directory using a fixed backup name (`"transcribe_temp.txt"`).  
    - This is used in case the main file already exists, to avoid overwriting existing data.

---

```python
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
```

- **Purpose:**  
  Writes the joined transcription text to a file, using a backup file if the intended file already exists.
- **What it does:**  
  - **Try Block:**  
    - Opens the file at `filepath` in exclusive creation mode (`"x"`).  
      - This mode creates the file only if it does not already exist; otherwise, it raises a `FileExistsError`.
    - Writes the combined transcription (`joined_result`) to the file.
    - Prints a confirmation message showing where the file was saved.
  - **Except Block (FileExistsError):**  
    - Catches the `FileExistsError` that occurs if the file already exists.
    - Prints an error message to alert the user that the file exists.
    - Creates and writes to a backup file at `backup_filepath` in write mode (`"w"`), which will overwrite any existing backup.
    - Prints a message confirming that the backup file has been saved.

---

## document verification section

### Summary

- **Verification Function:**  
  - Checks for the existence and correctness of a file's content.
  
- **User Interaction:**  
  - Asks whether to verify the saved document.
  - If chosen, attempts to verify both the primary and backup files.
  
- **Fallback Options:**  
  - If verification fails, the user can either:
    - Save the document to a new location, or
    - Print the transcription to the terminal.
  
- **Exit:**  
  - If the user skips verification, the process continues without further checks.

---

### 1. The `verify_file` Function

```python
def verify_file(file_path, expected_content):
    """Return True if the file exists and its content matches the expected content."""
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            file_content = f.read()
        return file_content == expected_content
    return False
```

- **Purpose:**  
  This function checks whether a file exists and if its content exactly matches the provided `expected_content`.

- **Step-by-Step Explanation:**  
  - **Check File Existence:**  
    - Uses `os.path.exists(file_path)` to determine if the file at `file_path` exists.
  - **Read File Content:**  
    - If the file exists, it opens the file in read mode with UTF-8 encoding.
    - The content is read into `file_content`.
  - **Content Comparison:**  
    - Compares `file_content` with the `expected_content` provided as an argument.
    - Returns `True` if they match; otherwise, returns `False`.
  - **File Not Found:**  
    - If the file does not exist, the function returns `False`.

---

### 2. Asking the User for Verification

```python
verify_choice = input("Do you want to verify the document before proceeding? (Y/N): ").strip().lower()
```

- **Purpose:**  
  Asks the user whether they want to perform a verification check on the saved document.

- **Step-by-Step Explanation:**  
  - **User Input:**  
    - The `input()` function prompts the user.
  - **Sanitization:**  
    - `.strip()` removes any leading or trailing whitespace.
    - `.lower()` converts the response to lowercase for standardized comparison.
  - **Result:**  
    - The result is stored in `verify_choice`.

---

### 3. Handling the User's Decision

#### a. If the User Chooses Verification

```python
if verify_choice == "y":
    if verify_file(filepath, joined_result):
        print(f"{transcription_filename} saved correctly in {path_in_which_to_save_transcription_file}.")
    elif verify_file(backup_filepath, joined_result):
        print("Backup file 'transcribe_temp.txt' saved correctly.")
    else:
        print("Error: The file was not saved correctly.")
        # If verification fails, ask the user to choose a fallback option
        option = input("Would you like to choose another location (C) or print the output in the terminal (P)? (C/P): ").strip().lower()
```

- **Primary Check:**  
  - The code first checks if the user's response is `"y"`, indicating that they want to verify the document.
  
- **Verification Process:**  
  - **Primary File Verification:**  
    - Calls `verify_file(filepath, joined_result)` to verify that the file at `filepath` contains the expected transcription (`joined_result`).
    - If successful, it prints a confirmation message indicating that the file was saved correctly.
  
  - **Backup File Verification:**  
    - If the primary file check fails, it then verifies the backup file (`backup_filepath`).
    - If the backup is correct, a message confirming the backup's success is printed.
  
  - **Failure Case:**  
    - If neither verification passes, it prints an error message.
    - Then, it prompts the user to choose a fallback action:
      - **Choose another location (option "C")** or
      - **Print the transcription output in the terminal (option "P")**.

#### b. Handling Fallback Options When Verification Fails

```python
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
```

- **Option "C" - Choosing a New Location:**  
  - Prompts the user to enter a new folder path.
  - Constructs a new file path using `os.path.join(new_folder, transcription_filename)`.
  - Attempts to create and write the transcription file in the new location:
    - Uses the mode `"x"` to create a new file, ensuring that an error is thrown if the file already exists.
  - If an error occurs during file writing, it catches the exception and prints an error message.

- **Option "P" - Printing Output to Terminal:**  
  - Simply prints the transcription result (`joined_result`) to the terminal.

- **Invalid Option:**  
  - If the user's input doesn't match either `"c"` or `"p"`, the code informs the user and defaults to printing the output in the terminal after an additional prompt.

#### c. If the User Chooses to Skip Verification

```python
else:
    print("Skipping verification.")
```

- **Purpose:**  
  - If the user does not choose `"y"` for verification, the code prints a message indicating that the verification step is being skipped.

---

