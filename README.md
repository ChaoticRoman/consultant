# WhatsApp Bot with OpenAI integration

The process was tested on Ubuntu 24.04.2 LTS (GNU/Linux 6.8.0-1026-oracle x86_64).

## Dependencies

```
sudo apt update
sudo apt upgrade
sudo apt install supervisor python3-pip nginx certbot python3-certbot-nginx logrotate
sudo pip install --break-system-packages openai "fastapi[standard]"
```

## Setup

### Firewall

```
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 80 -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport <RANDOM HIGH TLS PORT> -j ACCEPT
sudo netfilter-persistent save
```

### Nginx and TLS

```
sudo certbot --nginx
sudo nano /etc/nginx/sites-available/default
```

### Supervisor

```
sudo ln -s `pwd`/supervisor.conf /etc/supervisor/conf.d/consultant.conf
sudo systemctl enable supervisor
sudo systemctl start supervisor
```

### Logrotate

```
sudo ln -s `pwd`/logrotate.conf /etc/logrotate.d/consultant
```

### Meta WhatsApp

* We need long-lived System User Access Tokens

## Resources

* https://github.com/daveebbelaar/python-whatsapp-bot
* https://dev.to/armiedema/opening-up-port-80-and-443-for-oracle-cloud-servers-j35
* https://dylancastillo.co/posts/fastapi-nginx-gunicorn.html
* https://stackoverflow.com/questions/61153498/what-is-the-good-way-to-provide-an-authentication-in-fastapi
* https://stackoverflow.com/questions/75422064/validate-x-hub-signature-256-meta-whatsapp-webhook-request
* https://stackoverflow.com/a/75469968/12118546
* https://fastapi.tiangolo.com/tutorial/query-params-str-validations/?h=alias#alias-parameters
* https://developers.facebook.com/docs/whatsapp/business-management-api/get-started#system-user-access-tokens

## Talk about this

I have talked about this project on [May 2025 Brno Pyvo](https://pyvo.cz/brno-pyvo/2025-05/). 

[Google slides are available here.](https://docs.google.com/presentation/d/1s9HdK1kzuwCxpKui1C0Bo6DW5CpoPMqhAakbWvJIWdg/)
