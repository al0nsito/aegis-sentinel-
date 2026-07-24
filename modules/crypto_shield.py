# modules/crypto_shield.py
import json
import numpy as np

class NumpyEncoder(json.JSONEncoder):
    """
    Classe customizada para serializar objetos do NumPy (ndarrays, int64, float32, etc.)
    diretamente para formato JSON sem estourar TypeError.
    """
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return {
                "shape": list(obj.shape),
                "dtype": str(obj.dtype),
                "mean_val": float(np.mean(obj))
            }
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        return super(NumpyEncoder, self).default(obj)


class CryptoShield:
    def __init__(self):
        pass

    def generate_proof(self, dev_info, ai_res, matrix):
        """
        Gera a prova de integridade/auditoria tratando matrizes de vídeo/imagem
        e dicionários de telemetria sem erro de serialização JSON.
        """
        # Garante a extração de bytes de imagem caso a matriz seja fornecida
        if isinstance(matrix, np.ndarray):
            img_bytes = matrix.tobytes()[:1024]  # Amostra de bytes da imagem
        else:
            img_bytes = b""

        payload = {
            "dev_info": dev_info,
            "ai_res": ai_res,
            "matrix_summary": matrix if not isinstance(matrix, np.ndarray) else {
                "shape": list(matrix.shape),
                "dtype": str(matrix.dtype)
            }
        }

        # Serializa utilizando o encoder seguro do NumPy
        payload_bytes = json.dumps(payload, cls=NumpyEncoder, ensure_ascii=False).encode('utf-8') + img_bytes
        return payload_bytes
