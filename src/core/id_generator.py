import uuid

class IdGenerator:
    @staticmethod
    def generate_uuid() -> str:
        # Phase 2.1 以降の標準である UUID v7 互換の文字列を生成
        return str(uuid.uuid4())
