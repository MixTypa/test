## 8. Jenkins
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

** 10. Обеспечение безопасности (Istio, Cilium, Gatekeeper)

  1. Установлены Istio, Cilium, Gatekeeper:

```
root@k8s-cp:~# kubectl get pods -n kube-system | grep cili
cilium-envoy-2rmvp                1/1     Running   0              5d4h
cilium-envoy-88vgq                1/1     Running   0              5d4h
cilium-envoy-w6rtf                1/1     Running   0              5d4h
cilium-kbm5v                      1/1     Running   0              5d4h
cilium-np5h4                      1/1     Running   0              5d4h
cilium-operator-fdbf9fc48-6vn4n   1/1     Running   1 (36h ago)    5d4h
cilium-operator-fdbf9fc48-q8k4p   1/1     Running   0              5d4h
cilium-vmgch                      1/1     Running   0              5d4h

root@k8s-cp:~# kubectl get pods -n istio-system
NAME                                    READY   STATUS    RESTARTS   AGE
istio-ingressgateway-75c5b65db6-xgj7j   1/1     Running   0          5d4h
istiod-596798464f-7l7cz                 1/1     Running   0          5d4h

root@k8s-cp:~# kubectl get pods -n gatekeeper-system
NAME                                             READY   STATUS    RESTARTS       AGE
gatekeeper-audit-79b68c74b5-rg6kw                1/1     Running   1 (5d4h ago)   5d4h
gatekeeper-controller-manager-7965664c95-5hsqt   1/1     Running   0              5d4h
gatekeeper-controller-manager-7965664c95-dd75w   1/1     Running   0              5d4h
gatekeeper-controller-manager-7965664c95-vlsjh   1/1     Running   0              5d4h
```

  2. Конфигурация Cilium:

```
root@k8s-cp:~# kubectl get ciliumnetworkpolicy -n app -o yaml
apiVersion: v1
items:
- apiVersion: cilium.io/v2
  kind: CiliumNetworkPolicy
  metadata:
    annotations:
      kubectl.kubernetes.io/last-applied-configuration: |
        {"apiVersion":"cilium.io/v2","kind":"CiliumNetworkPolicy","metadata":{"annotations":{},"name":"app-egress-restricted","namespace":"app"},"spec":{"egress":[{"toEndpoints":[{"matchLabels":{"k8s:io.kubernetes.pod.namespace":"kube-system"}}],"toPorts":[{"ports":[{"port":"53","protocol":"ANY"}]}]},{"toEndpoints":[{"matchLabels":{"k8s:io.kubernetes.pod.namespace":"app"}}]},{"toCIDR":["77.88.8.8/32"]}],"endpointSelector":{"matchLabels":{"k8s:io.kubernetes.pod.namespace":"app"}}}}
    creationTimestamp: "2026-11-10T11:32:05Z"
    generation: 1
    name: app-egress-restricted
    namespace: app
    resourceVersion: "4497"
    uid: 6f30585e-33a6-42c3-a172-de87ee83d62a
  spec:
    egress:
    - toEndpoints:
      - matchLabels:
          k8s:io.kubernetes.pod.namespace: kube-system
      toPorts:
      - ports:
        - port: "53"
          protocol: ANY
    - toEndpoints:
      - matchLabels:
          k8s:io.kubernetes.pod.namespace: app
    - toCIDR:
      - 77.88.8.8/32
    endpointSelector:
      matchLabels:
        k8s:io.kubernetes.pod.namespace: app
  status:
    conditions:
    - lastTransitionTime: "2026-11-10T11:32:06Z"
      message: Policy validation succeeded
      status: "True"
      type: Valid
kind: List
metadata:
  resourceVersion: ""
```

Конфигурация Istio:

```
apiVersion: networking.istio.io/v1
kind: Sidecar
metadata:
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: |
      {"apiVersion":"networking.istio.io/v1","kind":"Sidecar","metadata":{"annotations":{},"name":"egress-local-only","namespace":"app"},"spec":{"egress":[{"hosts":["./*","istio-system/*"]}]}}
  creationTimestamp: "2026-11-10T11:32:10Z"
  generation: 1
  name: egress-local-only
  namespace: app
  resourceVersion: "4544"
  uid: d2034d55-22bc-4bfa-b087-88786b59feb9
spec:
  egress:
  - hosts:
    - ./*
    - istio-system/*
```

  Проверка сетевой доступности: 

