"""
Data preprocessing module for exoplanet classification.
Implements robust preprocessing inspired by NASA's EMAC techniques.
"""

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.impute import SimpleImputer
import warnings
warnings.filterwarnings('ignore')


class ExoplanetDataPreprocessor:
    """
    Preprocessor for exoplanet data with advanced noise handling and artifact removal.
    """
    
    def __init__(self):
        self.scaler = RobustScaler()
        self.imputer = SimpleImputer(strategy='median')
        self.feature_names = None
        
    def remove_outliers(self, df, columns, threshold=3.5):
        """
        Remove outliers using modified Z-score method.
        More robust than standard deviation for skewed distributions.
        """
        df_clean = df.copy()
        
        for col in columns:
            if col in df_clean.columns:
                median = df_clean[col].median()
                mad = np.median(np.abs(df_clean[col] - median))
                if mad > 0:
                    modified_z_scores = 0.6745 * (df_clean[col] - median) / mad
                    df_clean = df_clean[np.abs(modified_z_scores) < threshold]
        
        return df_clean
    
    def handle_missing_values(self, df):
        """
        Handle missing values with intelligent imputation.
        """
        # For critical features, use median imputation
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = self.imputer.fit_transform(df[numeric_cols])
        
        return df
    
    def apply_log_transform(self, df, columns):
        """
        Apply log transformation to highly skewed features.
        """
        df_transformed = df.copy()
        
        for col in columns:
            if col in df_transformed.columns:
                # Add small constant to avoid log(0)
                min_val = df_transformed[col].min()
                if min_val <= 0:
                    df_transformed[col] = df_transformed[col] - min_val + 1e-10
                df_transformed[col] = np.log1p(df_transformed[col])
        
        return df_transformed
    
    def detect_and_remove_artifacts(self, df):
        """
        Detect and handle light curve artifacts and instrumental noise.
        Based on techniques from Osborn et al. (2022) MNRAS paper.
        """
        df_clean = df.copy()
        
        # Remove physically impossible values
        if 'orbital_period' in df_clean.columns:
            df_clean = df_clean[df_clean['orbital_period'] > 0]
        if 'transit_duration' in df_clean.columns:
            df_clean = df_clean[df_clean['transit_duration'] > 0]
        if 'transit_depth' in df_clean.columns:
            df_clean = df_clean[(df_clean['transit_depth'] > 0) & (df_clean['transit_depth'] < 1)]
        if 'stellar_temp' in df_clean.columns:
            df_clean = df_clean[(df_clean['stellar_temp'] > 2000) & (df_clean['stellar_temp'] < 50000)]
        if 'stellar_mass' in df_clean.columns:
            df_clean = df_clean[(df_clean['stellar_mass'] > 0.1) & (df_clean['stellar_mass'] < 100)]
        
        return df_clean
    
    def calculate_quality_metrics(self, df):
        """
        Calculate data quality metrics for filtering low-quality observations.
        """
        quality_scores = []
        
        for idx, row in df.iterrows():
            score = 1.0
            
            # SNR quality
            if 'snr' in row and row['snr'] < 7:
                score *= 0.7
            
            # Transit depth consistency
            if 'transit_depth' in row and 'snr' in row:
                expected_depth_uncertainty = 1.0 / row['snr']
                if row['transit_depth'] < expected_depth_uncertainty:
                    score *= 0.5
            
            quality_scores.append(score)
        
        df['quality_score'] = quality_scores
        return df
    
    def preprocess(self, df, fit=True):
        """
        Complete preprocessing pipeline.
        """
        # Store original feature names
        if fit:
            self.feature_names = df.columns.tolist()
        
        # Remove artifacts and physically impossible values
        df = self.detect_and_remove_artifacts(df)
        
        # Handle missing values
        df = self.handle_missing_values(df)
        
        # Apply log transform to skewed features
        log_transform_cols = ['orbital_period', 'transit_duration', 'transit_depth']
        log_transform_cols = [col for col in log_transform_cols if col in df.columns]
        df = self.apply_log_transform(df, log_transform_cols)
        
        # Remove outliers
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        df = self.remove_outliers(df, numeric_cols, threshold=4.0)
        
        # Calculate quality metrics
        if 'snr' in df.columns and 'transit_depth' in df.columns:
            df = self.calculate_quality_metrics(df)
        
        # Scale features
        numeric_cols = [col for col in df.columns if col != 'quality_score']
        if fit:
            df[numeric_cols] = self.scaler.fit_transform(df[numeric_cols])
        else:
            df[numeric_cols] = self.scaler.transform(df[numeric_cols])
        
        return df


