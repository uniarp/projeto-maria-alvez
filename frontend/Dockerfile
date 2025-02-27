# Use a imagem oficial do Node.js
FROM node:16

# Defina o diretório de trabalho
WORKDIR /app

# Copie os arquivos de dependência
COPY package.json package-lock.json ./

# Instale as dependências do Vue
RUN npm install

# Copie o código do aplicativo Vue
COPY . .

# Exponha a porta 8080
EXPOSE 8080

# Comando para rodar o servidor Vue
CMD ["npm", "run", "serve"]
