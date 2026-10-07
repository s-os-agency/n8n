import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('version_policy', ROOT / 'scripts/validate-versions.py')
policy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(policy)


class VersionPolicyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        for name in ('.n8n-version', '.env.example', 'docker-compose.local.yml'):
            shutil.copyfile(ROOT / name, self.root / name)
        shutil.copytree(ROOT / '.do', self.root / '.do')
        self.original_root = policy.ROOT
        policy.ROOT = self.root

    def tearDown(self):
        policy.ROOT = self.original_root
        self.temp.cleanup()

    def replace(self, path, old, new):
        p = self.root / path
        p.write_text(p.read_text().replace(old, new))

    def test_aligned_configuration_passes(self):
        self.assertEqual(policy.validate()[0], (ROOT / '.n8n-version').read_text().strip())

    def test_floating_env_is_rejected(self):
        pin = (self.root / '.n8n-version').read_text().strip()
        self.replace('.env.example', f'N8N_VERSION={pin}', 'N8N_VERSION=latest')
        with self.assertRaisesRegex(ValueError, 'N8N_VERSION'):
            policy.validate()

    def test_compose_shell_override_is_rejected(self):
        pin = (self.root / '.n8n-version').read_text().strip()
        self.replace('docker-compose.local.yml', f'n8nio/n8n:{pin}', 'n8nio/n8n:${N8N_VERSION}')
        with self.assertRaisesRegex(ValueError, 'literal release pin'):
            policy.validate()

    def test_runner_drift_is_rejected(self):
        p = self.root / '.do/examples/with-runners.yaml'
        pin = (self.root / '.n8n-version').read_text().strip()
        s = p.read_text()
        start = s.index('repository: n8n-io/runners')
        p.write_text(s[:start] + s[start:].replace(f'tag: "{pin}"', 'tag: "9.9.9"'))
        with self.assertRaisesRegex(ValueError, 'n8n-runner'):
            policy.validate()

    def test_new_template_with_floating_tag_is_rejected(self):
        (self.root / '.do/examples/new.yaml').write_text('services:\n  - name: extra\n    image:\n      repository: n8n-io/n8n\n      tag: latest\n')
        with self.assertRaisesRegex(ValueError, 'new.yaml'):
            policy.validate()

    def test_private_env_drift_is_rejected_without_leaking_values(self):
        (self.root / '.env').write_text('N8N_VERSION=latest\nPOSTGRES_PASSWORD=private-fixture\n')
        with self.assertRaisesRegex(ValueError, '.env: N8N_VERSION') as caught:
            policy.validate(check_env=True)
        self.assertNotIn('private-fixture', str(caught.exception))


if __name__ == '__main__':
    unittest.main()
