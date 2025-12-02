import subprocess
import os
from robottools import RobotTools
from datetime import datetime, timezone, timedelta

# ===== 基本設定 =====
rt = RobotTools('192.168.0.3', 22222)
JST = timezone(timedelta(hours=+9), 'JST')

## robottools_audio_ext.py
import socket
import os

class RobotToolsAudioExt:
    def __init__(self, rt):
        self.rt = rt  # 既存の RobotTools インスタンスを受け取る

    def play_wav_local(self, wav_path):
        """ローカルの .wav ファイルをSotaに送って再生"""
        if not os.path.exists(wav_path):
            raise FileNotFoundError(f"ファイルが見つかりません: {wav_path}")

        # wavファイル読み込み
        with open(wav_path, "rb") as f:
            wav_data = f.read()

        print(f"🎵 送信開始: {wav_path} ({len(wav_data)} bytes)")

        # RobotToolsが使用しているTCPソケットを使う
        sock = self.rt.sock if hasattr(self.rt, "sock") else self.rt.socket
        header = f"PLAY_WAV {os.path.basename(wav_path)} {len(wav_data)}\n".encode("utf-8")

        sock.sendall(header)
        sock.sendall(wav_data)
        print("🎧 再生コマンド送信完了")
