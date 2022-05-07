#https://hub.docker.com/
FROM node:18-alpine
# indico donde se almacenará la aplicación dentro del controlador
WORKDIR /app
# Copio el archivo package.json dentro de la carpeta /app (directorio de trabajo)
# que archivo hacia donde (dentro del contenedor)

#COPY package.json /app/
#COPY package-lock.json /app/

COPY . /app/

# instalara todas las dependencias en el contenedor
# RUN pip install -r requirements.txt (si fuese python)
RUN npm install

#COPY /src/ /app/src/

#dare un comando para que se inicie el proyecto en el contenedor

CMD ["npm", "run", "start:dev"]