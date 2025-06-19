# CMI BFRB Detection - 提出ガイド

## 概要

このディレクトリには、CMI BFRB Detectionコンペティション用のベースライン提出ノートブックと関連ファイルが含まれています。

## ファイル構成

### 提出用ノートブック
- `baseline_submission.ipynb`: Kaggleに提出するメインのノートブック

### モデルファイル (kaggle_dataset ディレクトリ)
- `baseline_model.pkl`: 学習済みのRandomForestモデル
- `baseline_scaler.pkl`: 特徴量正規化用のStandardScaler
- `baseline_features.json`: 特徴量名のリスト
- `dataset-metadata.json`: Kaggleデータセット用のメタデータ

## 提出手順

### 1. モデルをKaggleデータセットとしてアップロード

```bash
# dataset-metadata.json の 'id' フィールドを自分のKaggleユーザー名に変更
# 例: "username/cmi-baseline-model" → "yourusername/cmi-baseline-model"

# Kaggle CLIでデータセットをアップロード
kaggle datasets create -p models/kaggle_dataset/
```

### 2. Kaggleノートブックでの提出

1. 新しいKaggleノートブックを作成
2. インターネット接続を有効にする
3. 以下のデータセットを入力として追加:
   - `cmi-detect-behavior-with-sensor-data` (公式データセット)
   - `yourusername/cmi-baseline-model` (アップロードしたモデル)
4. `baseline_submission.ipynb` の内容をコピー&ペースト
5. Submit to Competition

## モデルの詳細

### 特徴量
- 各センサー（加速度、ジャイロ、磁力計など）の統計的特徴量
- 時系列特徴量（長さ、サンプリングレート）
- 複合特徴量（加速度・ジャイロの合成ベクトル）

### アルゴリズム
- RandomForestClassifier
- 特徴量の標準化
- セッション単位での予測

### 予測出力
- `'BFRB detected'`: BFRBが検出された場合
- `'Text on phone'`: BFRBが検出されなかった場合

## トラブルシューティング

### よくある問題

1. **モデルファイルが見つからない**
   - dataset-metadata.jsonのidが正しく設定されているか確認
   - Kaggleデータセットが正常にアップロードされているか確認

2. **予測エラー**
   - 特徴量の次元が一致しているか確認
   - NaN値の処理が適切に行われているか確認

3. **タイムアウトエラー**
   - 推論時間を短縮するため、特徴量数を削減することを検討

## 改善のヒント

### 短期的改善
1. 特徴量エンジニアリングの改善
2. ハイパーパラメータのチューニング
3. モデルアンサンブル

### 長期的改善
1. 深層学習モデルの導入
2. 時系列モデル（LSTM、Transformer）
3. データ拡張手法

## 参考

- [Kaggle API documentation](https://github.com/Kaggle/kaggle-api)
- [CMI Inference Server documentation](https://www.kaggle.com/code/inversion/cmi-inference-server-demo)
