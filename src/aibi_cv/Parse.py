import json


class Parse:
    @staticmethod
    def parse(data: str) -> tuple:
        """Parse barcode text into (name, value).

        Tries JSON first, then `name:value` format, otherwise returns (None, data).
        """
        try:
            json_data = json.loads(data)
            if isinstance(json_data, dict):
                for key, value in json_data.items():
                    return key, str(value)
        except Exception:
            pass

        if ":" in data:
            parts = data.split(":", 1)
            return parts[0].strip(), parts[1].strip()
        return None, data
