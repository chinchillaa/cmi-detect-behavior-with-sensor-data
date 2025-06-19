#!/usr/bin/env python3
"""
Kaggle提出用のモデル準備スクリプト

このスクリプトは、学習済みモデルをKaggleデータセットとして
アップロードするための準備を行います。
"""

import shutil
from pathlib import Path
import json

def prepare_model_for_kaggle():
    """モデルファイルをKaggle提出用に準備"""
    
    # パス設定
    project_root = Path("/home/chinchilla/kaggle/pjt/cmi-detect-behavior-with-sensor-data")
    trained_models_path = project_root / "models" / "trained"
    kaggle_dataset_path = project_root / "models" / "kaggle_dataset"
    
    # 出力ディレクトリを作成
    kaggle_dataset_path.mkdir(exist_ok=True)
    
    # モデルファイルをコピー
    model_files = [
        "baseline_model.pkl",
        "baseline_scaler.pkl", 
        "baseline_features.json"
    ]
    
    for file_name in model_files:
        src = trained_models_path / file_name
        dst = kaggle_dataset_path / file_name
        
        if src.exists():
            shutil.copy2(src, dst)
            print(f"コピー完了: {file_name}")
        else:
            print(f"警告: {file_name} が見つかりません")
    
    # データセットのメタデータを作成
    dataset_metadata = {
        "title": "CMI BFRB Detection Baseline Model",
        "id": "username/cmi-baseline-model",  # 実際のユーザー名に変更してください
        "licenses": [
            {
                "name": "CC0-1.0"
            }
        ]
    }
    
    with open(kaggle_dataset_path / "dataset-metadata.json", "w") as f:
        json.dump(dataset_metadata, f, indent=2)
    
    print(f"\nKaggle用データセットの準備が完了しました: {kaggle_dataset_path}")
    print("\n次のステップ:")
    print("1. dataset-metadata.json の 'id' フィールドをあなたのKaggleユーザー名に変更してください")
    print("2. Kaggle CLI を使用してデータセットをアップロード:")
    print(f"   kaggle datasets create -p {kaggle_dataset_path}")
    print("3. アップロード後、Kaggleノートブックでデータセットを入力として追加してください")

if __name__ == "__main__":
    prepare_model_for_kaggle()
