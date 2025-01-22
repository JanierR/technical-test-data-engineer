from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

# Configuración de la base de datos
DATABASE_URI = "mssql+pyodbc://localhost/data_testing?driver=ODBC+Driver+17+for+SQL+Server"

# Conexión con la base de datos
engine = create_engine(DATABASE_URI, echo=True)

# Base para las tablas
Base = declarative_base()

# Definición de la tabla songs
class Song(Base):
    __tablename__ = 'songs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    artist = Column(String(255), nullable=False)
    genre = Column(String(100))
    duration = Column(Integer)
    release_date = Column(Date)

    def __repr__(self):
        return f"<Song(title={self.title}, artist={self.artist})>"

# Definición de la tabla users
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User(name={self.name}, email={self.email})>"

# Definición de la tabla listening_history
class ListeningHistory(Base):
    __tablename__ = 'listening_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    song_id = Column(Integer, ForeignKey('songs.id'), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", backref="listening_history")
    song = relationship("Song", backref="listening_history")

    def __repr__(self):
        return f"<ListeningHistory(user_id={self.user_id}, song_id={self.song_id})>"

# Crear las tablas en la base de datos
if __name__ == "__main__":
    # Crear las tablas en la base de datos
    Base.metadata.create_all(engine)
    print("Tablas creadas correctamente en SQL Server.")
