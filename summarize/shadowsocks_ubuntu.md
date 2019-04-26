(https://www.jianshu.com/p/41378f4e14bc)
su
pip install shadowsocks
vi /etc/shadowsocks.json  # add 
{
"server": "your_server_ip",  # ss服务器IP
"server_port": "your_server_port",  # 端口
"local_address": "127.0.0.1",  # 本地ip
"local_port": 1080,  # 本地端口
"password": "your_server_passwd",  # 连接ss密码
"timeout": 300,  # 等待超时
"method": "aes-256-cfb",  # 加密方式
"fast_open": true,  # true 或 false。如果你的服务器 Linux 内核在3.7+，可以开启 fast_open 以降低延迟。开启方法： echo 3 > /proc/sys/net/ipv4/tcp_fastopen 开启之后，将 fast_open 的配置设置为 true 即可
"workers": 1  # 工作线程数
}
sslocal -c /etc/shadowsocks.json  # start
or nohup sslocal -c /etc/shadowsocks.json /dev/null 2>&1 &
(if cannot start,vi /usr/local/lib/python2.7/dist-packages/shadowsocks/crypto/openssl.py, replace cleanup to reset)

firefox proxy:
 SOCKS Host 127.0.0.1:1080
 SOCKS_v5
 Proxy DNS when using SOCKS v5(others are all empty)
