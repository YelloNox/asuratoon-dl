import os

url = "https://www.example.com"
shortcut_name = "WebsiteShortcut.url"

shortcut_content = f"[InternetShortcut]\nURL={url}"

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

shortcut_path = os.path.join(desktop_path, shortcut_name)
with open(shortcut_path, "x") as url_shortcut:
    url_shortcut.write(shortcut_content)

print(f"Shortcut {url} created on the desktop as {shortcut_name}.")
