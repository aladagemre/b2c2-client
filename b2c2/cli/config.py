# -*- coding: utf-8 -*-
import configparser
import logging
import os
from pathlib import Path

from b2c2.common.settings import API_URL


class ConfigManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.config = configparser.ConfigParser()
        self.config_path = str(Path.home() / ".b2c2")

        if not os.path.exists(self.config_path):
            self.config["default"] = {"token": "", "api_url": API_URL}
            self.save_config()

        self.load_config()

    def load_config(self):
        self.config.read(self.config_path)

    def save_config(self):
        with open(self.config_path, "w") as configfile:
            self.config.write(configfile)
            self.logger.info("Config saved")

    def set_config(self, key, value, section="default"):
        self.config.set(section=section, option=key, value=value)

    def get_config(self, key, section="default"):
        return self.config.get(section=section, option=key)

    def get_token(self):
        return self.get_config("token")

    def set_token(self, token):
        self.set_config("token", token)

    def get_api_url(self):
        return self.get_config("api_url")

    def set_api_url(self, api_url):
        self.set_config("api_url", api_url)
