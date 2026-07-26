FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 8080

RUN apk add --no-cache python3

CMD sh -c "npm run build:widget && python3 -m http.server 8080 --directory dist"