import threading
import time
from datetime import datetime, timezone, timedelta
from robottools import RobotTools
import FreeSimpleGUI as sg
import math
import os

# ===== 基本設定 =====
rt = RobotTools('192.168.175.12', 22222)
JST = timezone(timedelta(hours=+9), 'JST')

# ===== 目の色の設定 =====
RED = dict(L_EYE_R=255, L_EYE_G=0, L_EYE_B=0, R_EYE_R=255, R_EYE_G=0, R_EYE_B=0)
BLUE = dict(L_EYE_R=0, L_EYE_G=0, L_EYE_B=255, R_EYE_R=0, R_EYE_G=0, R_EYE_B=255)
YELLOW = dict(L_EYE_R=255, L_EYE_G=255, L_EYE_B=0, R_EYE_R=255, R_EYE_G=255, R_EYE_B=0)

# ===== リセットポーズ =====
def reset_pose():
    pose = dict(Msec=800,
                ServoMap=dict(HEAD_R=0,HEAD_P=-15,HEAD_Y=-90,BODY_Y=-52,
                              L_SHOU=-88,L_ELBO=-22,R_SHOU=0,R_ELBO=92),
                LedMap=BLUE)
    rt.play_motion([pose])

def motion_duration(motion_list):
    if not motion_list:
        return 0.0
    return sum(m.get("Msec", 0) for m in motion_list) / 1000.0

# ===== アイドルモーション =====
def idle_motion():

    base_motion = [
        dict(Msec=1000, ServoMap=dict(HEAD_R=0,HEAD_P=-15,HEAD_Y=-90,BODY_Y=-52,L_SHOU=-88,L_ELBO=-22,R_SHOU=0,R_ELBO=92), LedMap=BLUE),
        dict(Msec=1000, ServoMap=dict(HEAD_R=0,HEAD_P=-10,HEAD_Y=-85,BODY_Y=-50,L_SHOU=-78,L_ELBO=-12,R_SHOU=10,R_ELBO=102), LedMap=BLUE)
    ]

    return base_motion

