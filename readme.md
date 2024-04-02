
# Run

Commands for docker compose to run and test application.

```bash
sudo docker-compose build

sudo docker-compose up -d app

sudo docker-compose down

docker-compose logs app | tail -100
```


# DB

Connect to db at localhost:54321 in dbeaver-ce
Also, make sure to set to show all databases.
![img.png](img.png)
![img_1.png](img_1.png)


# Judge0 

Dummy https://ce.judge0.com/dummy-client.html

Run judge0
docker-compose up -d
docker-compose up -d db redis

Send requests to http://localhost:2358 or wherever judge0 runs

Supported languages
```angular2html
curl 192.168.0.220:2358/languages | jq | less
```