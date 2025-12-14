import os

content = "GOOGLE_API_KEY=AIzaSyCo7gTwRgEefmixVPBnPmdyVT4g-QYmIDE"
with open(".env", "w", encoding="utf-8") as f:
    f.write(content)
print("Rewrote .env in UTF-8")
