import pandas as pd

class RAMVault:
    """Cofre em Memória RAM (0% uso de disco rígido)."""

    def __init__(self):
        self.events = []

    def log_event(self, device_name: str, event_type: str, hash_sha256: str, details: str):
        self.events.append({
            "Horário": pd.Timestamp.now().strftime("%H:%M:%S"),
            "Dispositivo": device_name,
            "Tipo": event_type,
            "Hash SHA-256 (Evidência Volátil)": hash_sha256,
            "Detalhes": details
        })

    def get_dataframe(self) -> pd.DataFrame:
        if not self.events:
            return pd.DataFrame(columns=["Horário", "Dispositivo", "Tipo", "Hash SHA-256 (Evidência Volátil)", "Detalhes"])
        return pd.DataFrame(self.events)
