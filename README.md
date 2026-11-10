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

