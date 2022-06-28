# Short Title

Summarize a video or audio file using Watson

# Long Title

Use speech to text and transformer or ML based models to generate summary and insights from video or audio files

# Author
* [Manoj Jahgirdar](https://www.linkedin.com/in/manoj-jahgirdar-6b5b33142/)
* [Sharath Kumar RK](https://www.linkedin.com/in/sharath-kumar-rk-52aa2562/)

# URLs

### Github repo

* https://github.com/IBM/video-summarizer-using-watson


### Video Link
* https://www.youtube.com/watch?v=zEHNVXtspM0

# Summary

In this code pattern, you will learn to build an end to end framework for generating summaries & insights from video and/or audio files using a combination of IBM and Open source technologies.

# Description

It is always beneficial if we can get a gist of the content without going through the entire data and the problem adds more complexity if the data is in the form of a video or audio file. In this code pattern you will learn about building a robust solution for analyzing the video or audio files to quickly generate meaningful summary & insights using different Deep learning and Machine learning approaches. You will also learn about improving the readibility of the transcripts with IBM Watson Speech to Text speech recognition models, how to optimize the parameteres, train different speech to text models and learn about different state of the art language models used for summarizing the text.

When you have completed this code pattern, you will understand how to:

- Use Watson Speech to Text service to convert the human voice into the written word.
- Transcribe video/audio with greater readibility by tuning the Watson Speech to Text parameters.
- Generate summary, highlights & insights using Transformer & ML based models.
- Visualize the results on the GUI for quick consumption and analysis.

# Flow

<!--add an image in this path-->
![architecture](doc/source/images/architecture.png)

1. User uploads a video or audio file.
1. If it is a video, then audio is extracted from the video.
1. The audio is sent to Watson Speech to Text that transcribes the audio to text.
1. The text is processed to extract summary, keywords & insights with different approaches.
1. The speaker diarization, summary and transcript are displayed on the UI.
1. User can then download the insights.

# Instructions

> Find the detailed steps in the [README](https://github.com/IBM/video-summarizer-using-watson/blob/main/README.md) file.

1. Clone the repo
2. Create Watson Services
    - 2.1. Create Watson Speech to Text service on IBM Cloud
    - 2.2. Add Watson Speech to Text credentials to the application
3. Run the Application
4. Generate summary and insights from the data
5. Watson Speech to Text Optimization
6. Summarizer Optimization
