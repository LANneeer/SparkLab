WORKDIR usr/src/app

# Устанавливаем переменные среды
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# Обновляем pip
RUN pip install --upgrade pip


# Копируем requirements.txt в текущую директорию образа
COPY requirements.txt /usr/src/app/

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Копируем исходный код Django в текущую директорию образа
COPY . /usr/src/app/
