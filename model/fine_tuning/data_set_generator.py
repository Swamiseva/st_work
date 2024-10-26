from sklearn.model_selection import train_test_split
import os

def prepare_data_with_single_file(audio_file, srt_file, test_size=0.2):
    # Ensure both the audio file and SRT file exist
    if not os.path.exists(audio_file) or not os.path.exists(srt_file):
        raise FileNotFoundError("Audio file or SRT file not found.")

    # Create a list containing the single audio file and SRT file
    audio_files = [audio_file]
    srt_files = [srt_file]

    # Split into training and validation sets
    train_audio_files, val_audio_files, train_srt_files, val_srt_files = train_test_split(
        audio_files, srt_files, test_size=test_size, random_state=42
    )

    # Create datasets for training and validation
    train_data = {"audio": train_audio_files, "transcription": train_srt_files}
    val_data = {"audio": val_audio_files, "transcription": val_srt_files}

    # Load and prepare the datasets
    train_dataset = load_dataset('csv', data_files=train_data)
    val_dataset = load_dataset('csv', data_files=val_data)

    # Cast the `audio` column to a format suitable for the model
    train_dataset = train_dataset.cast_column("audio", Audio(sampling_rate=16000))
    val_dataset = val_dataset.cast_column("audio", Audio(sampling_rate=16000))

    # Map the transcription into a format the model expects (using processor.tokenizer)
    train_dataset = train_dataset.map(lambda batch: processor(batch["transcription"]), batched=True)
    val_dataset = val_dataset.map(lambda batch: processor(batch["transcription"]), batched=True)

    return train_dataset, val_dataset
