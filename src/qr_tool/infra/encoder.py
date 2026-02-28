from io import StringIO, BytesIO
from qr_tool.core.models import OutputFormat
import segno
from qr_tool.core.models import QRCodeImage


class SegnoEncoderAdapter:
    def __init__(self, scale: int = 10):
        self.scale = scale
        
    def encode_qr(self, payload: str | bytes, format: str) -> QRCodeImage:
        qr = segno.make(payload, micro=False)
        buffer: BytesIO | StringIO
        
        if format == OutputFormat.TXT.value:
            buffer = StringIO()
            qr.terminal(out=buffer)
            return QRCodeImage(data=buffer.getvalue().encode('utf-8'), format=format)
        else:
            buffer = BytesIO()
            qr.save(buffer, kind=format, scale=self.scale)
            return QRCodeImage(data=buffer.getvalue(), format=format)
        