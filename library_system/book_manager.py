from typing import List, Optional
from .models import Book
from .database import Database


class BookManager:
    """图书管理类"""
    
    def __init__(self, db: Database):
        self.db = db
    
    def add_book(self, book: Book) -> int:
        """添加图书"""
        query = '''
            INSERT INTO books (title, author, isbn, publisher, publish_date, 
                             category, total_copies, available_copies)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        '''
        params = (
            book.title, book.author, book.isbn, book.publisher,
            book.publish_date, book.category, book.total_copies,
            book.available_copies
        )
        return self.db.insert(query, params)
    
    def delete_book(self, book_id: int) -> bool:
        """删除图书"""
        query = "DELETE FROM books WHERE book_id = %s"
        return self.db.delete(query, (book_id,)) > 0
    
    def update_book(self, book_id: int, **kwargs) -> bool:
        """更新图书信息"""
        if not kwargs:
            return False
        
        fields = []
        values = []
        for key, value in kwargs.items():
            fields.append(f"{key} = %s")
            values.append(value)
        
        values.append(book_id)
        
        query = f"UPDATE books SET {', '.join(fields)} WHERE book_id = %s"
        return self.db.update(query, tuple(values)) > 0
    
    def get_book_by_id(self, book_id: int) -> Optional[Book]:
        """根据ID获取图书"""
        query = "SELECT * FROM books WHERE book_id = %s"
        data = self.db.fetch_one(query, (book_id,))
        if data:
            return self._dict_to_book(data)
        return None
    
    def get_book_by_isbn(self, isbn: str) -> Optional[Book]:
        """根据ISBN获取图书"""
        query = "SELECT * FROM books WHERE isbn = %s"
        data = self.db.fetch_one(query, (isbn,))
        if data:
            return self._dict_to_book(data)
        return None
    
    def search_books(self, keyword: str) -> List[Book]:
        """搜索图书（支持书名、作者、ISBN）"""
        query = '''
            SELECT * FROM books 
            WHERE title LIKE %s OR author LIKE %s OR isbn LIKE %s
            ORDER BY created_at DESC
        '''
        search_term = f"%{keyword}%"
        results = self.db.fetch_all(query, (search_term, search_term, search_term))
        return [self._dict_to_book(data) for data in results]
    
    def get_all_books(self, page: int = 1, page_size: int = 20) -> List[Book]:
        """获取所有图书（分页）"""
        offset = (page - 1) * page_size
        query = "SELECT * FROM books ORDER BY created_at DESC LIMIT %s OFFSET %s"
        results = self.db.fetch_all(query, (page_size, offset))
        return [self._dict_to_book(data) for data in results]
    
    def get_total_count(self) -> int:
        """获取图书总数"""
        query = "SELECT COUNT(*) as count FROM books"
        result = self.db.fetch_one(query)
        return result['count'] if result else 0
    
    def update_availability(self, book_id: int, decrease: bool = True) -> bool:
        """更新图书可用数量"""
        if decrease:
            query = '''
                UPDATE books 
                SET available_copies = available_copies - 1
                WHERE book_id = %s AND available_copies > 0
            '''
        else:
            query = '''
                UPDATE books 
                SET available_copies = available_copies + 1
                WHERE book_id = %s
            '''
        return self.db.update(query, (book_id,)) > 0
    
    def _dict_to_book(self, data: dict) -> Book:
        """将字典转换为Book对象"""
        return Book(
            book_id=data['book_id'],
            title=data['title'],
            author=data['author'],
            isbn=data['isbn'],
            publisher=data.get('publisher'),
            publish_date=str(data.get('publish_date', '')),
            category=data.get('category'),
            total_copies=data['total_copies'],
            available_copies=data['available_copies'],
            created_at=str(data.get('created_at', '')),
            updated_at=str(data.get('updated_at', ''))
        )
