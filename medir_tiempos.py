"""Mide peticiones reales con reloj monotónico, sin inventar resultados."""
import argparse
import csv
from datetime import datetime, timezone
import json
from pathlib import Path
from time import perf_counter
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent


def medir(base_url, output, allow_local=False):
    parsed = urlparse(base_url)
    if not (parsed.scheme == 'https' and parsed.hostname and parsed.hostname.endswith('.onrender.com')):
        if not (allow_local and parsed.scheme == 'http' and parsed.hostname in {'localhost', '127.0.0.1'}):
            raise ValueError('Usa la URL HTTPS real de Render (o --local para comprobaciones locales).')
    sample = json.loads((ROOT / 'ejemplo_peticion.json').read_text(encoding='utf-8'))
    tests = [('GET', '/', None)] + [('POST', '/predict', sample) for _ in range(4)]
    output.mkdir(parents=True, exist_ok=True)
    results = []
    for i, (method, endpoint, body) in enumerate(tests, 1):
        data = json.dumps(body).encode('utf-8') if body is not None else None
        req = Request(base_url.rstrip('/') + endpoint, data=data, method=method,
                      headers={'Content-Type': 'application/json', 'User-Agent': 'Carlos-Casal-P2'})
        start = perf_counter()
        status, error, response_body = None, '', ''
        try:
            with urlopen(req, timeout=120) as response:
                status = response.status
                response_body = response.read().decode('utf-8')
        except HTTPError as exc:
            status, error = exc.code, str(exc)
            response_body = exc.read().decode('utf-8', errors='replace')
        except (URLError, TimeoutError) as exc:
            error = str(exc)
        elapsed = perf_counter() - start
        try:
            parsed_body = json.loads(response_body)
            valid = isinstance(parsed_body, dict) and (
                parsed_body.get('status') == 'ok' if method == 'GET' else
                isinstance(parsed_body.get('predictions'), list) and len(parsed_body['predictions']) == 1)
        except (ValueError, TypeError):
            valid = False
        result = {'peticion': i, 'metodo': method, 'endpoint': endpoint, 'estado_http': status,
                  'tiempo_s': round(elapsed, 6), 'respuesta_valida': valid, 'error': error}
        results.append(result)
        (output / f'respuesta_{i}.txt').write_text(response_body or error, encoding='utf-8')
        print(result)
    with (output / 'tiempos.csv').open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys()); writer.writeheader(); writer.writerows(results)
    metadata = {'autor': 'Carlos Casal P2', 'url': base_url, 'tipo': 'local' if allow_local else 'Render',
                'fecha_utc': datetime.now(timezone.utc).isoformat(), 'peticiones': results}
    (output / 'tiempos.json').write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding='utf-8')
    if not all(r['estado_http'] == 200 and r['respuesta_valida'] for r in results):
        raise RuntimeError('Hay peticiones fallidas; no presentar esta ejecución como prueba satisfactoria.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('url'); parser.add_argument('--salida', type=Path, default=ROOT / 'evidencias')
    parser.add_argument('--local', action='store_true')
    args = parser.parse_args()
    medir(args.url, args.salida, args.local)