```
root@k8s-cp:~# kubectl exec -n app webapp-7f7f98cb4c-gv8pw -- ping -c1 github.com
PING github.com (140.82.121.4) 56(84) bytes of data.

--- github.com ping statistics ---
1 packets transmitted, 0 received, 100% packet loss, time 0ms

command terminated with exit code 1

root@k8s-cp:~# kubectl exec -n app webapp-7f7f98cb4c-gv8pw -- ping -c1 77.88.8.8
PING 77.88.8.8 (77.88.8.8) 56(84) bytes of data.
64 bytes from 77.88.8.8: icmp_seq=1 ttl=48 time=33.3 ms

--- 77.88.8.8 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 33.331/33.331/33.331/0.000 ms
```

  3. Конфигурация квоты и лимита ресурсов: 

```
root@k8s-cp:~# kubectl get quota -n app
NAME        REQUEST                                                         LIMIT                                           AGE
app-quota   pods: 3/5, requests.cpu: 300m/1, requests.memory: 384Mi/512Mi   limits.cpu: 1500m/2, limits.memory: 768Mi/1Gi   5d4h
```
```
apiVersion: v1
items:
- apiVersion: v1
  kind: LimitRange
  metadata:
    annotations:
      kubectl.kubernetes.io/last-applied-configuration: |
        {"apiVersion":"v1","kind":"LimitRange","metadata":{"annotations":{},"name":"app-limits","namespace":"app"},"spec":{"limits":[{"max":{"cpu":"500m","memory":"256Mi"},"min":{"cpu":"10m","memory":"10Mi"},"type":"Container"}]}}
    creationTimestamp: "2026-11-10T11:32:02Z"
    name: app-limits
    namespace: app
    resourceVersion: "4437"
    uid: a72fa907-953e-4da8-b978-999a436b75c4
  spec:
    limits:
    - default:
        cpu: 500m
        memory: 256Mi
      defaultRequest:
        cpu: 500m
        memory: 256Mi
      max:
        cpu: 500m
        memory: 256Mi
      min:
        cpu: 10m
        memory: 10Mi
      type: Container
kind: List
metadata:
  resourceVersion: ""
```

Ограничение файловой системы - "readOnlyRootFilesystem: true" и прав пользователей:

```
root@k8s-cp:~# kubectl get deploy -n app -o yaml | grep -A10 "securityContext"
        {"apiVersion":"apps/v1","kind":"Deployment","metadata":{"annotations":{},"labels":{"app":"webapp"},"name":"webapp","namespace":"app"},"spec":{"replicas":2,"selector":{"matchLabels":{"app":"webapp"}},"template":{"metadata":{"labels":{"app":"webapp"}},"spec":{"containers":[{"image":"testapp:1.01","name":"webapp","ports":[{"containerPort":8000}],"resources":{"limits":{"cpu":"500m","memory":"256Mi"},"requests":{"cpu":"100m","memory":"128Mi"}},"securityContext":{"allowPrivilegeEscalation":false,"capabilities":{"add":["NET_RAW"],"drop":["ALL"]},"readOnlyRootFilesystem":true,"runAsNonRoot":true}}],"securityContext":{"runAsNonRoot":true,"sysctls":[{"name":"net.ipv4.ping_group_range","value":"0 2147483647"}]}}}}}
    creationTimestamp: "2026-11-10T11:32:02Z"
    generation: 3
    labels:
      app: webapp
    name: webapp
    namespace: app
    resourceVersion: "68073"
    uid: 494d6604-42fe-4e3d-a8f8-8900e533d17e
  spec:
    progressDeadlineSeconds: 600
--
          securityContext:
            allowPrivilegeEscalation: false
            capabilities:
              add:
              - NET_RAW
              drop:
              - ALL
            readOnlyRootFilesystem: true
            runAsNonRoot: true
          terminationMessagePath: /dev/termination-log
          terminationMessagePolicy: File
--
        securityContext:
          runAsNonRoot: true
          sysctls:
          - name: net.ipv4.ping_group_range
            value: 0 2147483647
        terminationGracePeriodSeconds: 30
  status:
    availableReplicas: 3
    conditions:
    - lastTransitionTime: "2026-11-10T11:32:02Z"
      lastUpdateTime: "2026-11-10T17:36:04Z"
```

