import cv2
import subprocess
import play_video
import time

window_name = "safe_video_play_window"
image_path = "safe_video_image_developer.jpg"

# === メニュー画面 ===
def show_main_screen():
    img = cv2.imread(image_path)
    cv2.imshow(window_name, img)

# === 動画＋モーションの並列再生 ===
def run_sequence(motion_script, video_file):

    # モーション開始（子プロセス）
    motion_proc = subprocess.Popen(["python", motion_script])

    # 動画再生（動画が終わるまでブロック）
    play_video.play_video(video_file, window_name)

    # 動画終了 → モーション停止
    if motion_proc.poll() is None:
        motion_proc.terminate()
        motion_proc.wait()

    # 少し間を空ける（任意）
    time.sleep(0.5)

# === メイン ===
def main():
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    show_main_screen()

    # 動画とモーションの対応表
    sequences = [
        ("play_motion_A_fire.py", "0722_火災_日本語006.mp4"),
        ("サウンドあり.py", "0722_地震_日本語006.mp4"),
        ("play_motion_A_fire.py", "0722_火災_英語003.mp4"),
        ("サウンドあり.py",      "0722_地震_英語003.mp4")
    ]

    idx = 0

    while True:
        # qキーで全体終了
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break

        motion_script, video_file = sequences[idx]
        run_sequence(motion_script, video_file)

        # 次の動画へ（交互）
        idx = (idx + 1) % len(sequences)

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()