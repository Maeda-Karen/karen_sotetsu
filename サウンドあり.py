import threading
import time
from datetime import datetime, timezone, timedelta
from robottools import RobotTools
import FreeSimpleGUI as sg
import math
import os

# ===== 基本設定 =====
rt = RobotTools('192.168.31.150', 22222)
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
    dict(Msec=1000,ServoMap=dict(HEAD_R=0,BODY_Y=-53,R_SHOU=85,HEAD_P=1,R_ELBO=59,L_ELBO=-55,HEAD_Y=1,L_SHOU=-88),LedMap = BLUE),
    dict(Msec=500,ServoMap=dict(HEAD_R=0,BODY_Y=-53,R_SHOU=85,HEAD_P=-21,R_ELBO=59,L_ELBO=-55,HEAD_Y=1,L_SHOU=-88),LedMap = BLUE),
    dict(Msec=500,ServoMap=dict(HEAD_R=0,BODY_Y=-53,R_SHOU=85,HEAD_P=1,R_ELBO=59,L_ELBO=-55,HEAD_Y=1,L_SHOU=-88),LedMap = BLUE),
    dict(Msec=500,ServoMap=dict(HEAD_R=0,BODY_Y=-53,R_SHOU=85,HEAD_P=-21,R_ELBO=59,L_ELBO=-55,HEAD_Y=1,L_SHOU=-88),LedMap = BLUE),
]

#TV見ながら
nod_tv_motion = [
    dict(Msec=1000,ServoMap=dict(HEAD_R=0,HEAD_Y=-90,BODY_Y=-53,R_SHOU=85,HEAD_P=1,R_ELBO=59,L_ELBO=-55,L_SHOU=-88),LedMap = BLUE),
    dict(Msec=500,ServoMap=dict(HEAD_R=0,HEAD_Y=-90,BODY_Y=-53,R_SHOU=85,HEAD_P=-21,R_ELBO=59,L_ELBO=-55,L_SHOU=-88),LedMap = BLUE),
    dict(Msec=500,ServoMap=dict(HEAD_R=0,HEAD_Y=-90,BODY_Y=-53,R_SHOU=85,HEAD_P=1,R_ELBO=59,L_ELBO=-55,L_SHOU=-88),LedMap = BLUE),
    dict(Msec=500,ServoMap=dict(HEAD_R=0,HEAD_Y=-90,BODY_Y=-53,R_SHOU=85,HEAD_P=-21,R_ELBO=59,L_ELBO=-55,L_SHOU=-88),LedMap = BLUE),
]

