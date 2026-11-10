## Jenkins
Запуск контейнера на порту 8080 командой: 

`docker run -d --name jenkins   -p 8080:8080 -p 50000:50000   -v jenkins_home:/var/jenkins_home   -v /srv/git:/srv/git:ro   --restart unless-stopped   jenkins/jenkins:lts`


<img width="272" height="161" alt="image" src="https://github.com/user-attachments/assets/afd2e1b3-3d9b-40c2-b476-b816fbffba51" />

Рис. 1 - Указанные креды в настройках Jenkins

<img width="372" height="135" alt="image" src="https://github.com/user-attachments/assets/0430104c-5126-4dc2-afc1-cbdcf97ad9b9" />

Рис. 2 - Использование общей директории для трех джобов

<img width="380" height="374" alt="image" src="https://github.com/user-attachments/assets/546d3c91-40d2-4f23-b6e5-58e07dcb9dff" />

Рис. 3 - Указание Git-репозитория

<img width="362" height="145" alt="image" src="https://github.com/user-attachments/assets/47f7f2e2-e994-4593-b36c-a5819bf41117" />

Рис. 4 - Настроенный запуск по триггеру - проверка раз в 5 минут на наличие изменения указанного репозитория


**Job 2** - Удаление файла из локального репозитория. Директория указана та же, что в Job 1.


<img width="503" height="207" alt="image" src="https://github.com/user-attachments/assets/0e136583-0b2c-47e0-a2ab-de0d4f4d8c8a" />

Рис. 5 - Настроенный триггер после успешной сработки Job 1

<img width="319" height="212" alt="image" src="https://github.com/user-attachments/assets/f8ec3e44-1608-4bea-a8ed-2190478057fc" />

Рис. 6 - Выполнение команд на удаление файла и проверки содержания локального репозитория


**Job 3** - Восстановление файлов до последней закоммиченной версии. Директория указана та же, что в Job 1.


<img width="494" height="196" alt="image" src="https://github.com/user-attachments/assets/25c8125d-8638-4ed5-af41-c90c49392b4d" />

Рис. 7 - Настроенный триггер после успешной сработки Job 2

<img width="329" height="220" alt="image" src="https://github.com/user-attachments/assets/ab843807-376a-47e0-8b09-04347ddbd366" />

Рис. 8 - Выполнение команд на восстановление локального репозитория до последней закоммиченной версии и проверка состояния git

<img width="566" height="355" alt="image" src="https://github.com/user-attachments/assets/0fe26514-dfc2-4e61-9d74-a8d800cb1383" />

Рис. 9 - Автоматический запуск цепочки джобов в результате проверки git-репозитория на наличие изменений

## 9. Задание на разработку и понимание работы сервисов
  1. Создано приложение 9_app/app.py. На запросы отвечает корректно:
```
INFO:     Application startup complete.
INFO:     192.168.10.20:41986 - "POST / HTTP/1.1" 200 OK
INFO:     192.168.10.20:54382 - "POST / HTTP/1.1" 403 Forbidden
INFO:     192.168.10.20:43340 - "GET /health HTTP/1.1" 200 OK
INFO:     192.168.10.20:43352 - "GET /metrics HTTP/1.1" 200 OK
```

  2. Написан Systemd сервис 9_app/testapp.service: 
