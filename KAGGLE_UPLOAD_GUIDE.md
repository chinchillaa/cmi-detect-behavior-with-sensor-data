# Kaggle提出手順書

## ノートブックのKaggleアップロード方法

### 方法1: Kaggle Web UIを使用（推奨）

1. **Kaggleにログイン**
   - https://www.kaggle.com にアクセス
   - アカウントでログイン

2. **新しいノートブック作成**
   - "Code" → "New Notebook" をクリック
   - または直接 https://www.kaggle.com/code にアクセス

3. **ノートブックの設定**
   - タイトル: "CMI BFRB Detection Baseline Submission"
   - 言語: Python
   - インターネット接続: 有効にする

4. **データセットの追加**
   - 右側パネルの "Input" セクション
   - "Add data" をクリック
   - 以下を検索して追加:
     - `cmi-detect-behavior-with-sensor-data` (公式データセット)
     - あなたがアップロードした `cmi-baseline-model` データセット

5. **ノートブック内容の貼り付け**
   - ローカルファイル `/home/chinchilla/kaggle/pjt/cmi-detect-behavior-with-sensor-data/notebooks/evaluation/baseline_submission.ipynb` の内容をコピー
   - Kaggleノートブックの各セルに貼り付け

6. **保存と実行**
   - "Save Version" をクリック
   - "Run All" で全セルを実行
   - エラーがないことを確認

7. **提出**
   - "Submit to Competition" ボタンをクリック

### 方法2: Kaggle CLI（要認証設定）

Kaggle CLIを使用する場合は、事前に以下の設定が必要です：

```bash
# 1. Kaggle API Keyの設定
# https://www.kaggle.com/settings/account からAPI Keyをダウンロード
# ~/.kaggle/kaggle.json に配置

# 2. アクセス権限の設定
chmod 600 ~/.kaggle/kaggle.json

# 3. Kaggle CLIのインストール
pip install kaggle

# 4. ノートブックのプッシュ
# kaggle kernels push -p /path/to/notebook/folder
```

### ファイル位置

- **ローカルノートブック**: `/home/chinchilla/kaggle/pjt/cmi-detect-behavior-with-sensor-data/notebooks/evaluation/baseline_submission.ipynb`
- **モデルファイル**: `/home/chinchilla/kaggle/pjt/cmi-detect-behavior-with-sensor-data/models/kaggle_dataset/`

### 重要な注意点

1. **モデルデータセットのアップロード**
   - まず `models/kaggle_dataset/` の内容をKaggleデータセットとしてアップロード
   - `dataset-metadata.json` の `id` フィールドを自分のユーザー名に変更してからアップロード

2. **ノートブック内のパス**
   - モデル読み込みパス: `/kaggle/input/cmi-baseline-model/`
   - データセット名が自分のユーザー名と一致していることを確認

3. **実行環境**
   - インターネット接続を有効にしてください
   - 必要なライブラリがすべてインストールされていることを確認

現在の状況では、Kaggle Web UIを使用した手動アップロードが最も確実な方法です。
