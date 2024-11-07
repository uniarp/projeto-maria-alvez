# projeto-maria-alvez

# Projeto Centro de Bem-Estar Animal Maria Alves

# Diretrizes para Commits #

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