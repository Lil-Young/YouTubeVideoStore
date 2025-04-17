import os
import cv2
import yt_dlp

# 유튜브 영상 다운로드
def download_youtube_video(youtube_url, output_path="videos"):
    os.makedirs(output_path, exist_ok=True)

    # 유튜브에서 다운로드한 파일명을 직접 추적하도록 설정
    video_path = os.path.join(output_path, "%(title)s.%(ext)s")
    ydl_opts = {
        'outtmpl': video_path,  # yt-dlp가 저장하는 정확한 파일명을 지정
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',  # 항상 mp4로 변환
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(youtube_url, download=True)
        video_filename = ydl.prepare_filename(info_dict)  # yt-dlp가 실제 저장한 파일명 가져오기

    # 확장자를 mp4로 변경 (yt-dlp가 자동 변환)
    if not video_filename.endswith(".mp4"):
        video_filename = os.path.splitext(video_filename)[0] + ".mp4"

    video_path = os.path.join(output_path, os.path.basename(video_filename))
    
    print(f"다운로드 완료! 파일명: {video_path}")
    return video_path

# (interval 값)초 단위로 프레임 저장
def extract_frames(video_path, idx, output_folder="frames", interval=1):
    os.makedirs(output_folder, exist_ok=True)
    cap = cv2.VideoCapture(video_path)  # 영상 열기
    if not cap.isOpened():
        raise RuntimeError(f"OpenCV가 영상을 열 수 없습니다: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)  # 초당 프레임 수
    frame_interval = int(fps * interval)  # 프레임 간격을 (interval 값) 초마다로 변경

    count = 0
    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if count % frame_interval == 0:
            frame_path = os.path.join(output_folder, f"frame_{idx}_{frame_count}.jpg")
            cv2.imwrite(frame_path, frame)
            print(f"📸 저장됨: {frame_path}")
            frame_count += 1
        count += 1

    cap.release()
    print("프레임 추출 완료!")


# 다운로드 및 사진 추출을 하고싶은 유튜브 링크를 넣어주세요.
youtube_links = [
    "https://www.youtube.com/ex/link"
]


for idx, url in enumerate(youtube_links):
    print(f"\n [{idx+1}/{len(youtube_links)}] 유튜브 영상 다운로드 중: {url}")
    video_path = download_youtube_video(url)
    extract_frames(video_path, idx)