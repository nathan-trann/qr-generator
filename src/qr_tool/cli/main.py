from qr_tool.core.models import DecodedPayloadEnum
import sys
from io import BytesIO
from qr_tool.core.models import OutputFormat
from qr_tool.core.engine import decode_qr_code
from qr_tool.infra.decoder import PyZbarDecoderAdapter
from qr_tool.core.exceptions import PayloadTooLargeError
from qr_tool.core.engine import generate_qr_code
from qr_tool.infra.encoder import SegnoEncoderAdapter
import click


@click.group()
@click.option("--verbose", is_flag=True, help="Enable verbose output.")
@click.version_option(version="0.1.0", prog_name="qr_generator")
@click.pass_context
def run(ctx: click.Context, verbose: bool):
    ctx.ensure_object(dict)
    ctx.obj['VERBOSE'] = verbose
    
    if verbose:
        click.secho('Verbose mode is on', fg='yellow')
        

@run.command('encode')
@click.option("-p", "--payload", type=str, help="A literal string to encode")
@click.option("-f", "--file", type=click.File('rb'), help="Read payload froma file.")
@click.option("-o", "--output", type=click.Path(dir_okay=False, writable=True), help="Path to save the generated QR code image (e.g., output.png)")
@click.pass_context
def encode(ctx: click.Context, payload: str | None, file: BytesIO | None,  output: str | None):
    verbose = ctx.obj.get('VERBOSE', False)
    
    if verbose:
        click.secho(f'Encoding payload: {payload}', fg='green')
    
    raw_data: str | bytes
    
    if file:
        raw_data = file.read()
    elif payload:
        raw_data = payload
    elif not sys.stdin.isatty():
        raw_data = sys.stdin.buffer.read()
    else:
        raise click.UsageError("You must provide data via --payload, --file, or pipe it via stdin.")
    
    click.echo("Generating QR code...")
    
    adapter = SegnoEncoderAdapter()
    
    if output is None:
        result_model = generate_qr_code(raw_data, OutputFormat.TXT.value, encoder=adapter)
        click.echo(result_model.data.decode('utf-8'))
    else:
        try:
            result_model = generate_qr_code(raw_data, OutputFormat.PNG.value, encoder=adapter)
            with open(output, "wb") as f:
                f.write(result_model.data)
            click.secho(f"Successfully generated {output}", fg="green")
        except PayloadTooLargeError as e:
            click.secho(f"Error: {e}", fg="red")
            return
    
    
    
@run.command('decode')
@click.argument("image_path", type=click.Path(exists=True, dir_okay=False, readable=True))
@click.pass_context
def decode(ctx: click.Context, image_path: str):
    verbose = ctx.obj.get('VERBOSE', False)
    
    if verbose:
        click.secho(f'Decoding image: {image_path}', fg='green')
    
    click.echo("Decoding QR code...")
    
    adapter = PyZbarDecoderAdapter()
    
    try:
        with open(image_path, "rb") as f:
            image_data = f.read()
        result_model = decode_qr_code(image_data, adapter)
        if result_model.type == DecodedPayloadEnum.TEXT:
            click.secho(f"Decoded result: {result_model.text}", fg="green")
        else:
            click.secho(f"Decoded result: [Binary Data Detected: {len(result_model.raw_bytes)} bytes]", fg="green")
    except PayloadTooLargeError as e:
        click.secho(f"Error: {e}", fg="red")
        return
    
    

if __name__ == "__main__":
    run(obj={})
