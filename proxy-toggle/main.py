import ctypes
import winreg

INTERNET_SETTINGS_KEY = ('\x53\x4f\x46\x54\x57\x41\x52\x45\x5c\x4d\x69\x63\x72\x6f\x73\x6f\x66\x74\x5c\x57'
                         '\x69\x6e\x64\x6f\x77\x73\x5c\x43\x75\x72\x72\x65\x6e\x74\x56\x65\x72\x73\x69\x6f'
                         '\x6e\x5c\x49\x6e\x74\x65\x72\x6e\x65\x74\x20\x53\x65\x74\x74\x69\x6e\x67\x73')
PROXY_SERVER_VALUE = '\x50\x72\x6f\x78\x79\x53\x65\x72\x76\x65\x72'
PROXY_ENABLE_VALUE = '\x50\x72\x6f\x78\x79\x45\x6e\x61\x62\x6c\x65'

MESSAGE_BOX_STYLE = {
    "MB_OK": 0x0,
    "MB_INFO": 0x40,
    "MB_ERROR": 0x10
}


def display_message_box(message_text, icon_style):
    ctypes.windll.user32.MessageBoxW(0, message_text, "Proxy Toggle", MESSAGE_BOX_STYLE["MB_OK"] | icon_style)


def toggle_proxy_settings():
    try:
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, INTERNET_SETTINGS_KEY, 0, winreg.KEY_ALL_ACCESS)
        current_proxy_value, _ = winreg.QueryValueEx(registry_key, PROXY_ENABLE_VALUE)
        proxy_server, _ = winreg.QueryValueEx(registry_key, PROXY_SERVER_VALUE)
        new_proxy_value = 1 - current_proxy_value
        winreg.SetValueEx(registry_key, PROXY_ENABLE_VALUE, 0, winreg.REG_DWORD, new_proxy_value)
        winreg.CloseKey(registry_key)
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, INTERNET_SETTINGS_KEY, 0, winreg.KEY_READ)
        current_proxy_value, _ = winreg.QueryValueEx(registry_key, PROXY_ENABLE_VALUE)
        winreg.CloseKey(registry_key)
        if current_proxy_value == new_proxy_value:
            if current_proxy_value == 1:
                display_message_box(f"Proxy {proxy_server} enabled successfully.",
                                    MESSAGE_BOX_STYLE["MB_INFO"])
            else:
                display_message_box(f"Proxy {proxy_server} disabled successfully.",
                                    MESSAGE_BOX_STYLE["MB_INFO"])
        else:
            action = "disable" if current_proxy_value == 1 else "enable"
            display_message_box(f"Unable to {action} Proxy {proxy_server}",
                                MESSAGE_BOX_STYLE["MB_ERROR"])

    except Exception as e:
        display_message_box(f"Error: {str(e)}",
                            MESSAGE_BOX_STYLE["MB_ERROR"])


def main():
    toggle_proxy_settings()


if __name__ == "__main__":
    main()
