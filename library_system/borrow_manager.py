from typing import List, Optional
from datetime import datetime, timedelta
from .models import BorrowRecord
from .database import Database
from .book_manager import BookManager
from .reader_manager import ReaderManager


class BorrowManager:
    """借阅管理类"""
    
    def __init__(self, db: Database):
        self.db = db
        self.book_manager = BookManager(db)
        self.reader_manager = ReaderManager(db)
    
    def borrow_book(self, book_id: int, reader_id: int, borrow_days: int = 30) -> Optional[int]:
        """借书"""
        # 检查图书是否存在且可借
        book = self.book_manager.get_book_by_id(book_id)
        if not book:
            print("✗ 图书不存在")
            return None
        
        if book.available_copies <= 0:
            print("✗ 图书已全部借出")
            return None
        
        # 检查读者是否存在
        reader = self.reader_manager.get_reader_by_id(reader_id)
        if not reader:
            print("✗ 读者不存在")
            return None
        
        # 检查是否有未归还的同本书
        query = '''
            SELECT COUNT(*) as count FROM borrow_records 
            WHERE book_id = %s AND reader_id = %s AND status = 'borrowed'
        '''
        result = self.db.fetch_one(query, (book_id, reader_id))
        if result and result['count'] > 0:
            print("✗ 该读者已借阅此书且未归还")
            return None
        
        # 创建借阅记录
        borrow_date = datetime.now().date()
        due_date = borrow_date + timedelta(days=borrow_days)
        
        record = BorrowRecord(
            book_id=book_id,
            reader_id=reader_id,
            borrow_date=str(borrow_date),
            due_date=str(due_date),
            status='borrowed'
        )
        
        query = '''
            INSERT INTO borrow_records (book_id, reader_id, borrow_date, due_date, status)
            VALUES (%s, %s, %s, %s, %s)
        '''
        params = (record.book_id, record.reader_id, record.borrow_date, 
                 record.due_date, record.status)
        
        record_id = self.db.insert(query, params)
        
        if record_id:
            # 更新图书可用数量
            self.book_manager.update_availability(book_id, decrease=True)
            print(f"✓ 借书成功！记录ID: {record_id}")
            print(f"  应还日期: {due_date}")
            return record_id
        
        return None
    
    def return_book(self, record_id: int) -> bool:
        """还书"""
        # 查询借阅记录
        query = "SELECT * FROM borrow_records WHERE record_id = %s AND status = 'borrowed'"
        record_data = self.db.fetch_one(query, (record_id,))
        
        if not record_data:
            print("✗ 借阅记录不存在或已归还")
            return False
        
        return_date = datetime.now().date()
        
        # 更新借阅记录
        update_query = '''
            UPDATE borrow_records 
            SET return_date = %s, status = 'returned'
            WHERE record_id = %s
        '''
        success = self.db.update(update_query, (str(return_date), record_id)) > 0
        
        if success:
            # 更新图书可用数量
            self.book_manager.update_availability(record_data['book_id'], decrease=False)
            print("✓ 还书成功！")
            return True
        
        return False
    
    def get_borrow_record(self, record_id: int) -> Optional[BorrowRecord]:
        """根据ID获取借阅记录"""
        query = "SELECT * FROM borrow_records WHERE record_id = %s"
        data = self.db.fetch_one(query, (record_id,))
        if data:
            return self._dict_to_record(data)
        return None
    
    def get_reader_borrows(self, reader_id: int, active_only: bool = False) -> List[BorrowRecord]:
        """获取读者的借阅记录"""
        if active_only:
            query = '''
                SELECT br.*, b.title as book_title, r.name as reader_name
                FROM borrow_records br
                JOIN books b ON br.book_id = b.book_id
                JOIN readers r ON br.reader_id = r.reader_id
                WHERE br.reader_id = %s AND br.status = 'borrowed'
                ORDER BY br.borrow_date DESC
            '''
        else:
            query = '''
                SELECT br.*, b.title as book_title, r.name as reader_name
                FROM borrow_records br
                JOIN books b ON br.book_id = b.book_id
                JOIN readers r ON br.reader_id = r.reader_id
                WHERE br.reader_id = %s
                ORDER BY br.borrow_date DESC
            '''
        
        results = self.db.fetch_all(query, (reader_id,))
        return [self._dict_to_record(data) for data in results]
    
    def get_book_borrows(self, book_id: int) -> List[BorrowRecord]:
        """获取图书的借阅记录"""
        query = '''
            SELECT br.*, b.title as book_title, r.name as reader_name
            FROM borrow_records br
            JOIN books b ON br.book_id = b.book_id
            JOIN readers r ON br.reader_id = r.reader_id
            WHERE br.book_id = %s
            ORDER BY br.borrow_date DESC
        '''
        results = self.db.fetch_all(query, (book_id,))
        return [self._dict_to_record(data) for data in results]
    
    def get_overdue_books(self) -> List[dict]:
        """获取超期未还的图书"""
        query = '''
            SELECT br.*, b.title as book_title, b.isbn, r.name as reader_name, r.phone
            FROM borrow_records br
            JOIN books b ON br.book_id = b.book_id
            JOIN readers r ON br.reader_id = r.reader_id
            WHERE br.status = 'borrowed' AND br.due_date < CURDATE()
            ORDER BY br.due_date ASC
        '''
        return self.db.fetch_all(query)
    
    def get_statistics(self) -> dict:
        """获取借阅统计信息"""
        stats = {}
        
        # 总借阅次数
        query = "SELECT COUNT(*) as total FROM borrow_records"
        result = self.db.fetch_one(query)
        stats['total_borrows'] = result['total'] if result else 0
        
        # 当前借出数量
        query = "SELECT COUNT(*) as count FROM borrow_records WHERE status = 'borrowed'"
        result = self.db.fetch_one(query)
        stats['current_borrows'] = result['count'] if result else 0
        
        # 超期数量
        query = '''
            SELECT COUNT(*) as count FROM borrow_records 
            WHERE status = 'borrowed' AND due_date < CURDATE()
        '''
        result = self.db.fetch_one(query)
        stats['overdue_count'] = result['count'] if result else 0
        
        # 热门图书TOP 10
        query = '''
            SELECT b.title, b.author, COUNT(br.record_id) as borrow_count
            FROM borrow_records br
            JOIN books b ON br.book_id = b.book_id
            GROUP BY br.book_id
            ORDER BY borrow_count DESC
            LIMIT 10
        '''
        stats['popular_books'] = self.db.fetch_all(query)
        
        # 活跃读者TOP 10
        query = '''
            SELECT r.name, r.phone, COUNT(br.record_id) as borrow_count
            FROM borrow_records br
            JOIN readers r ON br.reader_id = r.reader_id
            GROUP BY br.reader_id
            ORDER BY borrow_count DESC
            LIMIT 10
        '''
        stats['active_readers'] = self.db.fetch_all(query)
        
        return stats
    
    def _dict_to_record(self, data: dict) -> BorrowRecord:
        """将字典转换为BorrowRecord对象"""
        return BorrowRecord(
            record_id=data['record_id'],
            book_id=data['book_id'],
            reader_id=data['reader_id'],
            borrow_date=str(data.get('borrow_date', '')),
            due_date=str(data.get('due_date', '')),
            return_date=str(data.get('return_date')) if data.get('return_date') else None,
            status=data['status'],
            created_at=str(data.get('created_at', '')),
            updated_at=str(data.get('updated_at', ''))
        )
