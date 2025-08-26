#!/usr/bin/env python3
"""
协议时序图生成工具
支持各种网络协议的时序图生成和可视化
"""

import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Tuple, Optional
from pathlib import Path
import json

class ProtocolSequenceDiagram:
    """协议时序图生成器"""
    
    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def create_tcp_handshake_diagram(self, filename: str = "tcp_handshake.md"):
        """创建TCP三次握手时序图"""
        mermaid_code = """
```mermaid
sequenceDiagram
    participant Client as 客户端
    participant Server as 服务器
    
    Note over Client,Server: TCP三次握手
    
    Client->>Server: SYN (seq=x)
    Note right of Client: 客户端发送SYN包，序列号为x
    
    Server->>Client: SYN-ACK (seq=y, ack=x+1)
    Note left of Server: 服务器发送SYN-ACK包，序列号为y，确认号为x+1
    
    Client->>Server: ACK (seq=x+1, ack=y+1)
    Note right of Client: 客户端发送ACK包，序列号为x+1，确认号为y+1
    
    Note over Client,Server: 连接建立完成
```
"""
        
        # 保存Mermaid代码
        output_path = self.output_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(mermaid_code)
        
        return str(output_path)
    
    def create_http_request_diagram(self, filename: str = "http_request.md"):
        """创建HTTP请求时序图"""
        mermaid_code = """
```mermaid
sequenceDiagram
    participant Client as 客户端
    participant Server as 服务器
    
    Note over Client,Server: HTTP请求-响应
    
    Client->>Server: GET /index.html HTTP/1.1
    Note right of Client: 客户端发送HTTP GET请求
    
    Server->>Client: HTTP/1.1 200 OK
    Note left of Server: 服务器返回HTTP响应
    
    Server->>Client: Content-Type: text/html
    Note left of Server: 响应头信息
    
    Server->>Client: <html>...</html>
    Note left of Server: 响应体内容
    
    Note over Client,Server: 请求完成
```
"""
        
        # 保存Mermaid代码
        output_path = self.output_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(mermaid_code)
        
        return str(output_path)
    
    def create_tls_handshake_diagram(self, filename: str = "tls_handshake.md"):
        """创建TLS握手时序图"""
        mermaid_code = """
```mermaid
sequenceDiagram
    participant Client as 客户端
    participant Server as 服务器
    
    Note over Client,Server: TLS 1.3握手过程
    
    Client->>Server: ClientHello
    Note right of Client: 支持的密码套件、随机数等
    
    Server->>Client: ServerHello
    Note left of Server: 选择的密码套件、随机数等
    
    Server->>Client: Certificate
    Note left of Server: 服务器证书
    
    Server->>Client: ServerKeyExchange
    Note left of Server: 密钥交换参数
    
    Server->>Client: ServerHelloDone
    Note left of Server: 服务器Hello完成
    
    Client->>Server: ClientKeyExchange
    Note right of Client: 客户端密钥交换
    
    Client->>Server: ChangeCipherSpec
    Note right of Client: 切换到加密模式
    
    Client->>Server: Finished
    Note right of Client: 客户端握手完成
    
    Server->>Client: ChangeCipherSpec
    Note left of Server: 切换到加密模式
    
    Server->>Client: Finished
    Note left of Server: 服务器握手完成
    
    Note over Client,Server: TLS连接建立完成
```
"""
        
        # 保存Mermaid代码
        output_path = self.output_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(mermaid_code)
        
        return str(output_path)
    
    def create_dns_query_diagram(self, filename: str = "dns_query.md"):
        """创建DNS查询时序图"""
        mermaid_code = """
```mermaid
sequenceDiagram
    participant Client as 客户端
    participant LocalDNS as 本地DNS
    participant RootDNS as 根DNS
    participant TLDNS as 顶级域DNS
    participant AuthDNS as 权威DNS
    
    Note over Client,AuthDNS: DNS递归查询过程
    
    Client->>LocalDNS: 查询 www.example.com
    Note right of Client: 客户端发送DNS查询
    
    LocalDNS->>RootDNS: 查询 .com
    Note right of LocalDNS: 查询根DNS服务器
    
    RootDNS->>LocalDNS: 返回.com服务器地址
    Note left of RootDNS: 返回顶级域DNS地址
    
    LocalDNS->>TLDNS: 查询 example.com
    Note right of LocalDNS: 查询顶级域DNS
    
    TLDNS->>LocalDNS: 返回example.com服务器地址
    Note left of TLDNS: 返回权威DNS地址
    
    LocalDNS->>AuthDNS: 查询 www.example.com
    Note right of LocalDNS: 查询权威DNS
    
    AuthDNS->>LocalDNS: 返回IP地址
    Note left of AuthDNS: 返回www.example.com的IP
    
    LocalDNS->>Client: 返回IP地址
    Note right of LocalDNS: 返回最终结果给客户端
    
    Note over Client,AuthDNS: DNS查询完成
```
"""
        
        # 保存Mermaid代码
        output_path = self.output_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(mermaid_code)
        
        return str(output_path)
    
    def create_raft_consensus_diagram(self, filename: str = "raft_consensus.md"):
        """创建Raft共识时序图"""
        mermaid_code = """
```mermaid
sequenceDiagram
    participant Leader as Leader
    participant Follower1 as Follower1
    participant Follower2 as Follower2
    
    Note over Leader,Follower2: Raft共识过程
    
    Leader->>Follower1: AppendEntries RPC
    Note right of Leader: Leader发送日志条目
    
    Leader->>Follower2: AppendEntries RPC
    Note right of Leader: Leader发送日志条目
    
    Follower1->>Leader: AppendEntries Response
    Note left of Follower1: Follower1确认接收
    
    Follower2->>Leader: AppendEntries Response
    Note left of Follower2: Follower2确认接收
    
    Note over Leader,Follower2: 日志复制完成
    
    Leader->>Follower1: Commit Index Update
    Note right of Leader: 更新提交索引
    
    Leader->>Follower2: Commit Index Update
    Note right of Leader: 更新提交索引
    
    Note over Leader,Follower2: 共识达成
```
"""
        
        # 保存Mermaid代码
        output_path = self.output_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(mermaid_code)
        
        return str(output_path)
    
    def create_custom_protocol_diagram(self, protocol_name: str,
                                     steps: List[Dict],
                                     filename: str = "custom_protocol.md"):
        """创建自定义协议时序图"""
        mermaid_code = f"```mermaid\nsequenceDiagram\n"
        mermaid_code += f"    title {protocol_name}协议时序图\n\n"
        
        for step in steps:
            actor1 = step.get('from', 'Client')
            actor2 = step.get('to', 'Server')
            message = step.get('message', 'Message')
            note = step.get('note', '')
            
            mermaid_code += f"    {actor1}->>{actor2}: {message}\n"
            if note:
                mermaid_code += f"    Note right of {actor1}: {note}\n"
        
        mermaid_code += "```\n"
        
        # 保存Mermaid代码
        output_path = self.output_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(mermaid_code)
        
        return str(output_path)
    
    def create_protocol_comparison(self, protocols: Dict[str, List[Dict]],
                                 filename: str = "protocol_comparison.md"):
        """创建协议比较图"""
        mermaid_code = "```mermaid\ngraph TD\n"
        mermaid_code += "    subgraph 协议比较\n"
        
        for protocol_name, steps in protocols.items():
            mermaid_code += f"        subgraph {protocol_name}\n"
            for i, step in enumerate(steps):
                message = step.get('message', f'Step {i+1}')
                mermaid_code += f"            {protocol_name}_Step{i+1}[{message}]\n"
            mermaid_code += "        end\n"
        
        mermaid_code += "    end\n"
        mermaid_code += "```\n"
        
        # 保存Mermaid代码
        output_path = self.output_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(mermaid_code)
        
        return str(output_path)
    
    def create_protocol_state_machine(self, states: List[str],
                                    transitions: List[Tuple[str, str, str]],
                                    filename: str = "protocol_state_machine.md"):
        """创建协议状态机图"""
        mermaid_code = "```mermaid\nstateDiagram-v2\n"
        
        for state in states:
            mermaid_code += f"    {state}\n"
        
        for from_state, to_state, condition in transitions:
            mermaid_code += f"    {from_state} --> {to_state} : {condition}\n"
        
        mermaid_code += "```\n"
        
        # 保存Mermaid代码
        output_path = self.output_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(mermaid_code)
        
        return str(output_path)

