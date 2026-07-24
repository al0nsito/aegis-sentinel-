import json
import numpy as np

def generate_proof(dev_info, ai_res, matrix):
    # Trata matrizes de imagem/vídeo para não dar erro de JSON
    if isinstance(matrix, np.ndarray):
        matrix_payload = {
            "shape": list(matrix.shape),
            "dtype": str(matrix.dtype),
            "mean_val": float(np.mean(matrix))
        }
    else:
        matrix_payload = str(matrix)

    payload = {
        "device_info": dev_info,
        "analysis_result": ai_res,
        "telemetry_matrix": matrix_payload
    }

    return json.dumps(payload, ensure_ascii=False).encode('utf-8')
