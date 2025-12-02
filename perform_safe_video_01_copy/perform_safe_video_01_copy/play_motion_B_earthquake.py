from robottools import RobotTools
import time
from datetime import datetime, timezone, timedelta

# ===== 基本設定 =====
rt = RobotTools('192.168.50.50', 22222)
JST = timezone(timedelta(hours=+9), 'JST')

# ===== 目の色の設定 =====
RED = dict(L_EYE_R=255, L_EYE_G=0, L_EYE_B=0, R_EYE_R=255, R_EYE_G=0, R_EYE_B=0)
BLUE = dict(L_EYE_R=0, L_EYE_G=0, L_EYE_B=255, R_EYE_R=0, R_EYE_G=0, R_EYE_B=255)
YELLOW = dict(L_EYE_R=255, L_EYE_G=255, L_EYE_B=0, R_EYE_R=255, R_EYE_G=255, R_EYE_B=0)

# ===== ポーズのリセット =====
def reset_pose_motion():
    reset_pose = dict(HEAD_R=0, HEAD_P=-15, HEAD_Y=-90, BODY_Y=-52,
                  L_SHOU=-88, L_ELBO=-22, R_SHOU=84, R_ELBO=29)
    reset_map = BLUE
    pose = dict(Msec=1000, ServoMap=reset_pose, LedMap=reset_map)
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
    dict(Msec=1000,ServoMap=dict(HEAD_R=0,BODY_Y=-53,R_SHOU=85,HEAD_P=1,R_ELBO=59,L_ELBO=-55,HEAD_Y=1,L_SHOU=-88),LedMap = BLUE),
    dict(Msec=500,ServoMap=dict(HEAD_R=0,BODY_Y=-53,R_SHOU=85,HEAD_P=-21,R_ELBO=59,L_ELBO=-55,HEAD_Y=1,L_SHOU=-88),LedMap = BLUE),
    dict(Msec=500,ServoMap=dict(HEAD_R=0,BODY_Y=-53,R_SHOU=85,HEAD_P=1,R_ELBO=59,L_ELBO=-55,HEAD_Y=1,L_SHOU=-88),LedMap = BLUE),
    dict(Msec=500,ServoMap=dict(HEAD_R=0,BODY_Y=-53,R_SHOU=85,HEAD_P=-21,R_ELBO=59,L_ELBO=-55,HEAD_Y=1,L_SHOU=-88),LedMap = BLUE),
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

# ===== モーションのタイムライン (秒) =====
timeline = [
    (0.0, first_motion, "0:00| 初期ポーズ"),
    (20.0, nod_motion, "0:20| うなずき"),
    (38.0, awaawa_motion, "0:38| 地震発生"),
    (53.0, nod_motion, "0:53| うなずき"),
    (60.0, nod_motion, "1:00| うなずき"),
    (71.0, nod_motion, "1:11| うなずき"),
    (81.0, nod_motion, "1:21| うなずき"),
    (85.0, ng_motion, "1:25| NG"),
    (92.0, ng_motion, "1:32| NG"),
    (103.0, nod_motion, "1:43| うなずき"),
    (110.0, nod_motion, "1:50| うなずき"),
    (116.0, nod_motion, "1:56| うなずき"),
    (122.0, nod_motion, "2:02| 頭を抱える"),
    (131.0, nod_motion, "2:11| うなずき"),
    (141.0, nod_motion, "2:21| うなずき"),
    (155.0, nod_motion, "2:35| うなずき"),
    (171.0, nod_motion, "2:51| うなずき"),
    (182.0, nod_motion, "3:02| うなずき"),
    (191.0, nod_motion, "3:11| うなずき"),
    (206.0, nod_motion, "3:26| うなずき")
]

# ===== モーションの実行 =====

print("地震動画_ロボット動作シナリオ開始")
start_time = datetime.now(JST)

for i in range(len(timeline)):
    scheduled_time, motion, comment = timeline[i]

    while True:
        elapsed = (datetime.now(JST) - start_time).total_seconds()
        if elapsed >= scheduled_time:
            print(f"▶ {comment}")
            rt.play_motion(motion)
            reset_pose_motion()
            break
        else:
            time.sleep(0.05)

print("ロボット動作シナリオ終了")
