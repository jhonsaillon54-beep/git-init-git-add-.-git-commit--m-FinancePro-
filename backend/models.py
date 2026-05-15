"""
FinancePro Models
Classes de modelo para interação com banco de dados
"""
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
from config import config

class Database:
    """Classe para gerenciar conexão com MySQL"""
    
    @staticmethod
    def get_connection():
        """Criar conexão com o banco de dados"""
        try:
            connection = mysql.connector.connect(**config.DB_CONFIG)
            return connection
        except Error as e:
            print(f"Erro ao conectar ao MySQL: {e}")
            return None
    
    @staticmethod
    def execute_query(query, params=None, fetch=False):
        """Executar query no banco de dados"""
        connection = Database.get_connection()
        if not connection:
            return None
        
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            if fetch:
                result = cursor.fetchall()
            else:
                connection.commit()
                result = cursor.lastrowid or cursor.rowcount
            
            cursor.close()
            connection.close()
            return result
        except Error as e:
            print(f"Erro ao executar query: {e}")
            if connection:
                connection.close()
            return None

class User:
    """Model de usuário"""
    
    @staticmethod
    def create(name, email, password):
        """Criar novo usuário"""
        hashed_password = generate_password_hash(password)
        query = """
            INSERT INTO users (name, email, password)
            VALUES (%s, %s, %s)
        """
        user_id = Database.execute_query(query, (name, email, hashed_password))
        
        if user_id:
            # Criar categorias padrão
            User.create_default_categories(user_id)
        
        return user_id
    
    @staticmethod
    def create_default_categories(user_id):
        """Criar categorias padrão para novo usuário"""
        default_categories = [
            (user_id, 'Salário', 'income', '💰', '#10B981'),
            (user_id, 'Freelance', 'income', '💼', '#3B82F6'),
            (user_id, 'Investimentos', 'income', '📈', '#8B5CF6'),
            (user_id, 'Outros Ganhos', 'income', '💵', '#06B6D4'),
            (user_id, 'Alimentação', 'expense', '🍔', '#EF4444'),
            (user_id, 'Transporte', 'expense', '🚗', '#F59E0B'),
            (user_id, 'Lazer', 'expense', '🎮', '#EC4899'),
            (user_id, 'Saúde', 'expense', '🏥', '#14B8A6'),
            (user_id, 'Compras', 'expense', '🛒', '#6366F1'),
            (user_id, 'Educação', 'expense', '📚', '#8B5CF6'),
            (user_id, 'Moradia', 'expense', '🏠', '#64748B'),
            (user_id, 'Outros Gastos', 'expense', '📝', '#94A3B8'),
        ]
        
        query = """
            INSERT INTO categories (user_id, name, type, icon, color)
            VALUES (%s, %s, %s, %s, %s)
        """
        
        for category in default_categories:
            Database.execute_query(query, category)
    
    @staticmethod
    def find_by_email(email):
        """Buscar usuário por email"""
        query = "SELECT * FROM users WHERE email = %s"
        result = Database.execute_query(query, (email,), fetch=True)
        return result[0] if result else None
    
    @staticmethod
    def find_by_id(user_id):
        """Buscar usuário por ID"""
        query = "SELECT id, name, email, avatar, created_at FROM users WHERE id = %s"
        result = Database.execute_query(query, (user_id,), fetch=True)
        return result[0] if result else None
    
    @staticmethod
    def verify_password(stored_password, provided_password):
        """Verificar senha"""
        return check_password_hash(stored_password, provided_password)
    
    @staticmethod
    def update_profile(user_id, name, email):
        """Atualizar perfil do usuário"""
        query = "UPDATE users SET name = %s, email = %s WHERE id = %s"
        return Database.execute_query(query, (name, email, user_id))
    
    @staticmethod
    def update_avatar(user_id, avatar_path):
        """Atualizar avatar do usuário"""
        query = "UPDATE users SET avatar = %s WHERE id = %s"
        return Database.execute_query(query, (avatar_path, user_id))

