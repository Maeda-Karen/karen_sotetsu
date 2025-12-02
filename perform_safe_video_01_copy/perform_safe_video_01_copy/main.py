from PIL import Image
import numpy as np
import cv2
import subprocess
import os
import play_video

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
window_name = "safe_video_play_window"
image_path = os.path.join(BASE_DIR, "safe_video_image_developer.jpg")

def show_main_screen():
    if not os.path.exists(image_path):
        print(f"⚠️ ファイルが見つかりません: {image_path}")
        return
    try:
        img = Image.open(image_path)
        img = np.array(img.convert("RGB"))[:, :, ::-1]  # RGB→BGR
        cv2.imshow(window_name, img)
    except Exception as e:
        print(f"❌ 画像の読み込みエラー: {e}")

def run_sequence(motion_script, video_file):
    motion_path = os.path.join(BASE_DIR, motion_script)
    video_path = os.path.join(BASE_DIR, video_file)

    if not os.path.exists(video_path):
        print(f"⚠️ 動画が見つかりません: {video_path}")
        return
    if not os.path.exists(motion_path):
        print(f"⚠️ モーションスクリプトが見つかりません: {motion_path}")
        return

    # モーション開始
    motion_proc = subprocess.Popen(["python", motion_path])
    # 動画再生
    play_video.play_video(video_path, window_name)
    # 終了時に子プロセスを止める
    if motion_proc.poll() is None:
        motion_proc.terminate()
    show_main_screen()

def main():
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    show_main_screen()
    while True:
        key = cv2.waitKey(100) & 0xFF
        if key == ord('a'):
            run_sequence("play_motion_A_fire.py", "0722_火災_日本語006.mp4")
        elif key == ord('b'):
            run_sequence("play_motion_B_earthquake.py", "0722_地震_日本語006.mp4")
        elif key == ord('q'):
            break
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()