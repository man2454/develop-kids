import pygame
import pyttsx3
import os

class SoundManager:
    def __init__(self, base_path_audio):
        try:
            pygame.mixer.init()
            print("Pygame mixer initialized successfully.")
        except pygame.error as e:
            print(f"Warning: Pygame mixer could not be initialized. Sound effects will not work. Error: {e}")
            # Continue without mixer if it fails, TTS might still work.

        self.tts_engine = None
        try:
            self.tts_engine = pyttsx3.init()
            print("TTS engine initialized successfully.")
        except Exception as e:
            print(f"Warning: pyttsx3 engine could not be initialized. Text-to-speech will not work. Error: {e}")

        self.base_path_audio = base_path_audio
        self.sounds = {}
        self.selected_thai_voice_id = None

        if self.tts_engine:
            try:
                voices = self.tts_engine.getProperty('voices')
                # Attempt to find a Thai voice
                for voice in voices:
                    if "thai" in voice.name.lower() or "thai" in voice.id.lower():
                        self.selected_thai_voice_id = voice.id
                        print(f"Found Thai voice: {voice.name} ({voice.id})")
                        break
                
                if not self.selected_thai_voice_id:
                    # Fallback to checking language code 'th'
                    for voice in voices:
                        if hasattr(voice, 'languages') and voice.languages:
                            for lang in voice.languages: # voice.languages can be a list
                                if isinstance(lang, bytes): # sometimes it's bytes
                                    lang_code = lang.decode('utf-8', errors='ignore').split('_')[0]
                                else: # assuming it's a string
                                    lang_code = str(lang).split('_')[0]
                                if lang_code == 'th':
                                    self.selected_thai_voice_id = voice.id
                                    print(f"Found Thai voice by language code: {voice.name} ({voice.id})")
                                    break
                            if self.selected_thai_voice_id:
                                break
                
                if self.selected_thai_voice_id:
                    self.tts_engine.setProperty('voice', self.selected_thai_voice_id)
                else:
                    print("Warning: No specific Thai voice found. TTS will use the default system voice (likely English).")
            except Exception as e:
                print(f"Warning: Error during TTS voice setup: {e}")


    def load_sound(self, name, file_name):
        if not pygame.mixer.get_init():
            # print("Warning: Pygame mixer not initialized. Cannot load sound.") # Already warned in __init__
            return

        full_path = os.path.join(self.base_path_audio, file_name)
        if not os.path.exists(full_path):
            print(f"Warning: Sound file not found: {full_path}")
            return

        try:
            sound = pygame.mixer.Sound(full_path)
            self.sounds[name] = sound
            print(f"Sound '{name}' loaded from {full_path}")
        except pygame.error as e:
            print(f"Warning: Could not load sound {name} from {full_path}. Error: {e}")
        except Exception as e:
            print(f"Warning: An unexpected error occurred while loading sound {name}. Error: {e}")

    def play_sound(self, name, loops=0):
        if not pygame.mixer.get_init():
            # print("Warning: Pygame mixer not initialized. Cannot play sound.")
            return
        
        if name in self.sounds:
            try:
                self.sounds[name].play(loops=loops)
                # print(f"Playing sound: {name}") # Optional: for debugging
            except pygame.error as e:
                print(f"Warning: Could not play sound {name}. Error: {e}")
        else:
            print(f"Warning: Sound '{name}' not loaded. Cannot play.")

    def stop_sound(self, name):
        if not pygame.mixer.get_init():
            # print("Warning: Pygame mixer not initialized. Cannot stop sound.")
            return

        if name in self.sounds:
            try:
                self.sounds[name].stop()
            except pygame.error as e:
                print(f"Warning: Could not stop sound {name}. Error: {e}")
        # else:
            # print(f"Warning: Sound '{name}' not loaded. Cannot stop.") # Not critical to warn if trying to stop non-loaded sound

    def stop_all_sounds(self):
        if not pygame.mixer.get_init():
            # print("Warning: Pygame mixer not initialized. Cannot stop all sounds.")
            return
        try:
            pygame.mixer.stop()
        except pygame.error as e:
            print(f"Warning: Error stopping all sounds. Error: {e}")

    def speak(self, text, lang="th", use_cache=False): # use_cache not implemented yet
        if not self.tts_engine:
            print("Warning: TTS engine not initialized. Cannot speak.")
            return

        try:
            current_voice = self.tts_engine.getProperty('voice')
            target_voice_id = None

            if lang == "th":
                if self.selected_thai_voice_id:
                    target_voice_id = self.selected_thai_voice_id
                else: # Attempt to find a Thai voice again if not set during init or if different lang was used prior
                    voices = self.tts_engine.getProperty('voices')
                    for voice in voices: # Prioritize name/id checks
                        if "thai" in voice.name.lower() or "thai" in voice.id.lower():
                            target_voice_id = voice.id; break
                    if not target_voice_id: # Fallback to language code
                        for voice in voices:
                            if hasattr(voice, 'languages') and voice.languages:
                                for l_obj in voice.languages:
                                    l_code = (l_obj.decode('utf-8',errors='ignore') if isinstance(l_obj, bytes) else str(l_obj)).split('_')[0]
                                    if l_code == 'th': target_voice_id = voice.id; break
                            if target_voice_id: break
                    
                    if not target_voice_id:
                        print("Warning: Thai language selected, but no Thai voice found. Using default voice.")
            # else:
                # For other languages, or if lang is not "th", we'd use the default or find another voice.
                # Currently, it will just use the voice set (which is default or Thai if found in __init__)

            if target_voice_id and target_voice_id != current_voice:
                try:
                    self.tts_engine.setProperty('voice', target_voice_id)
                except Exception as e:
                    print(f"Warning: Could not set TTS voice to {target_voice_id}. Error: {e}")
            
            # If lang is not 'th' and no specific voice logic for it, it uses the current engine's voice.
            # If it's 'th' and a Thai voice was found (either in init or just now), it's set.
            # If it's 'th' and no Thai voice found, it uses default and prints a warning.

            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except RuntimeError as e: # Catches "runLoop already started" or other pyttsx3 runtime issues
            print(f"Warning: TTS engine error: {e}. Try restarting the application if issues persist.")
        except Exception as e:
            print(f"Warning: An unexpected error occurred during TTS speech. Error: {e}")

# Example usage (for testing purposes, normally not here)
if __name__ == '__main__':
    # This part needs Pygame to be initialized for mixer to work, 
    # but SoundManager itself tries to init mixer.
    # For standalone testing of SoundManager, you might init pygame here.
    pygame.init() # Needed for pygame.mixer.init() to not fail in some environments if called first

    # Create a dummy assets/audio directory and a test file for loading
    if not os.path.exists("assets/audio"):
        os.makedirs("assets/audio")
    with open("assets/audio/test_sound.wav", "w") as f: # Create a dummy wav file
        f.write("dummy_wav_data") # Not a real wav, but tests file existence

    sm = SoundManager(base_path_audio="assets/audio/")
    sm.load_sound("test", "test_sound.wav") # Will likely warn about format if not a real wav
    sm.play_sound("test")
    
    sm.speak("สวัสดีครับ ทดสอบระบบเสียงพูดภาษาไทย", lang="th")
    sm.speak("Hello, this is a test of the English voice.")

    # Clean up dummy file
    if os.path.exists("assets/audio/test_sound.wav"):
        os.remove("assets/audio/test_sound.wav")

    pygame.quit() # Clean up pygame
    print("SoundManager test finished.")
