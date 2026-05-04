from typing import List, Optional
from .models import Reader
from .database import Database


class ReaderManager:
    """读者管理类"""
    
    def __init__(self, db: Database):
        self.db = db
    
    def add_reader(self, reader: Reader) -> int:
        """添加读者"""
        query = '''
            INSERT INTO readers (name, phone, email, address)
            VALUES (%s, %s, %s, %s)
        '''
        params = (reader.name, reader.phone, reader.email, reader.address)
        return self.db.insert(query, params)
    
    def delete_reader(self, reader_id: int) -> bool:
        """删除读者"""
        query = "DELETE FROM readers WHERE reader_id = %s"
        return self.db.delete(query, (reader_id,)) > 0
    
    def update_reader(self, reader_id: int, **kwargs) -> bool:
        """更新读者信息"""
        if not kwargs:
            return False
        
        fields = []
        values = []
        for key, value in kwargs.items():
            fields.append(f"{key} = %s")
            values.append(value)
        
        values.append(reader_id)
        
        query = f"UPDATE readers SET {', '.join(fields)} WHERE reader_id = %s"
        return self.db.update(query, tuple(values)) > 0
    
    def get_reader_by_id(self, reader_id: int) -> Optional[Reader]:
        """根据ID获取读者"""
        query = "SELECT * FROM readers WHERE reader_id = %s"
        data = self.db.fetch_one(query, (reader_id,))
        if data:
            return self._dict_to_reader(data)
        return None
    
    def search_readers(self, keyword: str) -> List[Reader]:
        """搜索读者（支持姓名、电话、邮箱）"""
        query = '''
            SELECT * FROM readers 
            WHERE name LIKE %s OR phone LIKE %s OR email LIKE %s
            ORDER BY created_at DESC
        '''
        search_term = f"%{keyword}%"
        results = self.db.fetch_all(query, (search_term, search_term, search_term))
        return [self._dict_to_reader(data) for data in results]
    
    def get_all_readers(self, page: int = 1, page_size: int = 20) -> List[Reader]:
        """获取所有读者（分页）"""
        offset = (page - 1) * page_size
        query = "SELECT * FROM readers ORDER BY created_at DESC LIMIT %s OFFSET %s"
        results = self.db.fetch_all(query, (page_size, offset))
        return [self._dict_to_reader(data) for data in results]
    
    def get_total_count(self) -> int:
        """获取读者总数"""
        query = "SELECT COUNT(*) as count FROM readers"
        result = self.db.fetch_one(query)
        return result['count'] if result else 0
    
    def _dict_to_reader(self, data: dict) -> Reader:
        """将字典转换为Reader对象"""
        return Reader(
            reader_id=data['reader_id'],
            name=data['name'],
            phone=data.get('phone'),
            email=data.get('email'),
            address=data.get('address'),
            register_date=str(data.get('register_date', '')),
            created_at=str(data.get('created_at', '')),
            updated_at=str(data.get('updated_at', ''))
        )
