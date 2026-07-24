class DeviceAuthenticator:
    """Gerenciador de Handshake e Autorização de Dispositivos de Ingestão."""

    def __init__(self, authorized_list: list):
        self.authorized_devices = {dev["hardware_token"]: dev for dev in authorized_list}

    def validate_device(self, token: str) -> tuple[bool, str, dict | None]:
        """Verifica se o token do dispositivo está na whitelist antes de aceitar a mídia."""
        clean_token = token.strip()
        if clean_token in self.authorized_devices:
            dev_info = self.authorized_devices[clean_token]
            return True, f"Dispositivo Autorizado: {dev_info['device_name']} [{dev_info['device_id']}]", dev_info
        
        return False, "ACESSO NEGADO: Dispositivo ou Hardware não cadastrado na política de governança.", None
