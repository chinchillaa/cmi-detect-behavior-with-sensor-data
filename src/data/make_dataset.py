"""
CMI BFRB検出のためのデータ前処理パイプライン。

このモジュールは生センサーデータの読み込み、クリーニング、前処理を担当します。
"""

import os
import sys
import logging
from pathlib import Path
from typing import Tuple, Optional, Dict, Any

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import yaml

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

def setup_logging(level: str = "INFO") -> None:
    """ログ設定をセットアップします。"""
    logging.basicConfig(
        level=getattr(logging, level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def load_config(config_path: str = "config/config.yaml") -> Dict[str, Any]:
    """YAMLファイルから設定を読み込みます。"""
    config_path = project_root / config_path
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def load_raw_data(data_dir: str) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    データディレクトリから生データファイルを読み込みます。
    
    Args:
        data_dir: 生データファイルを含むディレクトリのパス
        
    Returns:
        (train_df, test_df, sample_submission_df)のタプル
    """
    data_path = Path(data_dir)
    
    # データ構造を理解するためディレクトリ内の全ファイルをリスト
    files = list(data_path.glob("*"))
    logging.info(f"Found files in {data_dir}: {[f.name for f in files]}")
    
    # コンペティションの実際のファイル名に基づいて更新
    train_file = data_path / "train.csv"  # 実際のファイル名で更新
    test_file = data_path / "test.csv"    # 実際のファイル名で更新
    sample_sub_file = data_path / "sample_submission.csv"  # 実際のファイル名で更新
    
    # データを読み込み（実際のデータ形式に基づいて更新）
    if train_file.exists():
        train_df = pd.read_csv(train_file)
        logging.info(f"Loaded train data: {train_df.shape}")
    else:
        logging.warning(f"Train file not found: {train_file}")
        train_df = pd.DataFrame()
    
    if test_file.exists():
        test_df = pd.read_csv(test_file)
        logging.info(f"Loaded test data: {test_df.shape}")
    else:
        logging.warning(f"Test file not found: {test_file}")
        test_df = pd.DataFrame()
    
    if sample_sub_file.exists():
        sample_sub_df = pd.read_csv(sample_sub_file)
        logging.info(f"Loaded sample submission: {sample_sub_df.shape}")
    else:
        logging.warning(f"Sample submission file not found: {sample_sub_file}")
        sample_sub_df = pd.DataFrame()
    
    return train_df, test_df, sample_sub_df

def basic_data_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    """
    基本的なデータクリーニング操作を実行します。
    
    Args:
        df: 入力データフレーム
        
    Returns:
        クリーニング済みデータフレーム
    """
    # 元データの変更を避けるためコピーを作成
    df_clean = df.copy()
    
    # データの基本情報
    logging.info(f"Data shape: {df_clean.shape}")
    logging.info(f"Data types: {df_clean.dtypes.value_counts().to_dict()}")
    logging.info(f"Missing values: {df_clean.isnull().sum().sum()}")
    
    # 欠損値の処理（戦略はデータに依存）
    if df_clean.isnull().sum().sum() > 0:
        logging.info("Handling missing values...")
        # センサーデータの場合、前方埋めや補間を使用する可能性
        # df_clean = df_clean.fillna(method='ffill')
        # df_clean = df_clean.interpolate()
    
    # 重複の削除
    before_count = len(df_clean)
    df_clean = df_clean.drop_duplicates()
    after_count = len(df_clean)
    if before_count != after_count:
        logging.info(f"Removed {before_count - after_count} duplicate rows")
    
    return df_clean

def create_time_windows(df: pd.DataFrame, 
                       window_size: int = 1000, 
                       stride: int = 500,
                       time_column: str = 'timestamp',
                       feature_columns: Optional[list] = None) -> pd.DataFrame:
    """
    連続センサーデータからスライディング時間窓を作成します。
    
    Args:
        df: 時系列データを含む入力データフレーム
        window_size: 窓あたりのサンプル数
        stride: 窓間のステップサイズ
        time_column: タイムスタンプ列名
        feature_columns: 含める特徴量列のリスト
        
    Returns:
        窓特徴量を持つデータフレーム
    """
    if feature_columns is None:
        # 時間列以外の全数値列が特徴量と仮定
        feature_columns = df.select_dtypes(include=[np.number]).columns.tolist()
        if time_column in feature_columns:
            feature_columns.remove(time_column)
    
    windows = []
    
    # タイムスタンプ列が存在する場合は時間でソート
    if time_column in df.columns:
        df = df.sort_values(time_column)
    
    # スライディング窓を作成
    for start_idx in range(0, len(df) - window_size + 1, stride):
        end_idx = start_idx + window_size
        window_data = df.iloc[start_idx:end_idx]
        
        # 窓から特徴量を抽出
        window_features = {}
        
        for col in feature_columns:
            # 基本統計特徴量
            window_features[f'{col}_mean'] = window_data[col].mean()
            window_features[f'{col}_std'] = window_data[col].std()
            window_features[f'{col}_min'] = window_data[col].min()
            window_features[f'{col}_max'] = window_data[col].max()
            window_features[f'{col}_skew'] = window_data[col].skew()
            window_features[f'{col}_kurtosis'] = window_data[col].kurtosis()
        
        # 窓メタデータを追加
        window_features['window_start'] = start_idx
        window_features['window_end'] = end_idx
        
        windows.append(window_features)
    
    return pd.DataFrame(windows)

def split_data(df: pd.DataFrame, 
               target_column: str,
               test_size: float = 0.2,
               val_size: float = 0.2,
               random_state: int = 42) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    データを訓練、検証、テストセットに分割します。
    
    Args:
        df: 入力データフレーム
        target_column: ターゲット列名
        test_size: テストセットの割合
        val_size: 検証セットの割合（残りデータから）
        random_state: ランダムシード
        
    Returns:
        (train_df, val_df, test_df)のタプル
    """
    # 特徴量とターゲットを分離
    X = df.drop(columns=[target_column])
    y = df[target_column]
    
    # 第一分割：テストセットを分離
    X_temp, X_test, y_temp, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    # 第二分割：訓練と検証を分離
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp, test_size=val_size, random_state=random_state, stratify=y_temp
    )
    
    # データフレームに再結合
    train_df = pd.concat([X_train, y_train], axis=1)
    val_df = pd.concat([X_val, y_val], axis=1)
    test_df = pd.concat([X_test, y_test], axis=1)
    
    logging.info(f"Data split - Train: {len(train_df)}, Val: {len(val_df)}, Test: {len(test_df)}")
    
    return train_df, val_df, test_df

def save_processed_data(train_df: pd.DataFrame,
                       val_df: pd.DataFrame,
                       test_df: pd.DataFrame,
                       output_dir: str) -> None:
    """処理済みデータをファイルに保存します。"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    train_df.to_csv(output_path / "train_processed.csv", index=False)
    val_df.to_csv(output_path / "val_processed.csv", index=False)
    test_df.to_csv(output_path / "test_processed.csv", index=False)
    
    logging.info(f"Saved processed data to {output_dir}")

def main():
    """メインデータ処理パイプライン。"""
    setup_logging()
    
    # 設定を読み込み
    config = load_config()
    
    # 生データを読み込み
    data_dir = project_root / config['data']['raw_dir']
    train_df, test_df, sample_sub_df = load_raw_data(data_dir)
    
    if train_df.empty:
        logging.error("No training data found. Please download the competition data first.")
        return
    
    # 基本データ探索
    logging.info("=== Data Exploration ===")
    logging.info(f"Train data shape: {train_df.shape}")
    logging.info(f"Train data columns: {train_df.columns.tolist()}")
    logging.info(f"Train data info:\n{train_df.info()}")
    
    # データをクリーニング
    logging.info("=== Data Cleaning ===")
    train_clean = basic_data_cleaning(train_df)
    
    # TODO: 実際のデータ構造に基づいて更新
    # これはプレースホルダー - コンペティションデータ形式に基づいて更新
    logging.info("=== Feature Engineering ===")
    # processed_df = create_time_windows(
    #     train_clean,
    #     window_size=config['data']['window_size'],
    #     stride=config['data']['stride']
    # )
    
    # 今のところクリーニング済みデータをそのまま使用
    processed_df = train_clean
    
    # データ分割（実際のデータに基づいてターゲット列名を更新）
    if 'target' in processed_df.columns:  # 実際のターゲット列名で更新
        logging.info("=== Data Splitting ===")
        train_split, val_split, test_split = split_data(
            processed_df,
            target_column='target',  # 実際のターゲット列名で更新
            test_size=config['data']['test_split'],
            val_size=config['data']['validation_split'],
            random_state=config['data']['random_state']
        )
        
        # 処理済みデータを保存
        output_dir = project_root / config['data']['processed_dir']
        save_processed_data(train_split, val_split, test_split, output_dir)
    else:
        logging.warning("Target column not found. Saving cleaned data without splitting.")
        output_dir = project_root / config['data']['processed_dir']
        output_dir.mkdir(parents=True, exist_ok=True)
        processed_df.to_csv(output_dir / "train_cleaned.csv", index=False)
    
    logging.info("Data preprocessing completed!")

if __name__ == "__main__":
    main()