def play_idle(rt, base_motion, duration):
    idle_time = motion_duration(base_motion)  # 1サイクル ≒ 2秒
    repeat_count = int(duration // idle_time)
    remainder = duration % idle_time

    if duration < idle_time:
        print(f"⏸ アイドルなし ({duration:.2f}s)")
        reset_pose()
        return
    
        # --- アイドル部分 ---
    play_count = max(0,repeat_count - 1)
    if play_count > 0:
        for _ in range(play_count):
            rt.play_motion(base_motion)
            time.sleep(0.05)
        print(f"🌀 アイドルモーション {play_count} 回 ({play_count * idle_time:.2f}s)")

    # --- 余り時間（割り切れなかった部分） ---
    if remainder >= 0.5:
        print(f"🔹 残り {remainder:.2f}s → リセットポーズ中")
        reset_pose()
        time.sleep(remainder)
    else:
        print(f"🔹 残り {remainder:.2f}s → 無視（次へ）")

# ===== 各モーションの定義 =====
# 初期モーション
first_motion = [
    dict(Msec=1000, ServoMap=dict(HEAD_R=0,BODY_Y=0,R_SHOU=90,HEAD_P=-1,HEAD_Y=0,R_ELBO=0,L_ELBO=-43,L_SHOU=36),LedMap = BLUE),
    dict(Msec=1000, ServoMap = dict(HEAD_R=0,BODY_Y=0,R_SHOU=90,HEAD_P=-1,HEAD_Y=0,R_ELBO=0,L_ELBO=-43,L_SHOU=-2),LedMap = BLUE),
    dict(Msec=1000, ServoMap=dict(HEAD_R=0,BODY_Y=0,R_SHOU=90,HEAD_P=-1,HEAD_Y=0,R_ELBO=0,L_ELBO=-43,L_SHOU=36),LedMap = BLUE),
    dict(Msec=1000, ServoMap = dict(HEAD_R=0,BODY_Y=0,R_SHOU=90,HEAD_P=-1,HEAD_Y=0,R_ELBO=0,L_ELBO=-43,L_SHOU=-2),LedMap = BLUE)
]
# うなずく時のモーション
nod_motion =[
    dict(Msec=1000,ServoMap=dict(HEAD_R=0,BODY_Y=0,R_SHOU=85,HEAD_P=1,R_ELBO=59,L_ELBO=-55,HEAD_Y=1,L_SHOU=-88),LedMap = BLUE),
    dict(Msec=500,ServoMap=dict(HEAD_R=0,BODY_Y=0,R_SHOU=85,HEAD_P=-21,R_ELBO=59,L_ELBO=-55,HEAD_Y=1,L_SHOU=-88),LedMap = BLUE),
    dict(Msec=500,ServoMap=dict(HEAD_R=0,BODY_Y=0,R_SHOU=85,HEAD_P=1,R_ELBO=59,L_ELBO=-55,HEAD_Y=1,L_SHOU=-88),LedMap = BLUE),
    dict(Msec=500,ServoMap=dict(HEAD_R=0,BODY_Y=0,R_SHOU=85,HEAD_P=-21,R_ELBO=59,L_ELBO=-55,HEAD_Y=1,L_SHOU=-88),LedMap = BLUE)
]

#TV見ながら
nod_tv_motion = [
    dict(Msec=1000,ServoMap=dict(HEAD_R=0,HEAD_Y=-90,BODY_Y=-53,R_SHOU=85,HEAD_P=1,R_ELBO=59,L_ELBO=-55,L_SHOU=-88),LedMap = BLUE),
    dict(Msec=500,ServoMap=dict(HEAD_R=0,HEAD_Y=-90,BODY_Y=-53,R_SHOU=85,HEAD_P=-21,R_ELBO=59,L_ELBO=-55,L_SHOU=-88),LedMap = BLUE),
    dict(Msec=500,ServoMap=dict(HEAD_R=0,HEAD_Y=-90,BODY_Y=-53,R_SHOU=85,HEAD_P=1,R_ELBO=59,L_ELBO=-55,L_SHOU=-88),LedMap = BLUE),
    dict(Msec=500,ServoMap=dict(HEAD_R=0,HEAD_Y=-90,BODY_Y=-53,R_SHOU=85,HEAD_P=-21,R_ELBO=59,L_ELBO=-55,L_SHOU=-88),LedMap = BLUE)
]

#指さしながら
nod_fin_motion =[
    dict(Msec=1000,ServoMap=dict(HEAD_R=0,BODY_Y=0,R_SHOU=-60,HEAD_P=1,R_ELBO=10,L_ELBO=-55,HEAD_Y=1,L_SHOU=-88),LedMap = BLUE),
    dict(Msec=500,ServoMap=dict(HEAD_R=0,BODY_Y=0,R_SHOU=-60,HEAD_P=-21,R_ELBO=10,L_ELBO=-55,HEAD_Y=1,L_SHOU=-88),LedMap = BLUE),
    dict(Msec=500,ServoMap=dict(HEAD_R=0,BODY_Y=0,R_SHOU=-60,HEAD_P=1,R_ELBO=10,L_ELBO=-55,HEAD_Y=1,L_SHOU=-88),LedMap = BLUE),
    dict(Msec=500,ServoMap=dict(HEAD_R=0,BODY_Y=0,R_SHOU=-60,HEAD_P=-21,R_ELBO=10,L_ELBO=-55,HEAD_Y=1,L_SHOU=-88),LedMap = BLUE)
]

#安心うなずき
nod_hot_motion =[
    dict(Msec=1000,ServoMap=dict(HEAD_R=0,BODY_Y=0,R_SHOU=7,HEAD_P=-21,R_ELBO=93,L_ELBO=-36,HEAD_Y=0,L_SHOU=-90),LedMap = BLUE),
    dict(Msec=1000,ServoMap=dict(HEAD_R=0,BODY_Y=0,R_SHOU=63,HEAD_P=7,R_ELBO=82,L_ELBO=-36,HEAD_Y=0,L_SHOU=-90),LedMap = BLUE)
]

# 慌てている時のモーション
awaawa_motion = [
    dict(Msec=1000, ServoMap=dict(HEAD_R=0,BODY_Y=0,R_SHOU=-18,HEAD_P=0,R_ELBO=70,L_ELBO=-77,HEAD_Y=-2,L_SHOU=12),LedMap = RED),
    dict(Msec=500, ServoMap = dict(HEAD_R=0,BODY_Y=0,R_SHOU=-18,HEAD_P=-4,R_ELBO=70,L_ELBO=-77,HEAD_Y=39,L_SHOU=12),LedMap = RED),
    dict(Msec=500, ServoMap=dict(HEAD_R=0,BODY_Y=0,R_SHOU=-18,HEAD_P=0,R_ELBO=70,L_ELBO=-77,HEAD_Y=-2,L_SHOU=12),LedMap = BLUE),
    dict(Msec=500, ServoMap = dict(HEAD_R=0,BODY_Y=0,R_SHOU=-18,HEAD_P=-4,R_ELBO=70,L_ELBO=-77,HEAD_Y=39,L_SHOU=12),LedMap = RED),
    dict(Msec=500, ServoMap = dict(HEAD_R=0,BODY_Y=0,R_SHOU=-18,HEAD_P=0,R_ELBO=70,L_ELBO=-77,HEAD_Y=-2,L_SHOU=12),LedMap = RED),
    dict(Msec=500, ServoMap = dict(HEAD_R=0,BODY_Y=0,R_SHOU=-18,HEAD_P=-4,R_ELBO=70,L_ELBO=-77,HEAD_Y=39,L_SHOU=12),LedMap = RED),
    dict(Msec=500, ServoMap = dict(HEAD_R=0,BODY_Y=0,R_SHOU=-18,HEAD_P=0,R_ELBO=70,L_ELBO=-77,HEAD_Y=-2,L_SHOU=12),LedMap = RED),
    dict(Msec=500, ServoMap = dict(HEAD_R=0,BODY_Y=0,R_SHOU=-18,HEAD_P=-4,R_ELBO=70,L_ELBO=-77,HEAD_Y=39,L_SHOU=12),LedMap = RED),
    dict(Msec=500, ServoMap = dict(HEAD_R=0,BODY_Y=0,R_SHOU=-18,HEAD_P=0,R_ELBO=70,L_ELBO=-77,HEAD_Y=-2,L_SHOU=12),LedMap = RED)
]
# 禁止事項のモーション
ng_motion =  [
    dict(Msec=1000, ServoMap=dict(HEAD_R=0,BODY_Y=0,R_SHOU=0,HEAD_P=6,R_ELBO=93,L_ELBO=-92,HEAD_Y=31,L_SHOU=-8),LedMap = YELLOW),
    dict(Msec=500, ServoMap = dict(HEAD_R=0,BODY_Y=0,R_SHOU=0,HEAD_P=6,R_ELBO=93,L_ELBO=-92,HEAD_Y=-31,L_SHOU=-8),LedMap =  YELLOW),
    dict(Msec=500, ServoMap=dict(HEAD_R=0,BODY_Y=0,R_SHOU=0,HEAD_P=6,R_ELBO=93,L_ELBO=-92,HEAD_Y=31,L_SHOU=-8),LedMap =  YELLOW),
    dict(Msec=500, ServoMap = dict(HEAD_R=0,BODY_Y=0,R_SHOU=0,HEAD_P=6,R_ELBO=93,L_ELBO=-92,HEAD_Y=-31,L_SHOU=-8),LedMap =  YELLOW)
]
# 袋の使い方
bag_motion = [
    dict(Msec=1000, ServoMap=dict(HEAD_R=0,BODY_Y=4,R_SHOU=-79,HEAD_P=-21,R_ELBO=8,HEAD_Y=2,L_ELBO=-8,L_SHOU=81),LedMap = BLUE),
    dict(Msec=500, ServoMap = dict(HEAD_R=0,BODY_Y=4,R_SHOU=-79,HEAD_P=-21,R_ELBO=8,HEAD_Y=2,L_ELBO=2,L_SHOU=81),LedMap = BLUE)
]

#袋ぱさぱさ
bag2_motion = [
    dict(Msec=1000, ServoMap=dict(HEAD_R=0,BODY_Y=0,R_SHOU=6,HEAD_P=-1,R_ELBO=93,L_ELBO=-34,HEAD_Y=0,L_SHOU=36),LedMap = BLUE),
    dict(Msec=1000, ServoMap = dict(HEAD_R=0,BODY_Y=0,R_SHOU=59,HEAD_P=-1,R_ELBO=23,L_ELBO=-93,HEAD_Y=0,L_SHOU=-49),LedMap = BLUE),
    dict(Msec=1000, ServoMap=dict(HEAD_R=0,BODY_Y=0,R_SHOU=-43,HEAD_P=-1,R_ELBO=28,L_ELBO=-93,HEAD_Y=0,L_SHOU=-10),LedMap = BLUE),
    dict(Msec=1000, ServoMap = dict(HEAD_R=0,BODY_Y=0,R_SHOU=62,HEAD_P=-1,R_ELBO=83,L_ELBO=-8,HEAD_Y=0,L_SHOU=-58),LedMap = BLUE)
]
         

#紐を結ぶ
line_motion = [
    dict(Msec=1000, ServoMap=dict(HEAD_R=0,BODY_Y=0,R_SHOU=-4,HEAD_P=-6,R_ELBO=93,L_ELBO=-93,HEAD_Y=0,L_SHOU=-1),LedMap = BLUE),
    dict(Msec=1000, ServoMap = dict(HEAD_R=0,BODY_Y=0,R_SHOU=9,HEAD_P=-6,R_ELBO=71,L_ELBO=-67,HEAD_Y=0,L_SHOU=-10),LedMap = BLUE)
]

#決めポーズ
decide_motion = [
    dict(Msec=1000, ServoMap=dict(HEAD_R=0,BODY_Y=0,R_SHOU=-69,HEAD_P=-4,R_ELBO=10,L_ELBO=-66,HEAD_Y=0,L_SHOU=-80),LedMap = BLUE),
    dict(Msec=1500, ServoMap = dict(HEAD_R=0,BODY_Y=0,R_SHOU=-69,HEAD_P=-4,R_ELBO=10,L_ELBO=-21,HEAD_Y=0,L_SHOU=59),LedMap = BLUE)
]

# ===== モーションのタイムライン (秒) =====
timeline = [
    (0.0, first_motion, "0:00| 初期ポーズ","start.wav"),
    (13.0, nod_fin_motion, "0:13| 指さしてうなずき","start.wav"),
    (19.0, nod_tv_motion, "0:19| TVうなずき",None),
    (33.0, awaawa_motion, "0:33| あわわ",None),
    (45.0, nod_motion, "0:45| うなずき",None),
    (58.0, nod_motion, "0:58| うなずき",None),
    (81.0, nod_hot_motion, "1:21| 安心うなずき",None),
    (87.0, awaawa_motion, "1:27| あわわ",None),
    (106.0, nod_tv_motion, "1:46| TVうなずき",None),
    (117.0, nod_tv_motion, "1:57| TVうなずき",None),
    (121.7, ng_motion, "2:02| NG","incorrect.wav"),
    (126.75, ng_motion, "2:06| NG","incorrect.wav"),
    (133.0, nod_tv_motion, "2:13| TVうなずき",None),
    (139.0, nod_motion, "2:19| うなずき",None),
    (145.0, None, "2:25| None","jaja-n.wav"),
    (148.0, nod_motion , "0:15| うなずき",None),
    (152.0, bag_motion, "2:32| 袋の使い方","basabasa.wav"),
    (156.0, bag2_motion, "2:36| 袋ぱさぱさ","basabasa.wav"),
    (159.0, line_motion, "2:39| ひもを結ぶ",None),
    (162.0, None, "2:42| None","correct.wav"),
    (178.0, nod_tv_motion, "2:58| TVうなずき",None),
    (184.0, decide_motion, "3:04| 決めポーズ","clap.wav")
]


# ===== timeline 実行部 =====
start_time = datetime.now(JST)  # ← 開始時刻を記録

for i, (scheduled_time, motion, comment, sound) in enumerate(timeline):
    while True:
        elapsed = (datetime.now(JST) - start_time).total_seconds()  # ← 修正：経過秒を計算

        if elapsed >= scheduled_time:
            print(f"▶ {comment}")

            # --- 効果音 + モーション実行 ---
            if sound:
                sound_path = os.path.join(os.path.dirname(__file__), sound)
                if os.path.exists(sound_path):
                    threading.Thread(target=lambda: rt.play_wav(sound_path)).start()
                else:
                    print(f"効果音ファイルが見つかりません: {sound_path}")

            rt.play_motion(motion)

            # --- 次のモーションまでの空き時間を算出 ---
            motion_time = motion_duration(motion)
            next_time = timeline[i+1][0] if i < len(timeline)-1 else scheduled_time + 5.0
            wait_time = next_time - (scheduled_time + motion_time)

            if wait_time > 0.8:
                play_idle(rt, idle_motion(), wait_time - 0.5)

            reset_pose()
            time.sleep(0.3)
            break
        else:
            time.sleep(0.05)

print("ロボット動作シナリオ終了")
