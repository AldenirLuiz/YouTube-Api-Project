import json


class MyKeys:
    json_file: str = "MyKeys.json"

    @property
    def keychain(self) -> list:
        """Returns: <list of keys from json>"""
        with open(self.json_file, "r", encoding="utf8", errors="ignore") as api_keys:
            keychain = json.load(api_keys)
        return keychain["YouTubeKey"]


if __name__ == "__main__":
    print(MyKeys().keychain)