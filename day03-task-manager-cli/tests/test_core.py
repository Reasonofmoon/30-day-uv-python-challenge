"""
Tests for Task Manager CLI
"""

import pytest
from src.task_manager_cli.core import TaskManagerCli, TaskManagerCliError


class TestTaskManagerCli:
    """Test class for TaskManagerCli"""
    
    @pytest.fixture
    def app(self):
        """Create test instance"""
        return TaskManagerCli()
    
    def test_initialization(self, app):
        """Test Task Manager CLI initialization"""
        assert app.initialized is True
        assert isinstance(app.data, dict)
    
    def test_run_success(self, app):
        """Test successful run"""
        result = app.run()
        assert result is True
        assert app.data.get('processed') is True
    
    def test_get_status(self, app):
        """Test status retrieval"""
        status = app.get_status()
        assert 'initialized' in status
        assert 'data_count' in status
        assert 'last_update' in status
        assert status['initialized'] is True
    
    def test_error_handling(self, app):
        """Test error handling"""
        # Test error scenarios here
        with pytest.raises(TaskManagerCliError):
            # Force an error condition
            app.data = None
            app._process()
    
    def test_process_functionality(self, app):
        """Test core processing"""
        result = app._process()
        assert result is True
        assert 'processed' in app.data
        assert app.data['processed'] is True


# Integration tests
def test_full_workflow():
    """Test complete workflow"""
    app = TaskManagerCli()
    
    # Test initialization
    assert app.initialized
    
    # Test run
    result = app.run()
    assert result
    
    # Test status
    status = app.get_status()
    assert status['initialized']
