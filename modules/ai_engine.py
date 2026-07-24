import time
import cv2
import numpy as np

class AdaptiveAIEngine:
    """Core Engine de IA com Early Exit e fatiamento proporcional."""

    def __init__(self):
        pass

    def run_inference(self, matrix: np.ndarray, force_infraction_simulation: bool = False) -> dict:
        start_time = time.perf_counter()
        h, w, _ = matrix.shape

        # 1. MECANISMO EARLY EXIT (<1ms)
        # Analisa o desvio padrão da matriz para detectar presença na cena
        frame_variance = np.std(matrix)
        has_person = frame_variance > 20.0

        if not has_person:
            elapsed = (time.perf_counter() - start_time) * 1000
            return {
                "status": "EARLY_EXIT_EMPTY",
                "latency_ms": elapsed,
                "has_person": False,
                "infraction": False,
                "missing_epi": [],
                "crop": None
            }

        # 2. FATIAMENTO PROPORCIONAL NUMPY (Nível C)
        # Recorta a região de cabeça/ombros adaptando-se a qualquer resolução da matriz
        crop_y1, crop_y2 = int(h * 0.05), int(h * 0.45)
        crop_x1, crop_x2 = int(w * 0.20), int(w * 0.80)
        roi_crop = matrix[crop_y1:crop_y2, crop_x1:crop_x2]

        # 3. INSPEÇÃO DE EPIs (Análise de Cor / Heurística na ROI)
        missing_epi = []
        hsv_crop = cv2.cvtColor(roi_crop, cv2.COLOR_RGB2HSV)
        
        # Filtro para detectar presença de tom de segurança/capacete
        helmet_mask = cv2.inRange(hsv_crop, (10, 80, 80), (35, 255, 255))
        
        if np.sum(helmet_mask) < 300 or force_infraction_simulation:
            missing_epi.append("Capacete de Segurança")

        elapsed = (time.perf_counter() - start_time) * 1000
        infraction = len(missing_epi) > 0

        return {
            "status": "PROCESSED",
            "latency_ms": elapsed,
            "has_person": True,
            "infraction": infraction,
            "missing_epi": missing_epi,
            "crop": roi_crop
        }
