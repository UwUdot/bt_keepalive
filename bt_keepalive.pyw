import pyaudio
import numpy as np
import time
import sys
import threading
from typing import Optional

class HeadphoneSoundPlayer:
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.is_playing = False
        self.running = True
        
        # Sound parameters - very low volume, high frequency (barely audible)
        self.sample_rate = 44100
        self.frequency = 18000  # 18kHz, barely audible for most people
        self.volume = 0.01  # Very low volume
        self.duration = 0.5  # Short duration
        self.check_interval = 2  # Check for headphones every 2 seconds
        
    def find_headphone_output(self) -> Optional[int]:
        """Find the index of the headphone output device"""
        for i in range(self.audio.get_device_count()):
            device_info = self.audio.get_device_info_by_index(i)
            device_name = device_info['name'].lower()
            
            # Check for headphone-related keywords
            headphones_keywords = ['headphone', 'headset', 'earphone', 'earbud']
            if any(keyword in device_name for keyword in headphones_keywords):
                return i
                
        # If no specific headphones found, use default output
        return self.audio.get_default_output_device_info()['index']
    
    def generate_sound(self) -> bytes:
        """Generate a very quiet, high-frequency sound"""
        t = np.linspace(0, self.duration, int(self.sample_rate * self.duration))
        # Generate sine wave
        wave = np.sin(2 * np.pi * self.frequency * t)
        # Apply very low volume
        wave = wave * self.volume
        # Convert to bytes
        wave = (wave * 32767).astype(np.int16)
        return wave.tobytes()
    
    def play_sound(self):
        """Play a single short sound burst"""
        if self.stream is None:
            return
            
        try:
            # Generate the sound
            sound_data = self.generate_sound()
            
            # Play the sound
            self.stream.write(sound_data)
            
        except Exception as e:
            # Silently handle errors
            pass
    
    def check_and_play(self):
        """Check for headphones and play if available"""
        while self.running:
            try:
                # Find headphone output
                device_index = self.find_headphone_output()
                
                if device_index is not None:
                    # Get device info
                    device_info = self.audio.get_device_info_by_index(device_index)
                    max_output_channels = device_info['maxOutputChannels']
                    
                    if max_output_channels > 0:
                        # Headphones are available, play sound
                        if self.stream is None:
                            self.stream = self.audio.open(
                                format=pyaudio.paInt16,
                                channels=1,
                                rate=self.sample_rate,
                                output=True,
                                output_device_index=device_index
                            )
                        
                        self.play_sound()
                        # Small delay between sounds
                        time.sleep(0.1)
                    else:
                        # No headphones, close stream if open
                        if self.stream is not None:
                            self.stream.close()
                            self.stream = None
                else:
                    # No headphones found
                    if self.stream is not None:
                        self.stream.close()
                        self.stream = None
                
                # Wait before checking again
                time.sleep(self.check_interval)
                
            except Exception as e:
                # Silently handle any errors
                if self.stream is not None:
                    try:
                        self.stream.close()
                    except:
                        pass
                    self.stream = None
                time.sleep(self.check_interval)
    
    def start(self):
        """Start the sound playing loop"""
        self.running = True
        self.thread = threading.Thread(target=self.check_and_play)
        self.thread.daemon = True
        self.thread.start()
        
    def stop(self):
        """Stop the sound playing loop"""
        self.running = False
        if self.stream is not None:
            self.stream.close()
        if self.audio is not None:
            self.audio.terminate()

def main():
    """Main function to run the script"""
    print("Headphone Sound Monitor")
    print("=======================")
    print("This script plays an almost inaudible sound when headphones are connected.")
    print("Press Ctrl+C to stop.")
    print()
    
    player = HeadphoneSoundPlayer()
    
    try:
        player.start()
        
        # Keep the main thread alive
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nStopping...")
        player.stop()
        print("Stopped.")
        sys.exit(0)

if __name__ == "__main__":
    main()
