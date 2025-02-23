# WhatsApp Bot with OpenAI integration

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

## Resources

* https://github.com/daveebbelaar/python-whatsapp-bot
* https://dev.to/armiedema/opening-up-port-80-and-443-for-oracle-cloud-servers-j35
* https://dylancastillo.co/posts/fastapi-nginx-gunicorn.html
* https://stackoverflow.com/questions/61153498/what-is-the-good-way-to-provide-an-authentication-in-fastapi
* https://stackoverflow.com/questions/75422064/validate-x-hub-signature-256-meta-whatsapp-webhook-request
* https://stackoverflow.com/a/75469968/12118546
* https://fastapi.tiangolo.com/tutorial/query-params-str-validations/?h=alias#alias-parameters
