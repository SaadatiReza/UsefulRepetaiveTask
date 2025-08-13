You can configure a V2Ray client on Ubuntu in two main ways:

Method 1: Using the official v2ray core directly with a JSON config file (CLI mode)

Method 2: Using a GUI client (like Qv2ray or V2RayN-Linux) for easier setup

Here’s the step-by-step CLI setup, which is the most stable:

1. Install V2Ray on Ubuntu
bash
Copy
Edit
# Download and install V2Ray via the official script
bash <(curl -L https://raw.githubusercontent.com/v2fly/fhs-install-v2ray/master/install-release.sh)
This will:

Install v2ray binaries to /usr/local/bin/v2ray and /usr/local/bin/v2ctl

Create default config at /usr/local/etc/v2ray/config.json

Set up a systemd service v2ray

2. Edit the V2Ray Client Config
Open the config file:

bash
Copy
Edit
sudo nano /usr/local/etc/v2ray/config.json
Here’s a sample client configuration (VMess protocol example):

```json
{
  "inbounds": [
    {
      "port": 1080,
      "listen": "127.0.0.1",
      "protocol": "socks",
      "settings": {
        "auth": "noauth",
        "udp": true
      }
    }
  ],
  "outbounds": [
    {
      "protocol": "vmess",
      "settings": {
        "vnext": [
          {
            "address": "YOUR_SERVER_IP_OR_DOMAIN",
            "port": 443,
            "users": [
              {
                "id": "YOUR_UUID",
                "alterId": 0,
                "security": "auto"
              }
            ]
          }
        ]
      },
      "streamSettings": {
        "network": "ws",
        "security": "tls",
        "wsSettings": {
          "path": "/YOUR_WS_PATH"
        }
      }
    }
  ]
}
```
🔹 Replace:

YOUR_SERVER_IP_OR_DOMAIN → your V2Ray server address

YOUR_UUID → server-provided UUID

/YOUR_WS_PATH → WebSocket path (if using WS)

3. Start and Enable the Service
bash
Copy
Edit
sudo systemctl start v2ray
sudo systemctl enable v2ray
Check if it’s running:

bash
Copy
Edit
systemctl status v2ray
4. Set Your Apps to Use the Proxy
Now your SOCKS5 proxy is running on:

makefile
Copy
Edit
127.0.0.1:1080
You can:

Configure browsers (Firefox: Preferences → Network Settings → SOCKS5)

Or use a global proxy tool like Proxychains or Clash

Example proxychains config:

bash
Copy
Edit
sudo apt install proxychains4
sudo nano /etc/proxychains4.conf
Add:

nginx
Copy
Edit
socks5 127.0.0.1 1080
Then run:

bash
Copy
Edit
proxychains4 curl ifconfig.me