def load_nasa_exoplanet_data():
    """
    Load NASA exoplanet data from the NASA Exoplanet Archive.
    Creates synthetic dataset based on real exoplanet distributions.
    """
    try:
        # Try to load from NASA Exoplanet Archive
        import requests
        url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+*+from+ps&format=csv"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            from io import StringIO
            df = pd.read_csv(StringIO(response.text))
            return df
    except:
        pass
    
    # Generate synthetic dataset based on Kepler/TESS distributions
    print("Generating synthetic training dataset based on Kepler/TESS statistics...")
    
    np.random.seed(42)
    n_samples = 5000
    
    # Create different classes with realistic distributions
    n_confirmed = int(n_samples * 0.3)
    n_candidate = int(n_samples * 0.35)
    n_false_positive = n_samples - n_confirmed - n_candidate
    
    data = []
    
    # Confirmed exoplanets (based on Kepler statistics)
    for _ in range(n_confirmed):
        orbital_period = np.random.lognormal(2.5, 1.5)  # Days
        stellar_mass = np.random.normal(1.0, 0.3)  # Solar masses
        stellar_temp = np.random.normal(5500, 800)  # Kelvin
        stellar_magnitude = np.random.normal(14, 2)
        
        # Calculate realistic transit parameters
        planet_radius = np.random.lognormal(0.5, 0.8)  # Earth radii
        transit_depth = (planet_radius * 0.00916) ** 2  # Relative to stellar radius
        transit_duration = np.random.normal(3, 1)  # Hours
        snr = np.random.lognormal(2.5, 0.7)  # Signal-to-noise ratio
        semi_major_axis = (orbital_period / 365.25) ** (2/3) * stellar_mass ** (1/3)  # AU
        planet_temp = stellar_temp * np.sqrt(1 / (2 * semi_major_axis)) * 0.01
        impact_parameter = np.random.uniform(0, 0.9)
        
        data.append({
            'orbital_period': max(0.5, orbital_period),
            'transit_duration': max(0.5, transit_duration),
            'transit_depth': max(0.0001, min(0.1, transit_depth)),
            'snr': max(5, snr),
            'stellar_mass': max(0.1, stellar_mass),
            'stellar_temp': max(3000, min(10000, stellar_temp)),
            'stellar_magnitude': max(8, min(20, stellar_magnitude)),
            'classification': 'confirmed_exoplanet',
            'planet_radius': planet_radius,
            'planet_temp': planet_temp,
            'semi_major_axis': semi_major_axis,
            'impact_parameter': impact_parameter
        })
    
    # Planetary candidates (similar but more uncertain)
    for _ in range(n_candidate):
        orbital_period = np.random.lognormal(2.5, 1.8)
        stellar_mass = np.random.normal(1.0, 0.4)
        stellar_temp = np.random.normal(5500, 1000)
        stellar_magnitude = np.random.normal(15, 2.5)
        
        planet_radius = np.random.lognormal(0.5, 1.0)
        transit_depth = (planet_radius * 0.00916) ** 2
        transit_duration = np.random.normal(3, 1.5)
        snr = np.random.lognormal(1.8, 0.8)  # Lower SNR
        semi_major_axis = (orbital_period / 365.25) ** (2/3) * stellar_mass ** (1/3)
        planet_temp = stellar_temp * np.sqrt(1 / (2 * semi_major_axis)) * 0.01
        impact_parameter = np.random.uniform(0, 0.95)
        
        data.append({
            'orbital_period': max(0.5, orbital_period),
            'transit_duration': max(0.5, transit_duration),
            'transit_depth': max(0.0001, min(0.1, transit_depth)),
            'snr': max(4, snr),
            'stellar_mass': max(0.1, stellar_mass),
            'stellar_temp': max(3000, min(10000, stellar_temp)),
            'stellar_magnitude': max(8, min(20, stellar_magnitude)),
            'classification': 'planetary_candidate',
            'planet_radius': planet_radius,
            'planet_temp': planet_temp,
            'semi_major_axis': semi_major_axis,
            'impact_parameter': impact_parameter
        })
    
    # False positives (eclipsing binaries, artifacts)
    for _ in range(n_false_positive):
        # False positives have different characteristics
        orbital_period = np.random.lognormal(2.0, 2.0)
        stellar_mass = np.random.normal(1.0, 0.5)
        stellar_temp = np.random.normal(5500, 1200)
        stellar_magnitude = np.random.normal(15.5, 3)
        
        # Larger transit depths (eclipsing binaries)
        transit_depth = np.random.lognormal(-4, 1.5)
        transit_duration = np.random.normal(4, 2)  # Often longer
        snr = np.random.lognormal(1.5, 1.0)  # Variable SNR
        
        data.append({
            'orbital_period': max(0.5, orbital_period),
            'transit_duration': max(0.5, transit_duration),
            'transit_depth': max(0.0001, min(0.3, transit_depth)),
            'snr': max(3, snr),
            'stellar_mass': max(0.1, stellar_mass),
            'stellar_temp': max(3000, min(10000, stellar_temp)),
            'stellar_magnitude': max(8, min(20, stellar_magnitude)),
            'classification': 'false_positive',
            'planet_radius': np.nan,
            'planet_temp': np.nan,
            'semi_major_axis': np.nan,
            'impact_parameter': np.nan
        })
    
    df = pd.DataFrame(data)
    return df


if __name__ == "__main__":
    # Test the preprocessing pipeline
    df = load_nasa_exoplanet_data()
    print(f"Loaded {len(df)} exoplanet observations")
    print(f"\nClass distribution:\n{df['classification'].value_counts()}")
    
    preprocessor = ExoplanetDataPreprocessor()
    df_processed = preprocessor.preprocess(df[['orbital_period', 'transit_duration', 
                                                'transit_depth', 'snr', 'stellar_mass', 
                                                'stellar_temp', 'stellar_magnitude']])
    print(f"\nAfter preprocessing: {len(df_processed)} samples")
