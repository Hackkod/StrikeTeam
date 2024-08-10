FROM node:20.13.1

WORKDIR /app

COPY striketeam/package*.json ./striketeam/

WORKDIR /app/striketeam

RUN npm install

COPY striketeam/ .

EXPOSE 8080

CMD ["npm", "run", "serve"]