```
[Unit]
Description=Test web app (FastAPI)
After=network.target

[Service]
User=webapp
Group=webapp
WorkingDirectory=/opt/testapp
ExecStart=/opt/testapp/venv/bin/uvicorn app:app --host 0.0.0.0 --port 8000
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

  3. Написан 9_app/Dockerfile и собран образ:
```
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y --no-install-recommends iputils-ping && rm -rf /var/lib/apt/lists/*
COPY app.py .
RUN useradd -u 1000 appuser
USER 1000:1000
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```
```
docker build -t testapp:1.01 .
```
Образ запущен:
```
docker run -it --name testapp-run -p 8000:8000 testapp:1.01 uvicorn app:app --host 0.0.0.0 --port 8000
```

   4. Написан 9_app/docker-compose.yml:
```
services:
  web:
    image: testapp:1.01
    ports:
      - "8000:8000"
  prometheus:
    image: prom/prometheus:v2.51.0
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - ./alerts.yml:/etc/prometheus/alerts.yml:ro
    ports:
      - "9090:9090"
  alertmanager:
    image: prom/alertmanager:v0.27.0
    volumes:
      - ./alertmanager.yml:/etc/alertmanager/alertmanager.yml:ro
    ports:
      - "9093:9093"
```
  Подняты сервисы: 

  <img width="1528" height="103" alt="image" src="https://github.com/user-attachments/assets/e4378acd-02bc-4cb6-b419-f4c7737ede10" />

  Настроен мониторинг:

<img width="417" height="254" alt="image" src="https://github.com/user-attachments/assets/21e1badf-a5b1-4805-a330-e9056cf7573c" />

  Создана ВМ-шлюз:

  <img width="560" height="72" alt="image" src="https://github.com/user-attachments/assets/db51f2ee-becc-4712-bd4d-2910b3b14c97" />

  Настроен NAT на GW: 

  <img width="705" height="203" alt="image" src="https://github.com/user-attachments/assets/944707ae-6c13-4957-a4cf-6aefef5270bf" />

  5. ВМ с приложением за NAT, сетевые настройки ВМ изменены:
```
auto ens18
iface ens18 inet static
        address 192.168.10.20/24
        gateway 192.168.10.1
        dns-nameservers 1.1.1.1
```
Доступ из другой сети (Jenkins) настроен:

<img width="814" height="198" alt="image" src="https://github.com/user-attachments/assets/77ff5423-8e16-434d-9c49-ca8746e49553" />

  6. Созданы ВМ для k8s:

<img width="134" height="75" alt="image" src="https://github.com/user-attachments/assets/1b386688-802e-46a7-83ad-213585859679" />

  Из бинарников установлены модули k8s на всех нодах:

  ```
kubeadm init --kubernetes-version v1.37.2 --apiserver-advertise-address=192.168.10.21 --pod-network-cidr=10.244.0.0/16
  ```

```
kubeadm join 192.168.10.21:6443 --token <tok> --discovery-token-ca-cert-hash sha256:<hash>
```

  Развернуто приложение на подах:

```
root@k8s-cp:~# kubectl get deploy,pods -n app -o wide
NAME                     READY   UP-TO-DATE   AVAILABLE   AGE    CONTAINERS   IMAGES         SELECTOR
deployment.apps/webapp   3/3     3            3           6h9m   webapp       testapp:1.01   app=webapp

NAME                          READY   STATUS    RESTARTS   AGE     IP             NODE     NOMINATED NODE   READINESS GATES
pod/webapp-7f7f98cb4c-gv8pw   1/1     Running   0          5m50s   10.244.3.184   k8s-w2   <none>           <none>
pod/webapp-7f7f98cb4c-h57jx   1/1     Running   0          4m35s   10.244.2.45    k8s-w1   <none>           <none>
pod/webapp-7f7f98cb4c-xwftc   1/1     Running   0          5m51s   10.244.2.225   k8s-w1   <none>           <none>
```

  8. Установлен и настроен ingress:
```
helm install ingress-nginx ingress-nginx/ingress-nginx -n ingress-nginx --create-namespace --set controller.service.nodePorts.http=31144 
```

  Содержимое ingress.yaml:
```
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: webapp
  namespace: app
spec:
  ingressClassName: nginx
  rules:
    - http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: webapp
                port:
                  number: 8000
```

  Проверка работы Ingress:
  
  <img width="1057" height="79" alt="image" src="https://github.com/user-attachments/assets/dc69eafc-a49c-4cc0-8523-a45f3e621b03" />

```
root@k8s-cp:~# curl http://192.168.10.21:31144/health
OK
```


