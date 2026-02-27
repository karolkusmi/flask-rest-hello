from __future__ import annotations

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    favorite_planets: Mapped[list["FavoritePlanet"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    favorite_characters: Mapped[list["FavoriteCharacter"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            
        }


class Planet(db.Model):
    __tablename__ = "planet"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    climate: Mapped[str] = mapped_column(String(80), nullable=True)
    terrain: Mapped[str] = mapped_column(String(80), nullable=True)
    population: Mapped[int | None]

    favorites: Mapped[list["FavoritePlanet"]] = relationship(
        back_populates="planet", cascade="all, delete-orphan"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain,
            "population": self.population,
        }


class Character(db.Model):
    __tablename__ = "character"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    gender: Mapped[str | None] = mapped_column(String(20), nullable=True)
    birth_year: Mapped[str | None] = mapped_column(String(20), nullable=True)
    eye_color: Mapped[str | None] = mapped_column(String(20), nullable=True)
    hair_color: Mapped[str | None] = mapped_column(String(20), nullable=True)
    skin_color: Mapped[str | None] = mapped_column(String(20), nullable=True)
    height: Mapped[int | None]

    homeworld_id: Mapped[int | None] = mapped_column(ForeignKey("planet.id"))
    homeworld: Mapped[Planet | None] = relationship("Planet")

    favorites: Mapped[list["FavoriteCharacter"]] = relationship(
        back_populates="character", cascade="all, delete-orphan"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "birth_year": self.birth_year,
            "eye_color": self.eye_color,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "height": self.height,
            "homeworld_id": self.homeworld_id,
        }


class FavoritePlanet(db.Model):
    __tablename__ = "favorite_planet"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"), nullable=False)

    user: Mapped[User] = relationship("User", back_populates="favorite_planets")
    planet: Mapped[Planet] = relationship("Planet", back_populates="favorites")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
        }


class FavoriteCharacter(db.Model):
    __tablename__ = "favorite_character"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    character_id: Mapped[int] = mapped_column(
        ForeignKey("character.id"), nullable=False
    )

    user: Mapped[User] = relationship("User", back_populates="favorite_characters")
    character: Mapped[Character] = relationship(
        "Character", back_populates="favorites"
    )

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
        }