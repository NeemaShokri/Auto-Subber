import six

from google.cloud import speech
from google.cloud import translate_v2 as translate
from google.cloud import storage


class Cloud:

    def __init__(self, in_language, out_language):
        self.in_language = in_language
        self.out_language = out_language

    def audio_to_text(self, speech_file):
        """Transcribe the given audio file asynchronously."""
        client = speech.SpeechClient()
        file_name = speech_file.split("\\")[-1]
        self.upload('async_audio_files', speech_file, file_name)
        pass
        '''
        with io.open(speech_file, "rb") as audio_file:
            content = audio_file.read()
        '''

        """
         Note that transcription is limited to a 60 seconds audio file.
         Use a GCS file for audio longer than 1 minute.
        """
        uri = 'gs://async_audio_files/' + file_name
        print("uri: " + uri)
        audio = speech.RecognitionAudio(uri = uri)

        config = speech.RecognitionConfig(
            #encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
            sample_rate_hertz = 44100,
            language_code = self.in_language,
            enable_word_time_offsets = True,
            enable_automatic_punctuation = True
        )

        operation = client.long_running_recognize(config=config, audio=audio)

        print("Waiting for operation to complete...")
        response = operation.result(timeout=300)

        srt_file = open(speech_file.replace(".mp3", ".srt"), "wb")
        
        sequence = 1

        for result in response.results:
            alternative = result.alternatives[0]
            start_time = str (alternative.words[0].start_time)
            end_time = str (alternative.words[-1].end_time)
            
            srt_file.write(bytes((str (sequence) + "\n").encode("utf-8")))
            srt_file.write(bytes((self.format_time_stamp(start_time) + " --> " + self.format_time_stamp(end_time) + "\n").encode("utf-8")))
            srt_file.write(bytes((self.translate(alternative.transcript) + "\n" + "\n").encode("utf-8")))

            sequence += 1
        
        srt_file.close()

        self.delete_blob('async_audio_files', file_name)
        print("Done Transcribing .SRT")

    def translate(self, text: str) -> str:
        """Translates text into the target language.
        Target must be an ISO 639-1 language code.
        See https://g.co/cloud/translate/v2/translate-reference#supported_languages
        """

        if self.in_language == self.out_language:
            return text

        translate_client = translate.Client()

        if isinstance(text, six.binary_type):
            text = text.decode("utf-8")

        # Text can also be a sequence of strings, in which case this method
        # will return a sequence of results for each text.
        result = translate_client.translate(text, target_language=self.out_language[0:2])

        print(u"Text: {}".format(result["input"]))
        print(u"Translation: {}".format(result["translatedText"]))
        print(u"Detected source language: {}".format(result["detectedSourceLanguage"]))

        return result["translatedText"]

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

    def format_time_stamp(self, time_stamp):
        time_stamp = "0" + time_stamp
        if (len(time_stamp) == 8):
            time_stamp += ",000"
        else:
            time_stamp = time_stamp.replace(".", ",")
            time_stamp = time_stamp[0:12]

        return time_stamp