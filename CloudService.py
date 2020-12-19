from configparser import ConfigParser
import six

from google.cloud import speech
from google.cloud import translate_v2 as translate
from google.cloud import storage

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

        self.upload('async-audio-file', speech_file, 'test/' + speech_file)

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
            language_code=language_code,
            enable_word_time_offsets=True,
            enable_automatic_punctuation=True
        )

        operation = client.long_running_recognize(config=config, audio=audio)

        print("Waiting for operation to complete...")
        response = operation.result(timeout=90)

        complete_text = []

        for result in response.results:
            alternative = result.alternatives[0]
            print("Transcript: {}".format(alternative.transcript))
            print("Confidence: {}".format(alternative.confidence))

            for word_info in alternative.words:
                word = word_info.word
                start_time = word_info.start_time
                end_time = word_info.end_time

                complete_text.append({'word': word, 'start': start_time, 'end': end_time})

                print(
                    f"Word: {word}, start_time: {start_time.total_seconds()}, end_time: {end_time.total_seconds()}"
                )
        
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

    def upload(self, bucket_name, source_file_name, destination_name):
        """Uploads a file to the bucket."""
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(destination_name)

        blob.upload_from_filename(source_file_name)

        return destination_name

    def delete_blob(self, bucket_name, blob_name):
        """Deletes a blob from the bucket."""
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)

        blob.delete()