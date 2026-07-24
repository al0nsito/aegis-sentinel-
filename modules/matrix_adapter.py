import cv2
import numpy as np

class DynamicMatrixAdapter:
    """Normalizador de Matrizes Adaptativo sem resolução fixa."""

    def __init__(self, max_side_px: int = 1280):
        self.max_side_px = max_side_px

    def process(self, raw_frame: np.ndarray) -> tuple[np.ndarray, dict]:
        """Preserva a proporção nativa do arquivo/aparelho e normaliza para RGB."""
        h, w = raw_frame.shape[:2]
        
        # Redimensionamento proporcional se o frame for maior que o limite configurado
        if max(h, w) > self.max_side_px:
            scale = self.max_side_px / float(max(h, w))
            new_w = int(w * scale)
            new_h = int(h * scale)
            resized = cv2.resize(raw_frame, (new_w, new_h), interpolation=cv2.INTER_AREA)
        else:
            resized = raw_frame.copy()

        # Conversão de BGR para RGB puro
        rgb_matrix = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
        
        matrix_metadata = {
            "original_resolution": f"{w}x{h}",
            "processed_resolution": f"{rgb_matrix.shape[1]}x{rgb_matrix.shape[0]}",
            "channels": rgb_matrix.shape[2]
        }

        return rgb_matrix, matrix_metadata