#指さしながら
nod_fin_motion =[
    dict(Msec=1000,ServoMap=dict(HEAD_R=0,BODY_Y=-60,R_SHOU=-60,HEAD_P=1,R_ELBO=10,L_ELBO=-55,HEAD_Y=1,L_SHOU=-88),LedMap = BLUE),
    dict(Msec=500,ServoMap=dict(HEAD_R=0,BODY_Y=-60,R_SHOU=-60,HEAD_P=-21,R_ELBO=10,L_ELBO=-55,HEAD_Y=1,L_SHOU=-88),LedMap = BLUE),
    dict(Msec=500,ServoMap=dict(HEAD_R=0,BODY_Y=-60,R_SHOU=-60,HEAD_P=1,R_ELBO=10,L_ELBO=-55,HEAD_Y=1,L_SHOU=-88),LedMap = BLUE),
    dict(Msec=500,ServoMap=dict(HEAD_R=0,BODY_Y=-60,R_SHOU=-60,HEAD_P=-21,R_ELBO=10,L_ELBO=-55,HEAD_Y=1,L_SHOU=-88),LedMap = BLUE),
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
    dict(Msec=1000, ServoMap=dict(HEAD_R=0,BODY_Y=2,R_SHOU=0,HEAD_P=6,R_ELBO=93,L_ELBO=-92,HEAD_Y=31,L_SHOU=-8),LedMap = YELLOW),
    dict(Msec=500, ServoMap = dict(HEAD_R=0,BODY_Y=2,R_SHOU=0,HEAD_P=6,R_ELBO=93,L_ELBO=-92,HEAD_Y=-31,L_SHOU=-8),LedMap =  YELLOW),
    dict(Msec=500, ServoMap=dict(HEAD_R=0,BODY_Y=2,R_SHOU=0,HEAD_P=6,R_ELBO=93,L_ELBO=-92,HEAD_Y=31,L_SHOU=-8),LedMap =  YELLOW),
    dict(Msec=500, ServoMap = dict(HEAD_R=0,BODY_Y=2,R_SHOU=0,HEAD_P=6,R_ELBO=93,L_ELBO=-92,HEAD_Y=-31,L_SHOU=-8),LedMap =  YELLOW),
]
# 頭を抱える
head_motion = [
    dict(Msec=1000, ServoMap=dict(HEAD_R=0,BODY_Y=15,R_SHOU=-45,HEAD_P=10,R_ELBO=44,L_ELBO=-30,HEAD_Y=32,L_SHOU=54),LedMap = YELLOW),
    dict(Msec=500, ServoMap = dict(HEAD_R=0,BODY_Y=15,R_SHOU=-44,HEAD_P=10,R_ELBO=44,L_ELBO=-30,HEAD_Y=-32,L_SHOU=54),LedMap =  YELLOW),
    dict(Msec=500, ServoMap=dict(HEAD_R=0,BODY_Y=15,R_SHOU=-45,HEAD_P=10,R_ELBO=44,L_ELBO=-30,HEAD_Y=32,L_SHOU=54),LedMap = YELLOW),
    dict(Msec=500, ServoMap = dict(HEAD_R=0,BODY_Y=15,R_SHOU=-44,HEAD_P=10,R_ELBO=44,L_ELBO=-30,HEAD_Y=-32,L_SHOU=54),LedMap =  YELLOW),
    dict(Msec=500, ServoMap=dict(HEAD_R=0,BODY_Y=15,R_SHOU=-45,HEAD_P=10,R_ELBO=44,L_ELBO=-30,HEAD_Y=32,L_SHOU=54),LedMap = YELLOW),
    dict(Msec=500, ServoMap = dict(HEAD_R=0,BODY_Y=15,R_SHOU=-44,HEAD_P=10,R_ELBO=44,L_ELBO=-30,HEAD_Y=-32,L_SHOU=54),LedMap =  YELLOW),
    dict(Msec=500, ServoMap=dict(HEAD_R=0,BODY_Y=15,R_SHOU=-45,HEAD_P=10,R_ELBO=44,L_ELBO=-30,HEAD_Y=32,L_SHOU=54),LedMap = YELLOW),
    dict(Msec=500, ServoMap = dict(HEAD_R=0,BODY_Y=15,R_SHOU=-44,HEAD_P=10,R_ELBO=44,L_ELBO=-30,HEAD_Y=-32,L_SHOU=54),LedMap =  YELLOW)
]

relax_motion = [dict(Msec=1000, ServoMap = dict(HEAD_R=0,BODY_Y=0,R_SHOU=9,HEAD_P=0,R_ELBO=90,L_ELBO=-80,HEAD_Y=0,L_SHOU=-11),LedMap =  YELLOW),
              dict(Msec=1000, ServoMap = dict(HEAD_R=0,BODY_Y=0,R_SHOU=9,HEAD_P=-18,R_ELBO=90,L_ELBO=-80,HEAD_Y=0,L_SHOU=-11),LedMap =  YELLOW),
              dict(Msec=1000, ServoMap = dict(HEAD_R=0,BODY_Y=0,R_SHOU=9,HEAD_P=0,R_ELBO=90,L_ELBO=-80,HEAD_Y=0,L_SHOU=-11),LedMap =  YELLOW)
]

hot_motion = [dict(Msec=1000, ServoMap = dict(HEAD_R=0,BODY_Y=0,R_SHOU=-12,HEAD_P=-18,R_ELBO=80,L_ELBO=-12,HEAD_Y=0,L_SHOU=-81),LedMap =  YELLOW),
              dict(Msec=1000, ServoMap = dict(HEAD_R=0,BODY_Y=0,R_SHOU=-14,HEAD_P=-27,R_ELBO=68,L_ELBO=5,HEAD_Y=25,L_SHOU=-92),LedMap =  YELLOW),
              dict(Msec=1000, ServoMap = dict(HEAD_R=0,BODY_Y=0,R_SHOU=103,HEAD_P=-18,R_ELBO=15,L_ELBO=5,HEAD_Y=7,L_SHOU=-109),LedMap =  YELLOW)
]

