-- ====================================
-- FINANCEPRO - DATABASE SCHEMA
-- Sistema de Controle Financeiro
-- ====================================

-- Criar banco de dados
CREATE DATABASE IF NOT EXISTS financepro CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE financepro;

-- ====================================
-- TABELA: users (Usuários)
-- ====================================
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    avatar VARCHAR(255) DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ====================================
-- TABELA: categories (Categorias)
-- ====================================
CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(50) NOT NULL,
    type ENUM('income', 'expense') NOT NULL,
    icon VARCHAR(50) DEFAULT '💰',
    color VARCHAR(7) DEFAULT '#3B82F6',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_type (user_id, type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ====================================
-- TABELA: transactions (Movimentações)
-- ====================================
CREATE TABLE IF NOT EXISTS transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    category_id INT NOT NULL,
    description VARCHAR(255) NOT NULL,
    amount DECIMAL(12, 2) NOT NULL,
    type ENUM('income', 'expense') NOT NULL,
    date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE RESTRICT,
    INDEX idx_user_date (user_id, date),
    INDEX idx_type (type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ====================================
-- TABELA: goals (Metas Financeiras)
-- ====================================
CREATE TABLE IF NOT EXISTS goals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    target_amount DECIMAL(12, 2) NOT NULL,
    current_amount DECIMAL(12, 2) DEFAULT 0.00,
    deadline DATE,
    status ENUM('active', 'completed', 'cancelled') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_status (user_id, status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ====================================
-- INSERIR CATEGORIAS PADRÃO
-- ====================================
-- Será feito via backend após criação do usuário

-- ====================================
-- VIEWS ÚTEIS
-- ====================================

-- View: Resumo mensal por usuário
CREATE OR REPLACE VIEW monthly_summary AS
SELECT 
    user_id,
    YEAR(date) as year,
    MONTH(date) as month,
    type,
    SUM(amount) as total
FROM transactions
GROUP BY user_id, YEAR(date), MONTH(date), type;

-- View: Gastos por categoria
CREATE OR REPLACE VIEW expenses_by_category AS
SELECT 
    t.user_id,
    c.name as category_name,
    c.icon,
    c.color,
    COUNT(t.id) as transaction_count,
    SUM(t.amount) as total_amount
FROM transactions t
JOIN categories c ON t.category_id = c.id
WHERE t.type = 'expense'
GROUP BY t.user_id, c.id, c.name, c.icon, c.color;

-- ====================================
-- STORED PROCEDURES
-- ====================================

DELIMITER $$

-- Procedure: Calcular saldo do usuário
CREATE PROCEDURE calculate_balance(IN p_user_id INT)
BEGIN
    SELECT 
        COALESCE(SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END), 0) as total_income,
        COALESCE(SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END), 0) as total_expense,
        COALESCE(SUM(CASE WHEN type = 'income' THEN amount ELSE -amount END), 0) as balance
    FROM transactions
    WHERE user_id = p_user_id;
END$$

-- Procedure: Resumo mensal
CREATE PROCEDURE monthly_report(IN p_user_id INT, IN p_year INT, IN p_month INT)
BEGIN
    SELECT 
        type,
        COUNT(*) as count,
        SUM(amount) as total
    FROM transactions
    WHERE user_id = p_user_id 
        AND YEAR(date) = p_year 
        AND MONTH(date) = p_month
    GROUP BY type;
END$$

DELIMITER ;

-- ====================================
-- DADOS DE EXEMPLO (OPCIONAL)
-- ====================================
-- Descomente para inserir dados de teste

/*
-- Usuário de teste (senha: 123456)
INSERT INTO users (name, email, password) VALUES 
('Admin Teste', 'admin@financepro.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5lHOjOEuuQT8W');

SET @user_id = LAST_INSERT_ID();

-- Categorias padrão
INSERT INTO categories (user_id, name, type, icon, color) VALUES
(@user_id, 'Salário', 'income', '💰', '#10B981'),
(@user_id, 'Freelance', 'income', '💼', '#3B82F6'),
(@user_id, 'Investimentos', 'income', '📈', '#8B5CF6'),
(@user_id, 'Alimentação', 'expense', '🍔', '#EF4444'),
(@user_id, 'Transporte', 'expense', '🚗', '#F59E0B'),
(@user_id, 'Lazer', 'expense', '🎮', '#EC4899'),
(@user_id, 'Saúde', 'expense', '🏥', '#14B8A6'),
(@user_id, 'Compras', 'expense', '🛒', '#6366F1');

-- Transações de exemplo
INSERT INTO transactions (user_id, category_id, description, amount, type, date) VALUES
(@user_id, 1, 'Salário Mensal', 5000.00, 'income', '2024-01-05'),
(@user_id, 4, 'Supermercado', 450.00, 'expense', '2024-01-10'),
(@user_id, 5, 'Uber', 85.00, 'expense', '2024-01-12'),
(@user_id, 6, 'Netflix', 45.90, 'expense', '2024-01-15');

-- Metas de exemplo
INSERT INTO goals (user_id, title, description, target_amount, current_amount, deadline) VALUES
(@user_id, 'Viagem para Europa', 'Economizar para viagem de 15 dias', 15000.00, 3000.00, '2024-12-31'),
(@user_id, 'Reserva de Emergência', '6 meses de despesas', 30000.00, 8000.00, '2024-12-31');
*/

-- ====================================
-- FIM DO SCHEMA
-- ====================================