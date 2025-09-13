from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import hashlib
import os

class DataEncryptor:
    """AES-256数据加密处理器"""
    
    def __init__(self, key: bytes = None):
        self.key = key or self.generate_key()
        self.bs = AES.block_size
        
    @staticmethod
    def generate_key() -> bytes:
        """生成随机加密密钥"""
        return get_random_bytes(32)
        
    def encrypt(self, raw_data: bytes) -> dict:
        """加密原始数据"""
        iv = get_random_bytes(self.bs)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        padded = self._pad(raw_data)
        encrypted = cipher.encrypt(padded)
        return {
            'iv': base64.b64encode(iv).decode('utf-8'),
            'ciphertext': base64.b64encode(encrypted).decode('utf-8')
        }
    
    def decrypt(self, enc_data: dict) -> bytes:
        """解密数据"""
        iv = base64.b64decode(enc_data['iv'])
        ciphertext = base64.b64decode(enc_data['ciphertext'])
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(ciphertext)
        return self._unpad(decrypted)
    
    def _pad(self, s: bytes) -> bytes:
        """PKCS#7填充"""
        pad_len = self.bs - len(s) % self.bs
        return s + bytes([pad_len] * pad_len)
        
    @staticmethod
    def _unpad(s: bytes) -> bytes:
        """去除PKCS#7填充"""
        return s[:-s[-1]]

class DataAnonymizer:
    """医疗数据脱敏处理器"""
    
    @staticmethod
    def anonymize_image(image: bytes) -> bytes:
        """图像脱敏处理（保留牙齿区域）"""
        # TODO: 实现基于CV的牙齿区域保留算法
        return image
        
    @staticmethod
    def anonymize_metadata(metadata: dict) -> dict:
        """元数据脱敏"""
        return {
            'age_range': f"{metadata['age']//10*10}-{metadata['age']//10*10+9}",
            'gender': metadata['gender'][0] if metadata['gender'] else 'U',
            'location': metadata['location'][:3] + '****'
        }