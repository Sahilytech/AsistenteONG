from src.resources_data import RESOURCES_DATABASE, search_resources
from src.reports.report_defaults import ReportDefaults
from src.config_manager import ConfigManager


def test_resources_have_official_sources():
    assert RESOURCES_DATABASE
    assert all(item.get('source', '').startswith('https://') for item in RESOURCES_DATABASE.values())
    assert any(x.get('phone') == '144' for x in search_resources('144'))


def test_report_defaults_roundtrip(tmp_path):
    store = ReportDefaults(tmp_path / 'settings.db')
    saved = store.save({'entidad_emisora': 'Centro Social', 'profesional_referencia': 'Profesional', 'colegiatura': '123', 'destinatario': 'Juzgado'})
    assert store.load() == saved


def test_context_word_does_not_raise_urgency():
    analysis = ConfigManager().analyze('Mi hijo está estudiando y vive conmigo.')
    assert analysis['urgency'] == 'Baja'


def test_accident_context_is_not_automatic_emergency():
    analysis = ConfigManager().analyze('Mi hijo se quemó con la estufa mientras cocinaba.')
    assert analysis['urgency'] in {'Baja', 'Media'}
    assert analysis['classification'] == 'Salud / accidente'
