#!/usr/bin/env python3
# File: scripts/data_ingestion.py

import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import logging
from typing import Optional

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


class PostgresDataStore:
    """Manages database connections and data operations with connection pooling"""

    def __init__(self, db_url: Optional[str] = None, pool_size: int = 5):
        self.db_url = db_url or os.getenv('DATABASE_URL')
        if not self.db_url:
            raise ValueError("DATABASE_URL not set in environment")

        self.engine = create_engine(
            self.db_url,
            pool_size=pool_size,
            max_overflow=pool_size * 2,
            pool_pre_ping=True,
            echo=False,
        )
        logger.info("Database connection pool initialized")

    def load_csv_to_postgres(self, csv_path: str, table_name: str = 'burnout_records'):
        """Load CSV data into Postgres table"""
        try:
            import pandas as pd

            df = pd.read_csv(csv_path)
            logger.info(f"Loaded {len(df)} records from {csv_path}")

            self._validate_data(df)

            with self.engine.connect() as conn:
                df.to_sql(table_name, conn, if_exists='append', index=False)
                conn.commit()

            logger.info(f"Successfully loaded {len(df)} records to {table_name}")
            return True

        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise

    def _validate_data(self, df):
        """Validate data quality before insertion"""
        required_cols = ['user_id', 'day_type', 'work_hours', 'sleep_hours', 'burnout_score']
        missing = [col for col in required_cols if col not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")

        nulls = df[required_cols].isnull().sum()
        if nulls.sum() > 0:
            logger.warning(f"Null values found: {nulls[nulls > 0].to_dict()}")

        assert df['work_hours'].min() >= 0, "work_hours must be >= 0"
        assert df['sleep_hours'].min() >= 0, "sleep_hours must be >= 0"

        logger.info("Data validation passed")

    def test_connection(self) -> bool:
        """Test database connection"""
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                logger.info("Database connection test passed")
                return True
        except Exception as e:
            logger.error(f"Connection test failed: {str(e)}")
            return False

    def get_sample_data(self, limit: int = 10):
        """Retrieve sample data from database"""
        import pandas as pd

        query = f"SELECT * FROM burnout_records LIMIT {limit}"
        return pd.read_sql(query, self.engine)


if __name__ == "__main__":
    store = PostgresDataStore()
    store.test_connection()
