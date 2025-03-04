## Github Actions Example

Этот проект использует GitHub Actions для автоматизации процессов тестирования, сборки и развертывания FastAPI приложения. Ниже описано, как работает CI/CD pipeline.

![Screenshot from 2025-03-01 13-20-04.png](Screenshot%20from%202025-03-01%2013-20-04.png)


---

### Как работает workflow?

#### 1. **Триггеры**
Workflow запускается автоматически при каждом пуше в ветку `main`.

---

#### 2. **Задачи (Jobs)**

##### **Job 1: `test` (Запуск тестов)**
Эта задача проверяет корректность кода. Она выполняется на виртуальной машине с Ubuntu.

- **Шаги:**
  1. **Клонирование репозитория**: Копируется код из репозитория.
  2. **Установка Python**: Устанавливается Python версии 3.9.
  3. **Установка зависимостей**:
     - Создается виртуальное окружение (`venv`).
     - Устанавливаются зависимости (`fastapi`, `uvicorn`, `httpx`, `pytest`).
  4. **Запуск тестов**: Запускаются тесты с помощью `pytest`.

##### **Job 2: `build-and-deploy` (Сборка и развертывание)**
Эта задача выполняется только после успешного завершения задачи `test`. Она отвечает за сборку Docker-образа, его загрузку в Docker Hub и развертывание на удаленном сервере.

- **Шаги:**
  1. **Клонирование репозитория**: Снова копируется код из репозитория.
  2. **Настройка Docker Buildx**: Устанавливается Docker Buildx для сборки многоплатформенных Docker-образов.
  3. **Авторизация в Docker Hub**: Происходит вход в Docker Hub с использованием логина и токена из секретов GitHub.
  4. **Сборка Docker-образа**: Собирается Docker-образ с именем, указанным в секретах.
  5. **Загрузка Docker-образа в Docker Hub**: Собранный образ загружается в Docker Hub.
  6. **Деплой на удаленный сервер**:
     - Устанавливается утилита `sshpass` для автоматизации ввода пароля при SSH-подключении.
     - Подключаемся к удаленному серверу через SSH (используя хост, пользователя и пароль из секретов).
     - На удаленном сервере:
       - Скачивается последняя версия Docker-образа из Docker Hub.
       - Останавливается и удаляется текущий контейнер (если он существует).
       - Запускается новый контейнер из скачанного образа на порту 80 (внутри контейнера приложение работает на порту 8000).

---

### Секреты (Secrets)
Workflow использует несколько секретов, которые хранятся в настройках репозитория GitHub:

- **`DOCKER_HUB_USERNAME`**: Логин для Docker Hub.
- **`DOCKER_HUB_TOKEN`**: Токен для доступа к Docker Hub (вместо пароля).
- **`REMOTE_HOST`**: Адрес удаленного сервера (например, IP или доменное имя).
- **`REMOTE_USER`**: Имя пользователя для подключения к серверу через SSH.
- **`REMOTE_PASSWORD`**: Пароль для подключения к серверу через SSH.

---

### Что происходит в итоге?
1. **При пуше в ветку `main`:**
   - Запускаются тесты.
   - Если тесты проходят успешно, начинается сборка и деплой.
2. **Сборка Docker-образа:**
   - Создается Docker-образ приложения.
   - Образ загружается в Docker Hub.
3. **Деплой на удаленный сервер:**
   - На удаленном сервере останавливается старый контейнер и запускается новый из обновленного образа.
   - Приложение становится доступным на порту 80 удаленного сервера.

---

### Для чего это нужно?
Этот workflow автоматизирует процесс разработки и развертывания приложения:

- **Тестирование**: Убеждаемся, что изменения не сломали приложение.
- **Сборка**: Создаем Docker-образ, который содержит все необходимое для запуска приложения.
- **Деплой**: Обновляем приложение на удаленном сервере без ручного вмешательства.

---

### Что можно улучшить?
- **Использование Docker Compose**: Упростить управление контейнерами на удаленном сервере.
- **Обработка ошибок**: Добавить проверки на каждом этапе, чтобы workflow не завершался с ошибкой.
- **Логирование**: Добавить логирование для упрощения отладки.
- **Уведомления**: Настроить уведомления (например, в Slack или Telegram) о результатах выполнения workflow.

---

Этот файл — мощный инструмент для автоматизации процессов разработки и развертывания, который экономит время и уменьшает вероятность ошибок.

---

Если у вас есть дополнительные вопросы, дайте знать! 😊

### Токен Docker Hub
Токен Docker Hub — это безопасный способ аутентификации в Docker Hub без использования вашего основного пароля. Docker Hub позволяет создавать Personal Access Tokens (PAT), которые можно использовать для входа в Docker Hub через API или CLI. Это более безопасно, чем использование пароля, так как токен можно отозвать в любой момент, и он имеет ограниченные права.
Что такое Docker Hub Token?

* Personal Access Token (PAT) — это строка, которая используется для аутентификации вместо пароля.

* Токен можно создать с определенными правами (например, только для чтения или для чтения/записи).

* Токен можно отозвать в любой момент, если он больше не нужен или скомпрометирован.

#### Как создать токен в Docker Hub?

* Войдите в Docker Hub:

    Перейдите на Docker Hub и войдите в свою учетную запись.

* Перейдите в настройки аккаунта:

Нажмите на ваш профиль в правом верхнем углу и выберите Account Settings.

* Создайте токен:

В меню слева выберите Security.

Нажмите New Access Token.

* Настройте токен:

    Введите описание токена (например, GitHub Actions).

    Выберите уровень доступа:

    Read-only: Только для чтения (например, для скачивания образов).

    Read & Write: Для чтения и записи (например, для загрузки образов).

    Нажмите Generate.

* Скопируйте токен:

После создания токена он будет показан только один раз. Скопируйте его и сохраните в надежном месте.

#### Как использовать токен в GitHub Actions?

Токен используется в шаге Log in to Docker Hub в вашем workflow. Вместо пароля вы используете токен:

```
- name: Log in to Docker Hub
  uses: docker/login-action@v1
  with:
    username: ${{ secrets.DOCKER_HUB_USERNAME }}
    password: ${{ secrets.DOCKER_HUB_TOKEN }}  # Используем токен вместо пароля
```



Как добавить токен в секреты GitHub?

* Перейдите в настройки вашего репозитория на GitHub.

    Перейдите в раздел Secrets and variables > Actions.

    Нажмите New repository secret.

    Введите:

    Имя: DOCKER_HUB_TOKEN

    Значение: Ваш токен Docker Hub.

    Сохраните.

Итог

* Токен Docker Hub — это безопасный способ аутентификации, который можно создать в настройках Docker Hub.

* Использование токена предпочтительнее, чем использование пароля, из-за повышенной безопасности и гибкости.

* Токен добавляется в секреты GitHub и используется в GitHub Actions для входа в Docker Hub.