class Transaction:
    """Model de transação"""
    
    @staticmethod
    def create(user_id, category_id, description, amount, trans_type, trans_date):
        """Criar nova transação"""
        query = """
            INSERT INTO transactions (user_id, category_id, description, amount, type, date)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        return Database.execute_query(
            query, 
            (user_id, category_id, description, amount, trans_type, trans_date)
        )
    
    @staticmethod
    def get_all(user_id, limit=100, offset=0):
        """Buscar todas as transações do usuário"""
        query = """
            SELECT t.*, c.name as category_name, c.icon, c.color
            FROM transactions t
            JOIN categories c ON t.category_id = c.id
            WHERE t.user_id = %s
            ORDER BY t.date DESC, t.created_at DESC
            LIMIT %s OFFSET %s
        """
        return Database.execute_query(query, (user_id, limit, offset), fetch=True)
    
    @staticmethod
    def get_by_id(trans_id, user_id):
        """Buscar transação por ID"""
        query = """
            SELECT t.*, c.name as category_name, c.icon, c.color
            FROM transactions t
            JOIN categories c ON t.category_id = c.id
            WHERE t.id = %s AND t.user_id = %s
        """
        result = Database.execute_query(query, (trans_id, user_id), fetch=True)
        return result[0] if result else None
    
    @staticmethod
    def update(trans_id, user_id, category_id, description, amount, trans_type, trans_date):
        """Atualizar transação"""
        query = """
            UPDATE transactions
            SET category_id = %s, description = %s, amount = %s, type = %s, date = %s
            WHERE id = %s AND user_id = %s
        """
        return Database.execute_query(
            query,
            (category_id, description, amount, trans_type, trans_date, trans_id, user_id)
        )
    
    @staticmethod
    def delete(trans_id, user_id):
        """Deletar transação"""
        query = "DELETE FROM transactions WHERE id = %s AND user_id = %s"
        return Database.execute_query(query, (trans_id, user_id))
    
    @staticmethod
    def get_summary(user_id):
        """Obter resumo financeiro do usuário"""
        query = """
            SELECT 
                COALESCE(SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END), 0) as total_income,
                COALESCE(SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END), 0) as total_expense,
                COALESCE(SUM(CASE WHEN type = 'income' THEN amount ELSE -amount END), 0) as balance
            FROM transactions
            WHERE user_id = %s
        """
        result = Database.execute_query(query, (user_id,), fetch=True)
        return result[0] if result else None
    
    @staticmethod
    def get_monthly_summary(user_id, year, month):
        """Obter resumo mensal"""
        query = """
            SELECT 
                type,
                COALESCE(SUM(amount), 0) as total,
                COUNT(*) as count
            FROM transactions
            WHERE user_id = %s AND YEAR(date) = %s AND MONTH(date) = %s
            GROUP BY type
        """
        return Database.execute_query(query, (user_id, year, month), fetch=True)
    
    @staticmethod
    def get_by_category(user_id):
        """Obter gastos por categoria"""
        query = """
            SELECT 
                c.name,
                c.icon,
                c.color,
                SUM(t.amount) as total,
                COUNT(t.id) as count
            FROM transactions t
            JOIN categories c ON t.category_id = c.id
            WHERE t.user_id = %s AND t.type = 'expense'
            GROUP BY c.id, c.name, c.icon, c.color
            ORDER BY total DESC
        """
        return Database.execute_query(query, (user_id,), fetch=True)
    
    @staticmethod
    def get_recent(user_id, limit=5):
        """Obter transações recentes"""
        query = """
            SELECT t.*, c.name as category_name, c.icon, c.color
            FROM transactions t
            JOIN categories c ON t.category_id = c.id
            WHERE t.user_id = %s
            ORDER BY t.date DESC, t.created_at DESC
            LIMIT %s
        """
        return Database.execute_query(query, (user_id, limit), fetch=True)

class Category:
    """Model de categoria"""
    
    @staticmethod
    def get_all(user_id):
        """Buscar todas as categorias do usuário"""
        query = """
            SELECT * FROM categories
            WHERE user_id = %s
            ORDER BY type, name
        """
        return Database.execute_query(query, (user_id,), fetch=True)
    
    @staticmethod
    def get_by_type(user_id, cat_type):
        """Buscar categorias por tipo"""
        query = """
            SELECT * FROM categories
            WHERE user_id = %s AND type = %s
            ORDER BY name
        """
        return Database.execute_query(query, (user_id, cat_type), fetch=True)
    
    @staticmethod
    def create(user_id, name, cat_type, icon='💰', color='#3B82F6'):
        """Criar nova categoria"""
        query = """
            INSERT INTO categories (user_id, name, type, icon, color)
            VALUES (%s, %s, %s, %s, %s)
        """
        return Database.execute_query(query, (user_id, name, cat_type, icon, color))
    
    @staticmethod
    def update(cat_id, user_id, name, icon, color):
        """Atualizar categoria"""
        query = """
            UPDATE categories
            SET name = %s, icon = %s, color = %s
            WHERE id = %s AND user_id = %s
        """
        return Database.execute_query(query, (name, icon, color, cat_id, user_id))
    
    @staticmethod
    def delete(cat_id, user_id):
        """Deletar categoria"""
        query = "DELETE FROM categories WHERE id = %s AND user_id = %s"
        return Database.execute_query(query, (cat_id, user_id))

class Goal:
    """Model de meta financeira"""
    
    @staticmethod
    def create(user_id, title, description, target_amount, deadline=None):
        """Criar nova meta"""
        query = """
            INSERT INTO goals (user_id, title, description, target_amount, deadline)
            VALUES (%s, %s, %s, %s, %s)
        """
        return Database.execute_query(
            query,
            (user_id, title, description, target_amount, deadline)
        )
    
    @staticmethod
    def get_all(user_id):
        """Buscar todas as metas do usuário"""
        query = """
            SELECT * FROM goals
            WHERE user_id = %s
            ORDER BY 
                CASE status
                    WHEN 'active' THEN 1
                    WHEN 'completed' THEN 2
                    WHEN 'cancelled' THEN 3
                END,
                deadline ASC
        """
        return Database.execute_query(query, (user_id,), fetch=True)
    
    @staticmethod
    def get_by_id(goal_id, user_id):
        """Buscar meta por ID"""
        query = "SELECT * FROM goals WHERE id = %s AND user_id = %s"
        result = Database.execute_query(query, (goal_id, user_id), fetch=True)
        return result[0] if result else None
    
    @staticmethod
    def update(goal_id, user_id, title, description, target_amount, current_amount, deadline, status):
        """Atualizar meta"""
        query = """
            UPDATE goals
            SET title = %s, description = %s, target_amount = %s, 
                current_amount = %s, deadline = %s, status = %s
            WHERE id = %s AND user_id = %s
        """
        return Database.execute_query(
            query,
            (title, description, target_amount, current_amount, deadline, status, goal_id, user_id)
        )
    
    @staticmethod
    def update_amount(goal_id, user_id, amount):
        """Atualizar valor atual da meta"""
        query = """
            UPDATE goals
            SET current_amount = %s
            WHERE id = %s AND user_id = %s
        """
        return Database.execute_query(query, (amount, goal_id, user_id))
    
    @staticmethod
    def delete(goal_id, user_id):
        """Deletar meta"""
        query = "DELETE FROM goals WHERE id = %s AND user_id = %s"
        return Database.execute_query(query, (goal_id, user_id))