def main():
    """主函数 - 示例用法"""
    # 初始化协议时序图生成器
    generator = ProtocolSequenceDiagram()
    
    # 创建TCP握手图
    generator.create_tcp_handshake_diagram()
    
    # 创建HTTP请求图
    generator.create_http_request_diagram()
    
    # 创建TLS握手图
    generator.create_tls_handshake_diagram()
    
    # 创建DNS查询图
    generator.create_dns_query_diagram()
    
    # 创建Raft共识图
    generator.create_raft_consensus_diagram()
    
    # 创建自定义协议图
    custom_steps = [
        {'from': 'Alice', 'to': 'Bob', 'message': 'Hello', 'note': '发送问候'},
        {'from': 'Bob', 'to': 'Alice', 'message': 'Hi', 'note': '回复问候'},
        {'from': 'Alice', 'to': 'Bob', 'message': 'How are you?', 'note': '询问状态'},
        {'from': 'Bob', 'to': 'Alice', 'message': 'Fine, thanks!', 'note': '回复状态'}
    ]
    generator.create_custom_protocol_diagram("问候协议", custom_steps)
    
    # 创建协议比较
    protocols = {
        'TCP': [
            {'message': 'SYN'},
            {'message': 'SYN-ACK'},
            {'message': 'ACK'}
        ],
        'UDP': [
            {'message': 'Data'},
            {'message': 'No ACK'}
        ]
    }
    generator.create_protocol_comparison(protocols)
    
    # 创建状态机
    states = ['Idle', 'Connecting', 'Connected', 'Disconnecting']
    transitions = [
        ('Idle', 'Connecting', 'connect()'),
        ('Connecting', 'Connected', 'connection established'),
        ('Connected', 'Disconnecting', 'disconnect()'),
        ('Disconnecting', 'Idle', 'disconnection complete')
    ]
    generator.create_protocol_state_machine(states, transitions)
    
    print("协议时序图生成完成！输出文件保存在 output/ 目录中。")

if __name__ == "__main__":
    main()
