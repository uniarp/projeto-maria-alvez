-- Criação da extensão pgcrypto para gerar o hash de senha
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Inserção de um superusuário (se não existir)
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM auth_user WHERE username = 'admin') THEN
        INSERT INTO auth_user (username, email, password, is_superuser, is_staff)
        VALUES
        ('admin', 'admin@admin.com', crypt('admin', gen_salt('bf', 8)), TRUE, TRUE);
    END IF;
END $$;
