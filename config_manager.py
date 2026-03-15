import yaml
import os
from pathlib import Path
from typing import Any, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class ConfigManager:
    """設定管理器 - 讀取與管理 config.yaml"""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """載入 YAML 設定檔"""
        if not self.config_path.exists():
            logger.error(f"設定檔不存在: {self.config_path}")
            raise FileNotFoundError(f"設定檔不存在: {self.config_path}")
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                logger.info(f"成功載入設定檔: {self.config_path}")
                return config if config else {}
        except yaml.YAMLError as e:
            logger.error(f"YAML 解析錯誤: {e}")
            raise
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        取得設定值 (支援點符號路徑)
        例如: config.get('screening_thresholds.min_volume')
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        
        return value
    
    def get_api_endpoints(self) -> Dict[str, str]:
        """取得所有 API 端點"""
        return self.config.get('api_endpoints', {})
    
    def get_data_parameters(self) -> Dict[str, Any]:
        """取得資料參數"""
        return self.config.get('data_parameters', {})
    
    def get_screening_thresholds(self) -> Dict[str, float]:
        """取得篩選閾值"""
        return self.config.get('screening_thresholds', {})
    
    def get_all_config(self) -> Dict[str, Any]:
        """取得整個設定字典"""
        return self.config

# 使用範例
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    config = ConfigManager()
    print(f"最低成交張數: {config.get('screening_thresholds.min_volume')}")
    print(f"API 端點: {config.get_api_endpoints()}")