from sqlalchemy import Column, Integer, String, Float, ForeignKey, UniqueConstraint, Date
from sqlalchemy.orm import relationship, validates
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

ALLOWED_UNITS = {"grams", "ml", "pcs"}

class Ingredient(Base):
    __tablename__ = "ingredients"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    unit = Column(String, nullable=False)

    inventory = relationship("Inventory", uselist=False, back_populates="ingredient")
    recipe_ingredients = relationship("RecipeIngredient", back_populates="ingredient")

    @validates('unit')
    def validate_unit(self, key, unit):
        if unit not in ALLOWED_UNITS:
            raise ValueError(f"Invalid unit '{unit}'. Allowed units: {ALLOWED_UNITS}")
        return unit

    def __repr__(self):
        return f"<Ingredient(name={self.name}, unit={self.unit})>"


class Inventory(Base):
    __tablename__ = "inventory"
    id = Column(Integer, primary_key=True)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), unique=True, nullable=False)
    quantity_in_stock = Column(Float, nullable=False)
    unit = Column(String, nullable=False)

    ingredient = relationship("Ingredient", back_populates="inventory")

    @validates('quantity_in_stock')
    def validate_quantity(self, key, quantity):
        if quantity < 0:
            raise ValueError("Quantity in stock cannot be negative")
        return quantity

    @validates('unit')
    def validate_unit(self, key, unit):
        if unit not in ALLOWED_UNITS:
            raise ValueError(f"Invalid unit '{unit}'. Allowed units: {ALLOWED_UNITS}")
        return unit

    def __repr__(self):
        return f"<Inventory(ingredient={self.ingredient.name}, qty={self.quantity_in_stock} {self.unit})>"


class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)

    recipe_ingredients = relationship("RecipeIngredient", back_populates="recipe")
    meal_plans = relationship("MealPlan", back_populates="recipe")

    def __repr__(self):
        return f"<Recipe(name={self.name})>"


class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"
    id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), nullable=False)
    quantity_needed = Column(Float, nullable=False)
    unit = Column(String, nullable=False)

    recipe = relationship("Recipe", back_populates="recipe_ingredients")
    ingredient = relationship("Ingredient", back_populates="recipe_ingredients")

    __table_args__ = (UniqueConstraint("recipe_id", "ingredient_id"),)

    @validates('quantity_needed')
    def validate_quantity(self, key, quantity):
        if quantity <= 0:
            raise ValueError("Quantity needed must be positive")
        return quantity

    @validates('unit')
    def validate_unit(self, key, unit):
        if unit not in ALLOWED_UNITS:
            raise ValueError(f"Invalid unit '{unit}'. Allowed units: {ALLOWED_UNITS}")
        return unit

    def __repr__(self):
        return f"<RecipeIngredient(recipe={self.recipe.name}, ingredient={self.ingredient.name}, qty={self.quantity_needed} {self.unit})>"


class MealPlan(Base):
    __tablename__ = "meal_plans"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)

    recipe = relationship("Recipe", back_populates="meal_plans")

    __table_args__ = (UniqueConstraint("date", "recipe_id"),)

    def __repr__(self):
        return f"<MealPlan(date={self.date}, recipe={self.recipe.name})>"
