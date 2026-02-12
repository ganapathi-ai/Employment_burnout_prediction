#!/usr/bin/env python3
# File: scripts/preprocessing.py

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
import joblib
import logging

logger = logging.getLogger(__name__)


class BurnoutPreprocessor:
    """Data preprocessing pipeline for burnout prediction"""

    def __init__(self):
        self.scaler = StandardScaler()
        self.preprocessor = None

    def load_data(self, filepath: str) -> pd.DataFrame:
        """Load transformed dataset"""
        df = pd.read_csv(filepath)
        logger.info(f"✓ Loaded {len(df)} records")
        return df

    def handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle missing values"""
        missing = df.isnull().sum()
        if missing.sum() > 0:
            logger.warning(f"Found {missing.sum()} missing values")
            df = df.fillna(df.mean(numeric_only=True))
        return df

    def create_target_variable(self, df: pd.DataFrame) -> tuple:
        """Create binary target: High Risk (1) vs Others (0)"""
        y = (df['burnout_risk'] == 'High').astype(int)
        X = df.drop(['burnout_risk', 'burnout_score'], axis=1)
        return X, y

    def split_features(self, df: pd.DataFrame):
        """Separate numerical and categorical features"""
        drop_cols = ['user_id']
        df = df.drop(columns=drop_cols, errors='ignore')
        categorical_features = ['day_type']
        numerical_features = [col for col in df.columns
                              if col not in categorical_features
                              and df[col].dtype != 'object']
        return numerical_features, categorical_features

    def create_preprocessing_pipeline(self, numerical_features: list,
                                      categorical_features: list):
        """Create preprocessing pipeline"""
        numerical_transformer = Pipeline(steps=[
            ('scaler', StandardScaler())
        ])
        categorical_transformer = Pipeline(steps=[
            ('onehot', OneHotEncoder(handle_unknown='ignore',
                                     sparse_output=False))
        ])
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', numerical_transformer, numerical_features),
                ('cat', categorical_transformer, categorical_features)
            ])
        logger.info(f"✓ Pipeline created with {len(numerical_features)} "
                    f"numerical and {len(categorical_features)} "
                    f"categorical features")
        return self.preprocessor

    def prepare_training_data(self, filepath: str,
                              test_size: float = 0.2):
        """Complete preprocessing pipeline"""
        df = self.load_data(filepath)
        df = self.handle_missing_values(df)
        X, y = self.create_target_variable(df)
        numerical_features, categorical_features = self.split_features(X)
        self.create_preprocessing_pipeline(numerical_features,
                                           categorical_features)
        X_processed = self.preprocessor.fit_transform(X)
        X_train, X_test, y_train, y_test = train_test_split(
            X_processed, y, test_size=test_size, random_state=42, stratify=y
        )
        logger.info(f"✓ Train: {X_train.shape}, Test: {X_test.shape}")
        return X_train, X_test, y_train, y_test, self.preprocessor

    def save_preprocessor(self,
                          filepath: str = 'models/preprocessor.joblib'):
        """Save preprocessing pipeline"""
        if self.preprocessor:
            joblib.dump(self.preprocessor, filepath)
            logger.info(f"✓ Preprocessor saved to {filepath}")


if __name__ == "__main__":
    preprocessor = BurnoutPreprocessor()
    X_train, X_test, y_train, y_test, _ = preprocessor.prepare_training_data(
        'data/work_from_home_burnout_dataset_transformed.csv'
    )
    preprocessor.save_preprocessor()
