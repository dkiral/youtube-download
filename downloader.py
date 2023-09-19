import os
import requests
from pytube import YouTube
from tqdm import tqdm

def download_video_with_progress(url, output_path=None):
    try:
        yt = YouTube(url)

        stream = yt.streams.filter(progressive=True, file_extension="mp4").get_highest_resolution()

        if output_path is None:
            script_directory = os.path.dirname(os.path.abspath(__file__))
            output_path = script_directory

        file_path = os.path.join(output_path, yt.title + ".mp4")

        video_url = stream.url

        total_size = int(requests.head(video_url).headers.get('content-length', 0))

        progress_bar = tqdm(total=total_size, unit="B", unit_scale=True)

        with requests.get(video_url, stream=True) as response:
            response.raise_for_status()
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
                    progress_bar.update(len(chunk))

        progress_bar.close()  
        print("Download completed successfully! The video is saved in:", file_path)

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    video_url = input("Enter the YouTube video URL: ")

    download_video_with_progress(video_url)