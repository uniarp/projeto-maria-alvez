# Projeto Centro de Bem-Estar Animal Maria Alves

# Instalação DOCKER E DOCKER-COMPOSE

    1. Linux
    Passo 1: Instale o Docker

    Se você ainda não tem o Docker instalado, siga estas etapas:

    sudo apt update
    sudo apt install -y docker.io

    Passo 2: Baixe a última versão do Docker Compose

    Verifique no GitHub do Docker Compose qual a versão mais recente e substitua no comando abaixo:

    sudo curl -L "https://github.com/docker/compose/releases/download/2.20.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

    Passo 3: Dê permissão de execução ao Docker Compose

    sudo chmod +x /usr/local/bin/docker-compose

    Passo 4: Verifique a instalação

    docker-compose --version

# 2. Windows

    Para Windows, o Docker Desktop inclui o Docker Compose, então você pode instalá-lo diretamente com o Docker Desktop:

        Baixe o Docker Desktop para Windows.
        Instale o Docker Desktop.
        Abra o Docker Desktop e vá até as configurações para confirmar que o Docker Compose está habilitado.

    Após a instalação, você pode verificar se o Docker Compose está funcionando abrindo o PowerShell e digitando:

    docker-compose --version

# 3. macOS

    No macOS, o Docker Desktop também inclui o Docker Compose:

        Baixe o Docker Desktop para macOS.
        Arraste o Docker para a pasta Aplicativos e abra-o.
        Siga as instruções para habilitar e configurar o Docker Desktop.

Depois, você pode verificar se o Docker Compose está funcionando no terminal:

docker-compose --version

# Iniciar container Docker

    docker build -t nome-do-projeto .

# iniciar todos os containers com docker-compose

    docker-compose up -d

# Diretrizes para Commits

# Todos os commits devem ser realizados na branch prod. Para garantir um fluxo de trabalho organizado, siga estas etapas:

    Crie uma branch para o desenvolvimento:

        Para cada nova funcionalidade ou correção de bug, crie uma nova branch de desenvolvimento:

        git checkout -b nome-da-sua-branch

# Finalize a funcionalidade e faça commit das mudanças:

    Faça commit das suas mudanças na branch de desenvolvimento:

        git add .
        git commit -m "Descrição do commit"

# Faça o merge na branch prod:

    Após revisar e testar suas alterações, faça o merge da sua branch de desenvolvimento para prod:

        git checkout prod
        git merge nome-da-sua-branch

# Push para o repositório remoto:

    Envie a branch prod para o repositório remoto:

        git push origin prod

# Tecnologias Utilizadas

    Django: Backend principal para gerenciamento de dados e lógica de negócio.
    Docker: Utilizado para containerização e fácil implantação do sistema.

# Contribuição

Para contribuir, siga as diretrizes de commits e faça o merge das suas alterações na branch prod apenas após a conclusão e teste das novas funcionalidades.
