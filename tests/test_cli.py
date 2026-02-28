from click.testing import CliRunner
from qr_tool.cli.main import run
from pathlib import Path

def test_encode_cli_output():
    runner = CliRunner()
    
    with runner.isolated_filesystem():
        raw_string_qr_path = 'output_qr_string.png'
        raw_string_qr = runner.invoke(run, ['encode', '--output', raw_string_qr_path, '--payload', 'Hello World'])
        
        assert raw_string_qr.exit_code == 0
        assert "Generating QR code..." in raw_string_qr.output
        assert Path(raw_string_qr_path).exists()
        
        binary_qr_path = 'binary.png'
        binary_qr = runner.invoke(run, ['encode', '--output', binary_qr_path, '--file', raw_string_qr_path])
        
        assert binary_qr.exit_code == 0
        assert "Generating QR code..." in binary_qr.output
        assert Path(binary_qr_path).exists()
        
        pipe_input_qr_path = 'pipe_input.png'
        pipe_input_qr = runner.invoke(run, ['encode', '--output', pipe_input_qr_path], input='This is a secret message')
        
        assert pipe_input_qr.exit_code == 0
        assert "Generating QR code..." in pipe_input_qr.output
        assert Path(pipe_input_qr_path).exists()
    
def test_decode_cli_output():
    runner = CliRunner()
    test_raw_string_qr_path = 'tests/fixtures/sample_qr.png'
    result = runner.invoke(run, ['decode', test_raw_string_qr_path])
    
    assert result.exit_code == 0
    assert "Decoding QR code..." in result.output
    assert "Decoded result: Hello World" in result.output
    
    test_binary_qr_path = 'tests/fixtures/sample_binary_qr.png'
    binary_qr = runner.invoke(run, ['decode', test_binary_qr_path])
    
    assert binary_qr.exit_code == 0
    assert "Decoding QR code..." in binary_qr.output
    assert "Decoded result: [Binary Data Detected: 496 bytes]" in binary_qr.output