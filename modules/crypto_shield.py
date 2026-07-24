# modules/crypto_shield.py
import json
import numpy as np
import builtins

class NumpyEncoder(json.JSONEncoder):
    """
    Encoder customizado para converter objetos do NumPy em tipos JSON serializáveis.
    """
    def default(self, obj):
        if builtins.isinstance(obj, np.ndarray):
            return {
                "shape": builtins.list(obj.shape),
                "dtype": builtins.str(obj.dtype),
                "mean_val": builtins.float(np.mean(obj))
            }
        if builtins.isinstance(obj, np.integer):
            return builtins.int(obj)
        if builtins.isinstance(obj, np.floating):
            return builtins.float(obj)
        return super(NumpyEncoder, self).default(obj)


class CryptoShield:
    def __init__(self):
        pass

    def generate_proof(self, dev_info, ai_res, matrix):
        """
        Gera a prova em bytes garantindo que matrizes numpy não quebrem o json.dumps.
        """
        if builtins.isinstance(matrix, np.ndarray):
            img_bytes = matrix.tobytes()[:1024]
        else:
            img_bytes = b""

        payload = {
            "dev_info": dev_info,
            "ai_res": ai_res,
            "matrix_summary": matrix if not builtins.isinstance(matrix, np.ndarray) else {
                "shape": builtins.list(matrix.shape),
                "dtype": builtins.str(matrix.dtype)
            }
        }

        # Serializa com tratamento seguro
        payload_bytes = json.dumps(payload, cls=NumpyEncoder, ensure_ascii=False).encode('utf-8') + img_bytes
        return payload_bytes
