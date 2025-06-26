# From LP305 to RM-01 through NginX

## 安装

## 更新apt-get源
`sudo apt-get update`

## 安装
`sudo apt-get install nginx`

## 安装后将自动开启nginx服务，打开浏览器输入ip即可查看初始页面

## 编辑Nginx配置文件：

`sudo nano /etc/nginx/sites-available/default`

## 编辑Nginx配置文件：

```
server {
      listen 40800;
      server_name _;

      location / {
          proxy_pass http://10.10.99.99:40800;
          proxy_set_header Host $host;
          proxy_set_header X-Real-IP $remote_addr;
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
          proxy_set_header X-Forwarded-Proto $scheme;
      }
  }

  server {
      listen 9998;
      server_name _;

      location / {
          proxy_pass http://10.10.99.99:9998;
          proxy_set_header Host $host;
          proxy_set_header X-Real-IP $remote_addr;
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
          proxy_set_header X-Forwarded-Proto $scheme;
      }
  }
  
    server {
      listen 3210;
      server_name _;

      location / {
          proxy_pass http://10.10.99.99:3210;
          proxy_set_header Host $host;
          proxy_set_header X-Real-IP $remote_addr;
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
          proxy_set_header X-Forwarded-Proto $scheme;
      }
  }
  
    server {
      listen 8000;
      server_name _;

      location / {
          proxy_pass http://10.10.99.98:8000;
          proxy_set_header Host $host;
          proxy_set_header X-Real-IP $remote_addr;
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
          proxy_set_header X-Forwarded-Proto $scheme;
      }
  }
```
  
## 重启Nginx：
  
`sudo systemctl restart nginx`
  
## 修改Nginx文件大小
  
```
  http {
    # ... 其他配置 ...

    client_max_body_size 100M; # 全局设置
```
    
## 重启NginX配置

`sudo nginx -s reload`

## 启用流式转发

## 不缓存，支持流式输出
```
    proxy_cache off;  # 关闭缓存
    proxy_buffering off;  # 关闭代理缓冲
    chunked_transfer_encoding on;  # 开启分块传输编码
    tcp_nopush on;  # 开启TCP NOPUSH选项，禁止Nagle算法
    tcp_nodelay on;  # 开启TCP NODELAY选项，禁止延迟ACK算法
    keepalive_timeout 300;  # 设定keep-alive超时时间为65秒
```
