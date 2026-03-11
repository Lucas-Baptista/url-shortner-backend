from datetime import datetime


class UrlEntity:
    def __init__(
        self,
        short_code: str,
        original_url: str,
        created_at: datetime
    ):
        self.short_code = short_code
        self.original_url = original_url
        self.created_at = created_at

    def to_dict(self):
        return {
            "short_code": self.short_code,
            "original_url": self.original_url,
            "created_at": self.created_at
        }