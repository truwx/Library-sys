import mysql.connector
from mysql.connector import Error
from typing import List, Dict, Optional
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DB_CONFIG


class Database:
    """MySQL数据库管理类"""
    
    def __init__(self):
        self.connection = None
        self.init_database()
    
    def connect(self):
        """建立数据库连接"""
        try:
            if self.connection is None or not self.connection.is_connected():
                self.connection = mysql.connector.connect(**DB_CONFIG)
                print("✓ 成功连接到MySQL数据库")
        except Error as e:
            print(f"✗ 连接数据库失败: {e}")
            raise
        return self.connection
    
    def close(self):
        """关闭数据库连接"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("✓ 数据库连接已关闭")
    
    def init_database(self):
        """初始化数据库和表"""
        try:
            conn = self.connect()
            cursor = conn.cursor()
            
            # 创建图书表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS books (
                    book_id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    author VARCHAR(255) NOT NULL,
                    isbn VARCHAR(20) UNIQUE NOT NULL,
                    publisher VARCHAR(255),
                    publish_date DATE,
                    category VARCHAR(100),
                    total_copies INT DEFAULT 1,
                    available_copies INT DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    INDEX idx_title (title),
                    INDEX idx_author (author),
                    INDEX idx_isbn (isbn)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            ''')
            
            # 创建读者表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS readers (
                    reader_id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    phone VARCHAR(20),
                    email VARCHAR(100),
                    address VARCHAR(255),
                    register_date DATE DEFAULT (CURDATE()),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    INDEX idx_name (name),
                    INDEX idx_phone (phone)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            ''')
            
            # 创建借阅记录表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS borrow_records (
                    record_id INT AUTO_INCREMENT PRIMARY KEY,
                    book_id INT NOT NULL,
                    reader_id INT NOT NULL,
                    borrow_date DATE DEFAULT (CURDATE()),
                    due_date DATE,
                    return_date DATE,
                    status ENUM('borrowed', 'returned', 'overdue') DEFAULT 'borrowed',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE,
                    FOREIGN KEY (reader_id) REFERENCES readers(reader_id) ON DELETE CASCADE,
                    INDEX idx_book_id (book_id),
                    INDEX idx_reader_id (reader_id),
                    INDEX idx_status (status)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            ''')
            
            conn.commit()
            cursor.close()
            print("✓ 数据库表初始化完成")
            
        except Error as e:
            print(f"✗ 初始化数据库失败: {e}")
            raise
    
    def execute_query(self, query: str, params: tuple = ()) -> Optional[mysql.connector.cursor.MySQLCursor]:
        """执行SQL查询"""
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor
        except Error as e:
            print(f"✗ 执行查询失败: {e}")
            raise
    
    def fetch_one(self, query: str, params: tuple = ()) -> Optional[Dict]:
        """查询单条记录"""
        cursor = self.execute_query(query, params)
        if cursor:
            row = cursor.fetchone()
            cursor.close()
            if row:
                columns = [desc[0] for desc in cursor.description]
                return dict(zip(columns, row))
        return None
    
    def fetch_all(self, query: str, params: tuple = ()) -> List[Dict]:
        """查询多条记录"""
        cursor = self.execute_query(query, params)
        if cursor:
            rows = cursor.fetchall()
            cursor.close()
            if rows:
                columns = [desc[0] for desc in cursor.description]
                return [dict(zip(columns, row)) for row in rows]
        return []
    
    def insert(self, query: str, params: tuple = ()) -> int:
        """插入记录并返回ID"""
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            last_id = cursor.lastrowid
            cursor.close()
            return last_id
        except Error as e:
            print(f"✗ 插入记录失败: {e}")
            raise
    
    def update(self, query: str, params: tuple = ()) -> int:
        """更新记录并返回影响行数"""
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            row_count = cursor.rowcount
            cursor.close()
            return row_count
        except Error as e:
            print(f"✗ 更新记录失败: {e}")
            raise
    
    def delete(self, query: str, params: tuple = ()) -> int:
        """删除记录并返回影响行数"""
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            row_count = cursor.rowcount
            cursor.close()
            return row_count
        except Error as e:
            print(f"✗ 删除记录失败: {e}")
            raise
    
    def __del__(self):
        self.close()
