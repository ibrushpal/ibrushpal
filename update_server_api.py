import paramiko
from scp import SCPClient
import os

def update_server_api():
    """更新服务器上的API文件"""
    # 服务器连接信息
    hostname = "42.194.142.158"
    username = "ubuntu"
    # 注意：在实际使用中，密码或密钥应该从安全的地方获取
    # 这里使用密钥文件方式更安全
    
    try:
        # 创建SSH客户端
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # 连接到服务器（这里需要配置正确的认证方式）
        # ssh.connect(hostname, username=username, password=your_password)
        # 或者使用密钥文件
        # ssh.connect(hostname, username=username, key_filename=path_to_private_key)
        
        print("✅ 连接到服务器成功")
        
        # 使用SCP传输文件
        with SCPClient(ssh.get_transport()) as scp:
            # 上传修复后的API文件
            scp.put('teeth_detection_api.py', '/home/ubuntu/ibrushpal/teeth_detection_api.py')
            print("✅ API文件上传成功")
            
            # 重启服务
            stdin, stdout, stderr = ssh.exec_command('cd /home/ubuntu/ibrushpal && sudo systemctl restart ibrushpal-api')
            print("✅ 服务重启命令执行")
            
            # 检查服务状态
            stdin, stdout, stderr = ssh.exec_command('sudo systemctl status ibrushpal-api')
            status_output = stdout.read().decode()
            print("服务状态:", status_output)
            
    except Exception as e:
        print(f"❌ 更新失败: {e}")
    
    finally:
        if ssh:
            ssh.close()

def manual_update_instructions():
    """提供手动更新说明"""
    print("\n📋 手动更新说明:")
    print("1. 连接到服务器: ssh ubuntu@42.194.142.158")
    print("2. 备份当前文件: cp /home/ubuntu/ibrushpal/teeth_detection_api.py /home/ubuntu/ibrushpal/teeth_detection_api.py.backup")
    print("3. 使用scp上传新文件（从本地）:")
    print("   scp teeth_detection_api.py ubuntu@42.194.142.158:/home/ubuntu/ibrushpal/")
    print("4. 重启服务: sudo systemctl restart ibrushpal-api")
    print("5. 检查状态: sudo systemctl status ibrushpal-api")

if __name__ == "__main__":
    print("服务器API更新工具")
    print("=" * 50)
    
    # 由于安全原因，自动更新需要配置认证信息
    # update_server_api()
    
    manual_update_instructions()