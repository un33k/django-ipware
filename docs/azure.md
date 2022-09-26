# Azure Application Gateway

If you use an Azure application gateways as a reverse proxy for your application the `HTTP_X_FORWARDED_FOR` header can be set using the IPv4 including a "random" port number - this for some reason does not happen on all requests


## Sample Headers

```
{
    "REMOTE_ADDR": "192.168.50.44",
    "HTTP_X_REAL_IP": "10.0.0.6",
    "HTTP_X_FORWARDED_FOR": "177.139.233.139:17085, 10.0.0.6"
}
```

## References

* https://learn.microsoft.com/en-gb/azure/application-gateway/rewrite-http-headers-url#remove-port-information-from-the-x-forwarded-for-header