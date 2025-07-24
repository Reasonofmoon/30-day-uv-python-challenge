"""
Data Tool Template

This template provides a standard structure for data analysis
and processing tools using pandas and modern Python practices.
"""

TEMPLATE_INFO = {
    "name": "Data Analysis Tool",
    "description": "Data processing and analysis tool template",
    "type": "data-tool",
    "base_dependencies": ["pandas", "numpy", "matplotlib", "seaborn", "pytest", "pytest-cov"],
    "python_version": ">=3.8"
}

DIRECTORY_STRUCTURE = [
    "src/{package_name}/__init__.py",
    "src/{package_name}/main.py",
    "src/{package_name}/processor.py",
    "src/{package_name}/analyzer.py",
    "src/{package_name}/exporter.py",
    "src/{package_name}/visualizer.py",
    "tests/__init__.py",
    "tests/test_processor.py",
    "tests/test_analyzer.py",
    "tests/conftest.py",
    "data/",
    "output/",
    "pyproject.toml",
    "README.md",
    ".gitignore"
]

TEMPLATE_FILES = {
    "src/{package_name}/processor.py": '''"""
Data processing utilities
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataProcessor:
    """Main data processing class"""
    
    def __init__(self):
        """Initialize data processor"""
        self.data: Optional[pd.DataFrame] = None
        self.processed_data: Optional[pd.DataFrame] = None
        self.metadata: Dict = {{}}
        logger.info("DataProcessor initialized")
    
    def load_data(self, source: Union[str, pd.DataFrame], **kwargs) -> pd.DataFrame:
        """Load data from various sources"""
        try:
            if isinstance(source, str):
                # Load from file
                if source.endswith('.csv'):
                    self.data = pd.read_csv(source, **kwargs)
                elif source.endswith('.xlsx') or source.endswith('.xls'):
                    self.data = pd.read_excel(source, **kwargs)
                elif source.endswith('.json'):
                    self.data = pd.read_json(source, **kwargs)
                else:
                    raise ValueError(f"Unsupported file format: {{source}}")
            elif isinstance(source, pd.DataFrame):
                self.data = source.copy()
            else:
                raise ValueError(f"Unsupported data source type: {{type(source)}}")
            
            # Store metadata
            self.metadata['rows'] = len(self.data)
            self.metadata['columns'] = len(self.data.columns)
            self.metadata['memory_usage'] = self.data.memory_usage(deep=True).sum()
            
            logger.info(f"Loaded data: {{self.metadata['rows']}} rows, {{self.metadata['columns']}} columns")
            return self.data
            
        except Exception as e:
            logger.error(f"Error loading data: {{e}}")
            raise
    
    def clean_data(self) -> pd.DataFrame:
        """Clean and preprocess data"""
        if self.data is None:
            raise ValueError("No data loaded. Call load_data() first.")
        
        try:
            # Create copy for processing
            cleaned_data = self.data.copy()
            
            # Remove duplicates
            duplicates_before = len(cleaned_data)
            cleaned_data = cleaned_data.drop_duplicates()
            duplicates_removed = duplicates_before - len(cleaned_data)
            
            # Handle missing values
            missing_before = cleaned_data.isnull().sum().sum()
            cleaned_data = cleaned_data.fillna(method='forward').fillna(method='backward')
            missing_after = cleaned_data.isnull().sum().sum()
            
            # Store processed data
            self.processed_data = cleaned_data
            
            # Update metadata
            self.metadata['duplicates_removed'] = duplicates_removed
            self.metadata['missing_values_before'] = missing_before
            self.metadata['missing_values_after'] = missing_after
            
            logger.info(f"Data cleaned: {{duplicates_removed}} duplicates removed, {{missing_before - missing_after}} missing values handled")
            return self.processed_data
            
        except Exception as e:
            logger.error(f"Error cleaning data: {{e}}")
            raise
    
    def transform_data(self, transformations: List[Dict]) -> pd.DataFrame:
        """Apply transformations to data"""
        if self.processed_data is None:
            raise ValueError("No processed data available. Call clean_data() first.")
        
        try:
            transformed_data = self.processed_data.copy()
            
            for transform in transformations:
                operation = transform.get('operation')
                column = transform.get('column')
                
                if operation == 'normalize':
                    # Normalize column to 0-1 range
                    transformed_data[column] = (transformed_data[column] - transformed_data[column].min()) / (transformed_data[column].max() - transformed_data[column].min())
                
                elif operation == 'standardize':
                    # Standardize column (z-score)
                    transformed_data[column] = (transformed_data[column] - transformed_data[column].mean()) / transformed_data[column].std()
                
                elif operation == 'log_transform':
                    # Log transformation
                    transformed_data[column] = np.log1p(transformed_data[column])
                
                # Add more transformations as needed
            
            self.processed_data = transformed_data
            logger.info(f"Applied {{len(transformations)}} transformations")
            return self.processed_data
            
        except Exception as e:
            logger.error(f"Error transforming data: {{e}}")
            raise
    
    def get_summary(self) -> Dict:
        """Get data summary statistics"""
        if self.data is None:
            return {{"error": "No data loaded"}}
        
        summary = {{
            "basic_info": self.metadata,
            "data_types": self.data.dtypes.to_dict(),
            "summary_stats": self.data.describe().to_dict(),
            "missing_values": self.data.isnull().sum().to_dict()
        }}
        
        return summary
''',

    "src/{package_name}/analyzer.py": '''"""
Data analysis utilities
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging

# Configure logging
logger = logging.getLogger(__name__)


class DataAnalyzer:
    """Data analysis class"""
    
    def __init__(self, data: Optional[pd.DataFrame] = None):
        """Initialize analyzer with optional data"""
        self.data = data
        self.analysis_results: Dict = {{}}
        logger.info("DataAnalyzer initialized")
    
    def set_data(self, data: pd.DataFrame):
        """Set data for analysis"""
        self.data = data
        logger.info(f"Data set for analysis: {{len(data)}} rows, {{len(data.columns)}} columns")
    
    def correlation_analysis(self, method: str = 'pearson') -> pd.DataFrame:
        """Perform correlation analysis"""
        if self.data is None:
            raise ValueError("No data available for analysis")
        
        try:
            # Select only numeric columns
            numeric_columns = self.data.select_dtypes(include=[np.number]).columns
            
            if len(numeric_columns) < 2:
                raise ValueError("Need at least 2 numeric columns for correlation analysis")
            
            correlations = self.data[numeric_columns].corr(method=method)
            self.analysis_results['correlations'] = correlations
            
            logger.info(f"Correlation analysis completed using {{method}} method")
            return correlations
            
        except Exception as e:
            logger.error(f"Error in correlation analysis: {{e}}")
            raise
    
    def outlier_detection(self, columns: Optional[List[str]] = None, method: str = 'iqr') -> Dict:
        """Detect outliers in data"""
        if self.data is None:
            raise ValueError("No data available for analysis")
        
        try:
            if columns is None:
                columns = self.data.select_dtypes(include=[np.number]).columns.tolist()
            
            outliers = {{}}
            
            for column in columns:
                if method == 'iqr':
                    Q1 = self.data[column].quantile(0.25)
                    Q3 = self.data[column].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    
                    outlier_mask = (self.data[column] < lower_bound) | (self.data[column] > upper_bound)
                    outliers[column] = {{
                        'count': outlier_mask.sum(),
                        'percentage': (outlier_mask.sum() / len(self.data)) * 100,
                        'indices': self.data[outlier_mask].index.tolist()
                    }}
                
                elif method == 'zscore':
                    z_scores = np.abs((self.data[column] - self.data[column].mean()) / self.data[column].std())
                    outlier_mask = z_scores > 3
                    
                    outliers[column] = {{
                        'count': outlier_mask.sum(),
                        'percentage': (outlier_mask.sum() / len(self.data)) * 100,
                        'indices': self.data[outlier_mask].index.tolist()
                    }}
            
            self.analysis_results['outliers'] = outliers
            logger.info(f"Outlier detection completed for {{len(columns)}} columns using {{method}} method")
            return outliers
            
        except Exception as e:
            logger.error(f"Error in outlier detection: {{e}}")
            raise
    
    def trend_analysis(self, time_column: str, value_column: str) -> Dict:
        """Analyze trends in time series data"""
        if self.data is None:
            raise ValueError("No data available for analysis")
        
        try:
            # Ensure time column is datetime
            self.data[time_column] = pd.to_datetime(self.data[time_column])
            
            # Sort by time
            data_sorted = self.data.sort_values(time_column)
            
            # Calculate basic trend statistics
            values = data_sorted[value_column]
            trend_results = {{
                'mean': values.mean(),
                'std': values.std(),
                'min': values.min(),
                'max': values.max(),
                'trend_direction': 'increasing' if values.iloc[-1] > values.iloc[0] else 'decreasing',
                'volatility': values.std() / values.mean() if values.mean() != 0 else 0
            }}
            
            # Calculate moving averages
            data_sorted['ma_7'] = values.rolling(window=7).mean()
            data_sorted['ma_30'] = values.rolling(window=30).mean()
            
            self.analysis_results['trend'] = trend_results
            logger.info(f"Trend analysis completed for {{value_column}} over time")
            return trend_results
            
        except Exception as e:
            logger.error(f"Error in trend analysis: {{e}}")
            raise
    
    def segment_analysis(self, segment_column: str, metric_columns: List[str]) -> Dict:
        """Analyze data by segments"""
        if self.data is None:
            raise ValueError("No data available for analysis")
        
        try:
            segments = {{}}
            
            for segment in self.data[segment_column].unique():
                segment_data = self.data[self.data[segment_column] == segment]
                
                segment_metrics = {{
                    'count': len(segment_data),
                    'percentage': (len(segment_data) / len(self.data)) * 100
                }}
                
                for metric in metric_columns:
                    if metric in segment_data.columns:
                        segment_metrics[metric] = {{
                            'mean': segment_data[metric].mean(),
                            'median': segment_data[metric].median(),
                            'std': segment_data[metric].std()
                        }}
                
                segments[segment] = segment_metrics
            
            self.analysis_results['segments'] = segments
            logger.info(f"Segment analysis completed for {{len(segments)}} segments")
            return segments
            
        except Exception as e:
            logger.error(f"Error in segment analysis: {{e}}")
            raise
    
    def get_insights(self) -> List[str]:
        """Generate insights from analysis results"""
        insights = []
        
        if 'correlations' in self.analysis_results:
            corr = self.analysis_results['correlations']
            # Find strong correlations
            strong_corr = []
            for i in range(len(corr.columns)):
                for j in range(i+1, len(corr.columns)):
                    corr_value = corr.iloc[i, j]
                    if abs(corr_value) > 0.7:
                        strong_corr.append(f"{{corr.columns[i]}} and {{corr.columns[j]}}: {{corr_value:.3f}}")
            
            if strong_corr:
                insights.append(f"Strong correlations found: {{', '.join(strong_corr)}}")
        
        if 'outliers' in self.analysis_results:
            outlier_columns = [col for col, info in self.analysis_results['outliers'].items() if info['count'] > 0]
            if outlier_columns:
                insights.append(f"Outliers detected in columns: {{', '.join(outlier_columns)}}")
        
        return insights
''',

    "tests/test_processor.py": '''"""
Tests for data processor
"""

import pytest
import pandas as pd
import numpy as np
from src.{package_name}.processor import DataProcessor


class TestDataProcessor:
    """Test class for DataProcessor"""
    
    @pytest.fixture
    def processor(self):
        """Create processor instance"""
        return DataProcessor()
    
    @pytest.fixture
    def sample_data(self):
        """Create sample test data"""
        return pd.DataFrame({{
            'A': [1, 2, 3, 4, 5, 1],  # Has duplicate
            'B': [10, 20, np.nan, 40, 50, 60],  # Has missing value
            'C': ['x', 'y', 'z', 'x', 'y', 'z']
        }})
    
    def test_load_data_from_dataframe(self, processor, sample_data):
        """Test loading data from DataFrame"""
        result = processor.load_data(sample_data)
        
        assert result is not None
        assert len(result) == 6
        assert processor.metadata['rows'] == 6
        assert processor.metadata['columns'] == 3
    
    def test_clean_data(self, processor, sample_data):
        """Test data cleaning"""
        processor.load_data(sample_data)
        cleaned = processor.clean_data()
        
        assert cleaned is not None
        assert processor.metadata['duplicates_removed'] == 1
        assert cleaned.isnull().sum().sum() == 0  # No missing values after cleaning
    
    def test_transform_data(self, processor, sample_data):
        """Test data transformation"""
        processor.load_data(sample_data)
        processor.clean_data()
        
        transformations = [
            {{'operation': 'normalize', 'column': 'A'}},
            {{'operation': 'standardize', 'column': 'B'}}
        ]
        
        transformed = processor.transform_data(transformations)
        
        assert transformed is not None
        # Check if normalization worked (values should be between 0 and 1)
        assert transformed['A'].min() >= 0
        assert transformed['A'].max() <= 1
    
    def test_get_summary(self, processor, sample_data):
        """Test summary generation"""
        processor.load_data(sample_data)
        summary = processor.get_summary()
        
        assert 'basic_info' in summary
        assert 'data_types' in summary
        assert 'summary_stats' in summary
        assert 'missing_values' in summary
    
    def test_no_data_error(self, processor):
        """Test error when no data is loaded"""
        with pytest.raises(ValueError, match="No data loaded"):
            processor.clean_data()
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