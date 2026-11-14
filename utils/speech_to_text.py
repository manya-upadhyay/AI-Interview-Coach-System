import speech_recognition as sr
import io

def recognize_speech():
    """Recognize speech using local hardware microphone (for local testing)."""
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("🎤 Speak now...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("🎤 Start speaking after this message...")

            audio = recognizer.listen(
                source,
                timeout=10,
                phrase_time_limit=30
            )

        text = recognizer.recognize_google(audio, language="en-IN")
        print("Recognized:", repr(text))
        return text

    except (sr.WaitTimeoutError, sr.UnknownValueError):
        print("No speech detected or could not understand audio.")
        return ""

    except sr.RequestError as e:
        print("Google Speech API Error:", e)
        return ""

    except (AttributeError, OSError, Exception) as e:
        print("System Microphone Error (Cloud environment detected):", e)
        return "SYSTEM_MIC_UNAVAILABLE"



def recognize_speech_from_audio(audio_file):
    """Recognize speech from browser-recorded audio buffer (for Streamlit Cloud & browser mic)."""
    if not audio_file:
        return ""

    recognizer = sr.Recognizer()

    try:
        if hasattr(audio_file, "getvalue"):
            audio_bytes = io.BytesIO(audio_file.getvalue())
        elif hasattr(audio_file, "read"):
            audio_bytes = io.BytesIO(audio_file.read())
        else:
            audio_bytes = audio_file

        with sr.AudioFile(audio_bytes) as source:
            audio_data = recognizer.record(source)

        text = recognizer.recognize_google(audio_data, language="en-IN")
        print("Recognized from audio file:", repr(text))
        return text

    except sr.UnknownValueError:
        print("Could not understand audio.")
        return ""

    except sr.RequestError as e:
        print("Google Speech API Error:", e)
        return ""

    except Exception as e:
        print("Error processing audio file:", e)
        return ""