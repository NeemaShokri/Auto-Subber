# Auto-Subber
A desktop application that takes in a video file and will create subtitles for it in a chosen language.

<img src="Assets\App.png" title="Screenshot of application ui">

## Requirements
- Python 3.9 or later installed
- Having a Google Cloud Platform Service Account Key

## Getting Started
1. Clone the repository to your local machine by running the following in command line:
    ```
    git clone https://github.com/NeemaShokri/Auto-Subber.git
    ```
    Alternatively, you can download and extract the zip file from github.

2. Paste the absolute path to the _.json_ file containing the account key into the _authentication.json_. __Note: If your path contains backslashes make sure to use double backslashes instead__
 > File\Path\With\Backslashes -> File\\\Path\\\With\\\Backslashes

3. Open up command line in your local repository and install the required libraries by running the following command:
    ```
    pip install -r requirements.txt
    ```

## Usage
1. Browse for and select a video from your computer
2. Select the language that the video is in
3. Select that language that you would like to create subtitles in
4. Click on the _Generate .SRT_ to create the _.SRT_ file in the same directory as video file. ___Note: This could take a couple minutes depending on the size of the file___
5. Open up video in any media/video player and then select the newly generated _.srt_ file to disaply the subtitles

## Support
- [How to create a google platform service account key](https://cloud.google.com/iam/docs/creating-managing-service-account-keys#creating_service_account_keys)