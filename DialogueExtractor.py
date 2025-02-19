"""
Main functional class of the program. 
Handles all of the video and audio processing.
"""
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.AudioClip import concatenate_audioclips
from TimeStamp import TimeStamp

def extract_dialogue(subs_path, video_path, result_path, tolerance = 3):
    sub_times = _format_subs(subs_path, tolerance)
    print("Subs converted...")
    _generate_audio(sub_times, video_path, result_path)

def _format_subs(subs_path, tolerance):
    """
    Chooses the appropriate function based on the subtitle file.
    """
    if subs_path.endswith(".srt"):
        print("srt selected")
        return _format_subs_srt(subs_path, tolerance)
    elif subs_path.endswith(".ass"):
        print("ass selected")
        return _format_subs_ass(subs_path, tolerance)
    else:
        print("incompatible subtitle format")
        return None # Should throw exception.

def _format_subs_ass(subs_path, tolerance):

    def convert_to_TimeStamp(timestamp_string):
        timestamp = timestamp_string.split(":")
        hours = int(timestamp[0])
        minutes = int(timestamp[1])
        timestamp = timestamp[2].split(".")
        seconds = int(timestamp[0])
        miliseconds = int(timestamp[1])*10
        return TimeStamp(hours, minutes, seconds, miliseconds)

    formatted_subs = []
    with open(subs_path, "r", encoding="utf-8") as subs:
        for line in subs.readlines():
            if line.startswith("Dialogue:"): # Should only look at lines that start with Dialogue:
                elements = line.split(",")
                if elements[9] == "\n":
                    continue
                formatted_times = [convert_to_TimeStamp(elements[1]), convert_to_TimeStamp(elements[2])]
                formatted_subs = _update_subs(formatted_subs, formatted_times, tolerance)
    return formatted_subs

def _format_subs_srt(subs_path, tolerance):
    """
    Takes in subs in .srt format and generates a list of timestampped intervals.
    Tolerance can be used to prevent excessive cuts.

    :param subs_path: path to .srt file.
    :param tolerance: minimum number of seconds between each voice line for 
    for there to be a cut between them. Set to 5 by default.
    :returns: list of [TimeStamp, TimeStamp].
    """
    formatted_subs = []
    with open(subs_path, "r", encoding="utf-8") as subs:
        lines = subs.readlines()
        i = 0
        n = 1
        while i < len(lines):
            times = lines[i+1].split(" --> ")
            formatted_times = [TimeStamp.from_string(times[0]), TimeStamp.from_string(times[1])]
            formatted_subs = _update_subs(formatted_subs, formatted_times, tolerance)
            n += 1
            while i < len(lines) and lines[i] != str(n)+"\n":
                i += 1
    return formatted_subs

def _update_subs(formatted_subs, formatted_times, tolerance):
    """
    Works out all of the logic for merging clips together, given the tolerance.
    """
    if formatted_subs == []:
        formatted_subs.append(formatted_times)
    else:
        if formatted_times[0] < formatted_subs[-1][0]:
            return formatted_subs
        previousStamp = formatted_subs[-1][1]
        if (previousStamp + tolerance) > formatted_times[0]: # Merges timestamps
            formatted_subs[-1][1] = formatted_times[1]
        else:
            formatted_subs.append(formatted_times)
    return formatted_subs

def _generate_audio(sub_times, video_path, result_path):
    """
    Generates an audio file from a video, given a list of timestampped intervals.

    :param sub_times: list of [TimeStamp, TimeStamp].
    :param video_path: Path of video to be cut.
    :param result_path: Path to save the resulting audio file.
    :returns: Audio file with joined clips indicated by timestampped intervals.
    """
    episode = VideoFileClip(video_path).audio
    final_timestamp = TimeStamp(seconds=episode.duration)
    audio = []
    n = 1
    for sub in sub_times:
        print(f"Processing clip {n} of {len(sub_times)}")
        if sub[0] > final_timestamp:
            break
        if sub[1] > final_timestamp:
            sub[1] = final_timestamp
        n += 1
        clip = episode.subclipped(str(sub[0]), str(sub[1]))
        audio.append(clip)


    audio = concatenate_audioclips(audio)
    audio.write_audiofile(result_path)
