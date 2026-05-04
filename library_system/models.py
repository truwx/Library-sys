from dataclasses import dataclass
from typing import Optional


@dataclass
class Book:
    """图书模型"""
    title: str
    author: str
    isbn: str
    publisher: str
    publish_date: str
    category: str
    total_copies: int
    available_copies: int
    book_id: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def to_dict(self):
        return {
            'book_id': self.book_id,
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'publisher': self.publisher,
            'publish_date': self.publish_date,
            'category': self.category,
            'total_copies': self.total_copies,
            'available_copies': self.available_copies,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


@dataclass
class Reader:
    """读者模型"""
    name: str
    phone: str
    email: str
    address: str
    reader_id: Optional[int] = None
    register_date: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def to_dict(self):
        return {
            'reader_id': self.reader_id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'register_date': self.register_date,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


@dataclass
class BorrowRecord:
    """借阅记录模型"""
    book_id: int
    reader_id: int
    borrow_date: str
    due_date: str
    return_date: Optional[str] = None
    record_id: Optional[int] = None
    status: str = "borrowed"
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def to_dict(self):
        return {
            'record_id': self.record_id,
            'book_id': self.book_id,
            'reader_id': self.reader_id,
            'borrow_date': self.borrow_date,
            'due_date': self.due_date,
            'return_date': self.return_date,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
