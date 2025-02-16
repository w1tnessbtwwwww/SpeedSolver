# Используем официальный Node.js образ
FROM node:20 AS build

# Устанавливаем рабочую директорию
WORKDIR /app/frontend

# Копируем package.json и package-lock.json
COPY package*.json ./

# Устанавливаем зависимости
RUN npm install

# Копируем весь проект в контейнер
COPY . .

# Строим проект
RUN npm run build

# Используем Nginx для продакшн сервера
FROM nginx:alpine


COPY nginx.conf /etc/nginx/nginx.conf
COPY --from=build /app/frontend/dist /usr/share/nginx/html

# Открываем порт 80
EXPOSE 3000


CMD ["nginx", "-g", "daemon off;"]