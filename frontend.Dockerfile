FROM node:lts-alpine

WORKDIR /app
COPY ./frontend/package*.json ./
RUN npm install
COPY ./frontend /app/
RUN npm run build

FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]