"""
ConfigManager — 配置檔案管理器
負責讀取和寫入 config.json
"""

import json
import os


class ConfigManager:
    """管理應用程式配置"""

    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        self._config = self._load_config()

    def _load_config(self):
        """載入配置檔案"""
        if not os.path.exists(self.config_path):
            return self._get_default_config()

        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"載入配置檔案失敗：{e}")
            return self._get_default_config()

    def _get_default_config(self):
        """預設配置"""
        return {
            "app_name": "Wani-Doko! ワニどこ!",
            "window_width": 900,
            "window_height": 650,
            "quiz_question_count": 10,
            "weak_word_threshold": 2,
            "unlock_score_percent": 80,
            "csv_encoding": "utf-8",
            "custom_background": None
        }

    def get(self, key, default=None):
        """取得配置值"""
        return self._config.get(key, default)

    def set(self, key, value):
        """設定配置值並儲存"""
        self._config[key] = value
        self._save_config()

    def _save_config(self):
        """儲存配置到檔案"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"儲存配置檔案失敗：{e}")

    def set_custom_background(self, background_name):
        """設定自訂背景"""
        self.set("custom_background", background_name)

    def get_custom_background(self):
        """取得自訂背景"""
        return self.get("custom_background")

    def clear_custom_background(self):
        """清除自訂背景（使用預設）"""
        self.set("custom_background", None)
