import hashlib
import json
import time
import numpy as np
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class LegalCryptoShield:
    """Blindagem Criptográfica para Evidências Jurídicas."""

    def __init__(self):
        self.aes_key = AESGCM.generate_key(bit_length=256)
        self.aesgcm = AESGCM(self.aes_key)

    def generate_proof(self, device_info: dict, metadata: dict, matrix: np.ndarray) -> dict:
        """Gera assinatura SHA-256 e cifra a evidência mantendo-a na RAM."""
        img_bytes = matrix.tobytes()
        payload = {
            "device": device_info,
            "metadata": metadata,
            "timestamp": time.time()
        }
        
        payload_bytes = json.dumps(payload).encode('utf-8') + img_bytes

        # Assinatura Digital Hash SHA-256
        sha256_hash = hashlib.sha256(payload_bytes).hexdigest()

        # Criptografia Simétrica AES-256-GCM
        nonce = hashlib.sha256(str(time.time()).encode()).digest()[:12]
        encrypted_payload = self.aesgcm.encrypt(nonce, payload_bytes, None)

        return {
            "hash_sha256": sha256_hash,
            "encrypted_bytes_len": len(encrypted_payload),
            "nonce_hex": nonce.hex(),
            "timestamp_str": time.strftime("%Y-%m-%d %H:%M:%S")
        }
