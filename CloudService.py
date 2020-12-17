from configparser import ConfigParser
from google.cloud import speech
import six
from google.cloud import translate_v2 as translate

import io

class Cloud:

    def __init__(self):
        # Read in api key from config file
        config = ConfigParser()
        config.read('config.ini')

        self.api_key = config['account']['api_key']
        print(self.api_key)

    def audio_to_text(self, speech_file, language_code: str) -> str:
        """Transcribe the given audio file asynchronously."""
        client = speech.SpeechClient()

        with io.open(speech_file, "rb") as audio_file:
            content = audio_file.read()

        """
         Note that transcription is limited to a 60 seconds audio file.
         Use a GCS file for audio longer than 1 minute.
        """
        audio = speech.RecognitionAudio(content=content)

        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
            sample_rate_hertz=16000,
            audio_channel_count=2,
            language_code=language_code
        )

        operation = client.long_running_recognize(config=config, audio=audio)

        print("Waiting for operation to complete...")
        response = operation.result(timeout=90)

        complete_text = ''

        # Each result is for a consecutive portion of the audio. Iterate through
        # them to get the transcripts for the entire audio file.
        for result in response.results:
            complete_text += result.alternatives[0].transcript

            # The first alternative is the most likely one for this portion.
            print(u"Transcript: {}".format(result.alternatives[0].transcript))
            print("Confidence: {}".format(result.alternatives[0].confidence))
        
        return complete_text

    def translate(self, text: str, source_language: str, target_language: str) -> str:
        """Translates text into the target language.

        Target must be an ISO 639-1 language code.
        See https://g.co/cloud/translate/v2/translate-reference#supported_languages
        """

        translate_client = translate.Client()

        if isinstance(text, six.binary_type):
            text = text.decode("utf-8")

        # Text can also be a sequence of strings, in which case this method
        # will return a sequence of results for each text.
        result = translate_client.translate(text, source_language=source_language,
                                            target_language=target_language)

        print(u"Text: {}".format(result["input"]))
        print(u"Translation: {}".format(result["translatedText"]))
        print(u"Detected source language: {}".format(result["detectedSourceLanguage"]))