import cv2
import numpy as np

class UniversalDecoder:
    """Decodificador síncrono para arquivos e fluxos universais de mídia."""

    def __init__(self):
        self.cap = None

    def load_stream_or_device(self, source_input: str | int) -> bool:
        """Carrega streams RTSP, HTTP ou dispositivos USB conectados ao servidor."""
        if self.cap is not None:
            self.cap.release()
        
        # Converte para inteiro se for um ID de câmera USB
        if str(source_input).isdigit():
            source_input = int(source_input)

        self.cap = cv2.VideoCapture(source_input)
        return self.cap.isOpened()

    def load_file_from_bytes(self, file_bytes: bytes, file_extension: str) -> bool:
        """Decodifica arquivos de vídeo enviados de qualquer aparelho via memória RAM."""
        import tempfile
        if self.cap is not None:
            self.cap.release()

        # Cria buffer volátil temporário sem gravar permanentemente no HD
        self.temp_file = tempfile.NamedTemporaryFile(delete=True, suffix=f".{file_extension}")
        self.temp_file.write(file_bytes)
        self.temp_file.flush()
        
        self.cap = cv2.VideoCapture(self.temp_file.name)
        return self.cap.isOpened()

    def get_next_frame(self) -> tuple[bool, np.ndarray | None]:
        """Extrai o próximo frame do arquivo/stream em formato bruto."""
        if self.cap is None or not self.cap.isOpened():
            return False, None

        ret, frame = self.cap.read()
        
        # Se for um arquivo de vídeo e chegar ao fim, reinicia o loop
        if not ret:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.cap.read()

        return ret, frame

    def release(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None
