import youtube_dl

def validate_youtube_link(link):
    try:
        with youtube_dl.YoutubeDL({}) as ydl:
            info_dict = ydl.extract_info(link, download=False)

            if 'entries' in info_dict:
                # It's a playlist or multiple videos
                return False
            elif info_dict.get('_type') == 'url':
                # It's a video
                return True
            elif info_dict.get('extractor') == 'youtube:channel':
                # It's a channel
                return True
            else:
                return False
    except youtube_dl.utils.DownloadError:
        return False

# Example usage:
video_link = "https://www.youtube.com/watch?v=QnhSGLUldMY"
channel_link = "https://www.youtube.com/c/your_channel_name"

if validate_youtube_link(video_link):
    print(f"The video link '{video_link}' is valid.")
else:
    print(f"The video link '{video_link}' is not valid.")

if validate_youtube_link(channel_link):
    print(f"The channel link '{channel_link}' is valid.")
else:
    print(f"The channel link '{channel_link}' is not valid.")
