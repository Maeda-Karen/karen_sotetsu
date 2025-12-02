import cv2
from ffpyplayer.player import MediaPlayer
import time
import numpy as np

# ffpyplayer のオプション
ff_opts = {"out_fmt": "bgr24"}

def play_video(video_path, window_name):
    
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
            print("動画の再生が中断されました")
            return

        # 音声との同期
        if val is not None and isinstance(val, float):
            time.sleep(val)

    player.close_player()
    print("動画の再生が完了しました。")
    return