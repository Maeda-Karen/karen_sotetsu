import cv2
from ffpyplayer.player import MediaPlayer
import time
import numpy as np

# 再生する動画ファイル
video_list = ["0722_火災_日本語006.mp4", "0722_地震_日本語006.mp4"]

ff_opts = {"out_fmt": "bgr24"}

window_name = "0722_火災地震_日本語006"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

def play_video(video_path):
    print(f"再生開始: {video_path}")
    player = MediaPlayer(video_path, ff_opts=ff_opts)

    while True:
        frame, val = player.get_frame()

        # 映像なし
        if frame is None:
            if val == 'eof':   # ファイル終了を検知
                print(f"終了: {video_path}")
                break
            time.sleep(0.01)
            continue

        # フレームを描画
        img, t = frame
        w, h = img.get_size()
        arr = np.frombuffer(img.to_bytearray()[0], np.uint8)
        arr = arr.reshape((h, w, 3))
        cv2.imshow(window_name, arr)

        # 'q'で強制終了
        if cv2.waitKey(1) & 0xFF == ord('q'):
            player.close_player()
            cv2.destroyAllWindows()
            exit()

        # 音声との同期
        if val is not None and isinstance(val, float):
            time.sleep(val)

    player.close_player()

# リストの動画を順番にループ再生
while True:
    for video in video_list:
        play_video(video)

cv2.destroyAllWindows()
print("すべての動画を再生しました。")