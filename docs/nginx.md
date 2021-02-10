### Nginx Users

By default,using Ningx as a reverse proxy to Gunicorn doesn't forward the client's IP to gunicorn. 
As a reverse proxy, NGINX will receive HTTP requests from clients and then send those requests to our
Gunicorn WSGI server. The problem is that NGINX hides information from our WSGI server. 
The HTTP request that Gunicorn receives is not the same as the one that NGINX received from the client.
To solve this problem, open up your `nginx conf file` and add the following lines to the `location` block
```
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header Host $host;
proxy_set_header X-Forwarded-Proto $scheme;
```

```
server {
    listen 80;
    location / {
        include proxy_params;
        proxy_pass http://unix:/<where_your_sock_file_is>/coincard.sock;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

```