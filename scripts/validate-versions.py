#!/usr/bin/env python3
"""Reject image drift across local and DigitalOcean release paths."""
import argparse
from pathlib import Path
import re
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]


def validate(check_env=False):
    pin = (ROOT / '.n8n-version').read_text().strip()
    errors = []
    if not re.fullmatch(r'\d+\.\d+\.\d+', pin):
        errors.append('.n8n-version must contain one explicit MAJOR.MINOR.PATCH')
    paths = [ROOT / '.env.example']
    if check_env:
        paths.append(ROOT / '.env')
    for path in paths:
        if not path.exists():
            errors.append(f'{path.name} missing')
            continue
        values = re.findall(r'^N8N_VERSION=(.*)$', path.read_text(), re.M)
        if values != [pin]:
            errors.append(f'{path.name}: N8N_VERSION must match .n8n-version')
    compose = yaml.safe_load((ROOT / 'docker-compose.local.yml').read_text())
    image = compose['services']['n8n'].get('image')
    if image != f'n8nio/n8n:{pin}':
        errors.append('Compose n8n image must use the literal release pin')
    count = 0
    for path in sorted((ROOT / '.do').rglob('*.yaml')):
        spec = yaml.safe_load(path.read_text())
        spec = spec.get('spec', spec)
        found = 0
        for group in ('services', 'workers'):
            for component in spec.get(group, []):
                image = component.get('image', {})
                if image.get('repository') in ('n8n-io/n8n', 'n8n-io/runners'):
                    found += 1
                    count += 1
                    if image.get('tag') != pin:
                        errors.append(f'{path.relative_to(ROOT)}: {component["name"]} image tag must match .n8n-version')
        if not found:
            errors.append(f'{path.relative_to(ROOT)}: no n8n/runner images found')
    if errors:
        raise ValueError('\n'.join(errors))
    return pin, count


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check-env', action='store_true', help='also check local .env version without printing secrets')
    try:
        pin, count = validate(parser.parse_args().check_env)
    except (ValueError, KeyError, TypeError, OSError, yaml.YAMLError) as exc:
        print(f'Version policy failed: {exc}', file=sys.stderr)
        sys.exit(1)
    print(f'Version policy passed: {pin}; Compose and {count} App Platform image references')
