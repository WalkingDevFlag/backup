import psutil
import sounddevice as sd
import numpy as np

# Function to get process ID by name
def get_pid_by_name(process_name):
    for proc in psutil.process_iter(['pid', 'name']):
        if process_name.lower() in proc.info['name'].lower():
            return proc.info['pid']

# Function to capture and route audio streams
def capture_and_route_audio(process_name, output_device_index):
    pid = get_pid_by_name(process_name)
    if pid:
        # Capture audio from the specified process using a callback
        def audio_capture_callback(indata, frames, time, status):
            # Check if the captured audio is from the target process
            if is_audio_from_process(pid):  # Function to check process association
                sd.write(indata, device=output_device)  # Route to output device

        # Route audio to the specified output device
        output_devices = sd.query_devices(kind='output')
        if output_device_index < len(output_devices):
            output_device = output_devices[output_device_index]['immortal 121']
            with sd.InputStream(callback=audio_capture_callback):
                sd.sleep(10000)  # Capture for 10 seconds (modify as needed)

def is_audio_from_process(pid):
    # Implement logic to check process association with audio data
    # This might involve system-specific tools or libraries
    # Simplified example:
    return True  # Replace with actual process identification

# Example usage
process_name_brave = "brave.exe"
process_name_spotify = "spotify.exe"
output_device_index_earphones = 0
output_device_index_speaker = 1

# Capture and route audio for Brave browser and Spotify
capture_and_route_audio(process_name_brave, output_device_index_earphones)
capture_and_route_audio(process_name_spotify, output_device_index_speaker)
