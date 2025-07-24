"""
Web Application Template

This template provides a standard structure for web applications
using FastAPI and modern Python practices.
"""

TEMPLATE_INFO = {
    "name": "Web Application",
    "description": "FastAPI web application template",
    "type": "web-app",
    "base_dependencies": ["fastapi", "uvicorn", "pydantic", "httpx", "pytest", "pytest-asyncio"],
    "python_version": ">=3.8"
}

DIRECTORY_STRUCTURE = [
    "src/{package_name}/__init__.py",
    "src/{package_name}/main.py",
    "src/{package_name}/api.py",
    "src/{package_name}/models.py",
    "src/{package_name}/database.py",
    "src/{package_name}/config.py",
    "tests/__init__.py",
    "tests/test_api.py",
    "tests/test_models.py",
    "tests/conftest.py",
    "pyproject.toml",
    "README.md",
    ".gitignore"
]

TEMPLATE_FILES = {
    "src/{package_name}/api.py": '''"""
FastAPI application and routes
"""

from fastapi import FastAPI, HTTPException, Depends
from typing import List, Optional
import logging

from .models import {class_name}Model, {class_name}Create, {class_name}Response
from .database import get_database

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="{project_name}",
    description="{description}",
    version="1.0.0"
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {{"message": "Welcome to {project_name} API", "status": "active"}}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {{"status": "healthy", "service": "{project_name}"}}


@app.post("/{package_name}/", response_model={class_name}Response)
async def create_item(item: {class_name}Create, db=Depends(get_database)):
    """Create a new item"""
    try:
        # Create item logic here
        new_item = {class_name}Model(**item.dict())
        
        # Save to database (placeholder)
        logger.info(f"Creating item: {{item.dict()}}")
        
        return {class_name}Response(
            id=1,
            message="Item created successfully",
            data=new_item
        )
    except Exception as e:
        logger.error(f"Error creating item: {{e}}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/{package_name}/{{item_id}}", response_model={class_name}Response)
async def get_item(item_id: int, db=Depends(get_database)):
    """Get item by ID"""
    try:
        # Get item logic here
        logger.info(f"Fetching item ID: {{item_id}}")
        
        # Placeholder item
        item = {class_name}Model(name=f"Item {{item_id}}", value="example")
        
        return {class_name}Response(
            id=item_id,
            message="Item retrieved successfully",
            data=item
        )
    except Exception as e:
        logger.error(f"Error fetching item {{item_id}}: {{e}}")
        raise HTTPException(status_code=404, detail="Item not found")


@app.get("/{package_name}/", response_model=List[{class_name}Response])
async def list_items(skip: int = 0, limit: int = 10, db=Depends(get_database)):
    """List all items with pagination"""
    try:
        logger.info(f"Listing items: skip={{skip}}, limit={{limit}}")
        
        # Placeholder items
        items = []
        for i in range(skip, skip + limit):
            item = {class_name}Model(name=f"Item {{i}}", value=f"value_{{i}}")
            items.append({class_name}Response(
                id=i,
                message="Item retrieved",
                data=item
            ))
        
        return items
    except Exception as e:
        logger.error(f"Error listing items: {{e}}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.put("/{package_name}/{{item_id}}", response_model={class_name}Response)
async def update_item(item_id: int, item: {class_name}Create, db=Depends(get_database)):
    """Update item by ID"""
    try:
        logger.info(f"Updating item {{item_id}}: {{item.dict()}}")
        
        # Update logic here
        updated_item = {class_name}Model(**item.dict())
        
        return {class_name}Response(
            id=item_id,
            message="Item updated successfully",
            data=updated_item
        )
    except Exception as e:
        logger.error(f"Error updating item {{item_id}}: {{e}}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/{package_name}/{{item_id}}")
async def delete_item(item_id: int, db=Depends(get_database)):
    """Delete item by ID"""
    try:
        logger.info(f"Deleting item {{item_id}}")
        
        # Delete logic here
        
        return {{"message": f"Item {{item_id}} deleted successfully"}}
    except Exception as e:
        logger.error(f"Error deleting item {{item_id}}: {{e}}")
        raise HTTPException(status_code=500, detail=str(e))
''',

    "src/{package_name}/models.py": '''"""
Pydantic models for data validation
"""

from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime


class {class_name}Base(BaseModel):
    """Base model for {class_name}"""
    name: str = Field(..., description="Name of the item")
    value: str = Field(..., description="Value of the item")


class {class_name}Create({class_name}Base):
    """Model for creating new items"""
    description: Optional[str] = Field(None, description="Optional description")


class {class_name}Model({class_name}Base):
    """Core model with all fields"""
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        """Pydantic configuration"""
        from_attributes = True
        json_encoders = {{
            datetime: lambda v: v.isoformat()
        }}


class {class_name}Response(BaseModel):
    """API response model"""
    id: int
    message: str
    data: {class_name}Model
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        """Pydantic configuration"""
        json_encoders = {{
            datetime: lambda v: v.isoformat()
        }}


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    detail: str
    timestamp: datetime = Field(default_factory=datetime.now)
''',

    "src/{package_name}/database.py": '''"""
Database connection and utilities
"""

import logging
from typing import Generator

# Configure logging
logger = logging.getLogger(__name__)


class DatabaseManager:
    """Database manager class"""
    
    def __init__(self):
        """Initialize database manager"""
        self.connected = False
        logger.info("Database manager initialized")
    
    def connect(self):
        """Connect to database"""
        # Database connection logic here
        self.connected = True
        logger.info("Connected to database")
    
    def disconnect(self):
        """Disconnect from database"""
        self.connected = False
        logger.info("Disconnected from database")
    
    def get_session(self):
        """Get database session"""
        if not self.connected:
            self.connect()
        
        # Return session object
        return self
    
    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.disconnect()


# Global database manager instance
db_manager = DatabaseManager()


def get_database() -> Generator[DatabaseManager, None, None]:
    """Dependency for getting database session"""
    try:
        yield db_manager.get_session()
    finally:
        # Cleanup if needed
        pass
''',

    "tests/test_api.py": '''"""
Tests for FastAPI application
"""

import pytest
from fastapi.testclient import TestClient
from src.{package_name}.api import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "status" in data


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_create_item():
    """Test creating an item"""
    item_data = {{
        "name": "Test Item",
        "value": "test_value",
        "description": "Test description"
    }}
    
    response = client.post("/{package_name}/", json=item_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "id" in data
    assert "message" in data
    assert "data" in data


def test_get_item():
    """Test getting an item"""
    response = client.get("/{package_name}/1")
    assert response.status_code == 200
    
    data = response.json()
    assert "id" in data
    assert "data" in data


def test_list_items():
    """Test listing items"""
    response = client.get("/{package_name}/")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)


def test_update_item():
    """Test updating an item"""
    item_data = {{
        "name": "Updated Item",
        "value": "updated_value"
    }}
    
    response = client.put("/{package_name}/1", json=item_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["message"] == "Item updated successfully"


def test_delete_item():
    """Test deleting an item"""
    response = client.delete("/{package_name}/1")
    assert response.status_code == 200
    
    data = response.json()
    assert "deleted successfully" in data["message"]


def test_pagination():
    """Test pagination parameters"""
    response = client.get("/{package_name}/?skip=5&limit=3")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) <= 3
'''
}


def generate_template(package_name: str, class_name: str, project_name: str, description: str) -> dict:
    """Generate template files with substitutions"""
    files = {}
    
    for file_path, content in TEMPLATE_FILES.items():
        # Substitute template variables
        formatted_content = content.format(
            package_name=package_name,
            class_name=class_name,
            project_name=project_name,
            description=description
        )
        
        # Format file path
        formatted_path = file_path.format(package_name=package_name)
        
        files[formatted_path] = formatted_content
    
    return files