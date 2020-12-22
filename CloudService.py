import six

from google.cloud import translate_v2 as translate
from google.cloud import storage
from google.cloud import speech

class Cloud:

    def __init__(self, in_language, out_language):
        self.in_language = in_language
        self.out_language = out_language


    def audio_to_text(self, speech_file):
        """Transcribe the given audio file asynchronously."""
        client = speech.SpeechClient()

        self.upload('async_audio_files', speech_file, speech_file)

        '''
        with io.open(speech_file, "rb") as audio_file:
            content = audio_file.read()
        '''

        """
         Note that transcription is limited to a 60 seconds audio file.
         Use a GCS file for audio longer than 1 minute.
        """
        uri = 'gs://async_audio_files/' + speech_file
        print("uri: " + uri)
        audio = speech.RecognitionAudio(uri = uri)

        config = speech.RecognitionConfig(
            # encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
            # sample_rate_hertz = 44100,
            language_code=self.in_language,
            enable_word_time_offsets=True,
            enable_automatic_punctuation=True
        )

        operation = client.long_running_recognize(config=config, audio=audio)

        print("Waiting for operation to complete...")
        response = operation.result(timeout=300)
        print("Responses: " + str (len(response.results)))

        srt_file = open(speech_file.split(".")[0] + ".srt", "w+")

        sequence = 1

        for result in response.results:
            alternative = result.alternatives[0]

            start_time = str(alternative.words[0].start_time)
            end_time = str(alternative.words[-1].end_time)

            srt_file.write(str(sequence) + "\n")
            srt_file.write(self.format_time_stamp(start_time) + " --> " + self.format_time_stamp(end_time) + "\n")
            srt_file.write(translate(alternative.transcript) + "\n" + "\n")
            sequence += 1

        srt_file.close()
        self.delete_blob('async_audio_files', speech_file)
        print("Done Transcribing .SRT")

    def translate(self, text: str) -> str:
        """Translates text into the target language.
        Target must be an ISO 639-1 language code.
        See https://g.co/cloud/translate/v2/translate-reference#supported_languages
        """
        if (self.in_language == self.out_language):
            return text

        translate_client = translate.Client()

        if isinstance(text, six.binary_type):
            text = text.decode("utf-8")

        # Text can also be a sequence of strings, in which case this method
        # will return a sequence of results for each text.
        result = translate_client.translate(text, source_language=self.in_language,
                                            target_language=self.out_language)


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

    def format_time_stamp(self, time_stamp):
        time_stamp = "0" + time_stamp
        if (len(time_stamp) == 8):
            time_stamp += ",000"
        else:
            time_stamp = time_stamp.replace(".", ",")
            time_stamp = time_stamp[0:12]

        return time_stamp