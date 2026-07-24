import cv2
import numpy as np

class AgnosticHardwareConnector:
    def __init__(self, mode="synthetic"):
        self.mode = mode

    def get_synthetic_frame(self, simulate_person=True, simulate_infraction=False) -> np.ndarray:
        """Gera um frame em matriz BGR puro na memória RAM para testes de bancada."""
        # Cria matriz 640x640 com fundo escuro
        frame = np.zeros((640, 640, 3), dtype=np.uint8) + 40
        
        if simulate_person:
            # Desenha um operador sintético
            cv2.rectangle(frame, (200, 150), (440, 550), (200, 200, 200), -1) # Corpo
            cv2.circle(frame, (320, 220), 60, (180, 180, 180), -1) # Cabeça
            
            # Simula EPIs
            if not simulate_infraction:
                # Capacete Verde (Conforme)
                cv2.ellipse(frame, (320, 190), (65, 30), 0, 180, 360, (0, 255, 0), -1)
            else:
                # Sem Capacete / Alerta Vermelho visual no teste
                cv2.putText(frame, "SEM CAPACETE", (220, 120), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                
        return frame
