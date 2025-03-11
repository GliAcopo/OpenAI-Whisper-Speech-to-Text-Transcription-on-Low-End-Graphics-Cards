```markdown
# Configuration Variables 
The only thing that you'll need to edit in order to interact with the project is the `USER VARIABLES` section. Just be sure to follow the instructions below.
Below is the snippet of code that defines the main configuration variables for the project:

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


```