fin_motion = [dict(Msec=1000, ServoMap = dict(HEAD_R=0,BODY_Y=0,R_SHOU=-38,HEAD_P=-21,R_ELBO=35,L_ELBO=5,HEAD_Y=-6,L_SHOU=-56),LedMap =  YELLOW),
              dict(Msec=1000, ServoMap = dict(HEAD_R=0,BODY_Y=0,R_SHOU=-38,HEAD_P=-21,R_ELBO=12,L_ELBO=5,HEAD_Y=-6,L_SHOU=-68),LedMap =  YELLOW),
]

# ===== モーションのタイムライン (秒) =====
timeline = [
    (0.0, first_motion, "0:00| 初期ポーズ","start.wav"),
    (17.0, nod_motion, "0:17| うなずき",None),
    (35.0, awaawa_motion, "0:35| 地震発生","警報.wav"),
    (46.0, head_motion, "0:46| 頭抱える",None),
    (52.0, nod_motion, "0:52| うなずき",None),
    (60.0, nod_tv_motion, "1:00| TVうなずき",None),
    (67.0, fin_motion, "1:07| 指さし",None),
    (69.0, nod_motion, "1:09| うなずき",None),
    (78.0, nod_motion, "1:18| うなずき",None),
    (84.0, ng_motion, "1:24| NG","NG.wav"),
    (91.0, ng_motion, "1:31| NG","NG.wav"),
    (96.0, nod_motion, "1:36| うなずき",None),
    (101.0, nod_tv_motion, "1:41| TVうなずき",None),
    (108.0, fin_motion, "1:48| 指さし",None),
    (115.0, nod_motion, "1:55| うなずき",None),
    (123.0, nod_motion, "2:03| うなずき",None),
    (129.0, nod_motion, "2:09| うなずき",None),
    (140.0, nod_tv_motion, "2:20| TVうなずき",None),
    (144.0, nod_tv_motion, "2:24| TVうなずき",None),
    (151.0, fin_motion, "2:31| 指さし",None),
    (160.0, ng_motion, "2:40| NG","NG.wav"),
    (168.0, relax_motion, "2:48| 落ち着き",None),
    (175.0, fin_motion, "2:55| 指さし",None),
    (182.0, nod_tv_motion, "3:02| TVうなずき",None),
    (190.0, nod_motion, "3:10| うなずき",None),
    (199.0, relax_motion, "3:19| 落ち着き",None),
    (207.0, nod_motion, "3:27| うなずき",None)
]

# ===== timeline 実行部 =====
start_time = datetime.now(JST)  # 開始時刻を記録

for i, (scheduled_time, motion, comment, sound) in enumerate(timeline):
    while True:
        elapsed = (datetime.now(JST) - start_time).total_seconds()

        if elapsed >= scheduled_time:
            print(f"▶ {comment}")

            # --- 効果音あれば再生 ---
            if sound:
                sound_path = os.path.join(os.path.dirname(__file__), sound)
                if os.path.exists(sound_path):
                    threading.Thread(target=lambda: rt.play_wav(sound_path)).start()
                else:
                    print(f"効果音ファイルが見つかりません: {sound_path}")

            # --- モーション実行 ---
            rt.play_motion(motion)

            # --- 次のモーションまでの空き時間を計算 ---
            motion_time = motion_duration(motion)
            next_time = timeline[i + 1][0] if i < len(timeline) - 1 else scheduled_time + 5.0
            wait_time = next_time - (scheduled_time + motion_time)

            # --- アイドルモーション ---
            if wait_time > 0.1:
                play_idle(rt, idle_motion(), wait_time)

            # --- リセットポーズ ---
            reset_pose()
            time.sleep(0.05)

            # 次のタイムライン要素へ進む
            break
