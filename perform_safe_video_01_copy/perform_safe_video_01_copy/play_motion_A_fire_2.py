import threading
import time
from datetime import datetime, timezone, timedelta
from robottools import RobotTools
import FreeSimpleGUI as sg

# ===== 基本設定 =====
rt = RobotTools('192.168.0.12', 22222)
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
    (0.0, first_motion, "0:00| 初期ポーズ","始まるよー"),
    (19.0, nod_fin_motion , "0:19| 指さしてうなずき","ここ、だいじ"),
    (33.0, awaawa_motion, "0:33| あわわ","どうしよう！"),
    (51.0, nod_tv_motion, "0:51| TVうなずき",None),
    (58.0, nod_motion, "0:58| うなずき","わかったー"),
    (81.0, nod_hot_motion, "1:21| 安心うなずき","よかったー"),
    (87.0, awaawa_motion, "1:27| あわわ","、、、大変だー、どうしよう！"),
    (106.0, nod_tv_motion, "1:46| TVうなずき",None),
    (117.0, nod_tv_motion, "1:57| TVうなずき",None),
    (122.0, ng_motion, "2:02| NG",None),
    (127.0, ng_motion, "2:07| NG",None),
    (133.0, nod_tv_motion, "2:13| TVうなずき",None),
    (139.0, nod_motion, "2:19| うなずき",None),
    (149.0, nod_motion, "2:29| うなずき","どうするのかなー"),
    (152.0, bag_motion, "2:32| 袋の使い方",None),
    (156.0, bag2_motion, "2:36| 袋ぱさぱさ",None),
    (159.0, line_motion, "2:39| ひもを結ぶ","こうか！"),
    (178.0, nod_tv_motion, "2:58| TVうなずき",None),
    (184.0, decide_motion, "3:04| 決めポーズ","みれくれてありがとう！"),
]
# ===== 実行部 =====

print("🔥 火災動画_ロボット動作シナリオ開始")
start_time = datetime.now(JST)
start = time.time()
end = time.time()

for scheduled_time, motion, comment, speech in timeline:
    while True:
        elapsed = (datetime.now(JST) - start_time).total_seconds()
        if elapsed >= scheduled_time:
            print(f"▶ {comment, speech}")

            if speech:
                # 発話と動作を同時に行う（スレッド使用）
                def speak():
                    d = rt.say_text(speech)
                    m = rt.make_beat_motion(d)
                    rt.play_motion(m)

                t = threading.Thread(target=speak)
                t.start()

                # メイン側では同時にモーション実行
                rt.play_motion(motion)

                # 発話が終わるまで待つ
                t.join()

            else:
                # 発話なしなら普通にモーションだけ実行
                rt.play_motion(motion)

            # モーション終了後にリセット（被り防止に少し待つ）
            time.sleep(0.3)
            reset_pose()
            break

        else:
            time.sleep(0.05)

print("ロボット動作シナリオ終了")