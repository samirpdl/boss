''' Unit tests for boss.config module. '''

from boss.constants import DEFAULT_CONFIG, PRESET_WEB
from boss.config import (
    merge_config,
    get_deployment_preset
)


def test_get_deployment_preset_returns_configured_preset():
    '''
    Check get_deployment_preset() function returns
    the configured deployment preset if it is configured.
    '''
    raw_config = {
        'deployment': {
            'preset': 'test-preset'
        }
    }
    preset = get_deployment_preset(raw_config)

    assert preset == 'test-preset'


def test_get_deployment_preset_returns_default_preset_if_not_set():
    '''
    Check get_deployment_preset() function returns,
    the default deployment preset if it is not configured.
    '''
    raw_config = {
        'project_name': 'test-project'
    }
    preset = get_deployment_preset(raw_config)

    assert preset == DEFAULT_CONFIG['deployment']['preset']


def test_merge_config_that_default_config_values_are_put():
    '''
    Ensure default values are put if config options are not provided.
    '''
    raw_config = {}
    result = merge_config(raw_config)

    assert result['user'] == DEFAULT_CONFIG['user']
    assert result['port'] == DEFAULT_CONFIG['port']
    assert result['deployment'] == DEFAULT_CONFIG['deployment']
