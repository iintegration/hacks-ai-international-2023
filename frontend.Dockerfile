FROM node:lts-alpine

RUN npm install -g http-server

WORKDIR /app

COPY ./frontend/package*.json ./

RUN npm install

COPY ./frontend /app/

RUN npm run build

EXPOSE 80
CMD [ "http-server", "-p", "80", "dist" ]