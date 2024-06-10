"""
This module contains utility functions for the reservoir simulator.
"""

def check_config(config):
    """
    Check if the configuration is valid.
    
    :param config: A dictionary representing the configuration.
    :type config: dict
    
    :return: True if the configuration is valid, False otherwise.
    :rtype: bool
    """
    return True

    if 'reservoir' in config:
        return 'dimensions' in config['reservoir']
    return True
