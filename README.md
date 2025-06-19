# CMI - センサーデータによる行動検出

**コンペティション**: [CMI - Detect Behavior with Sensor Data](https://www.kaggle.com/competitions/cmi-detect-behavior-with-sensor-data)

**締切**: 2025年9月2日 23:59 UTC

## 📋 コンペティション概要

このKaggleコンペティションでは、「Helios」と呼ばれる手首装着デバイスのセンサーデータを用いて、身体焦点反復行動（BFRB）と通常のジェスチャーを区別する機械学習モデルの開発に挑戦します。

### 問題設定
- **目的**: 手首装着デバイスのセンサーデータから身体焦点反復行動（抜毛、皮膚むしり、爪かみなど）を予測
- **デバイス**: Helios - プロトタイプ手首装着ジェスチャー認識デバイス
- **センサー**: IMU（慣性計測ユニット）、近接センサー、温度センサー
- **影響**: BFRB患者（人口の約5%）のモニタリングとリアルタイムフィードバック提供を支援

### 主要技術詳細
- **データ型**: 手首装着デバイスからの時系列センサーデータ
- **使用センサー**: 
  - IMUセンサー（加速度計、ジャイロスコープ、磁力計）
  - 近接センサー
  - 温度センサー（検出精度を大幅に向上）
- **カテゴリ**: ヘルス、時系列解析、カスタムメトリック
- **GPU要件**: 不要（Kaggleの無料リソースで利用可能）

## 🗂️ プロジェクト構成

```
cmi-detect-behavior-with-sensor-data/
├── data/
│   ├── raw/                    # 元の不変データ
│   ├── processed/              # クリーニング・処理済みデータセット
│   ├── external/               # 外部データソース
│   └── interim/                # 中間処理ステップ
├── notebooks/
│   ├── exploratory/            # EDAと初期分析
│   ├── modeling/               # モデル開発ノートブック
│   └── evaluation/             # モデル評価・比較
├── src/
│   ├── data/                   # データ読み込み・前処理
│   ├── features/               # 特徴量エンジニアリング
│   ├── models/                 # モデルアーキテクチャ・学習
│   ├── visualization/          # プロット・可視化ユーティリティ
│   └── utils/                  # 汎用ユーティリティ関数
├── models/
│   ├── trained/                # 保存済み学習モデル
│   ├── checkpoints/            # 学習チェックポイント
│   └── submissions/            # コンペ提出ファイル
├── reports/
│   ├── figures/                # 生成された図表
│   └── final/                  # 最終レポート・ドキュメント
├── experiments/                # 実験追跡・設定
├── config/                     # 設定ファイル
├── docs/                       # ドキュメント
├── tests/                      # ユニットテスト
├── requirements.txt            # Python依存関係
├── environment.yml             # Conda環境ファイル
├── setup.py                    # パッケージセットアップ
├── Makefile                    # 自動化コマンド
└── README.md                   # このファイル
```

## 🚀 クイックスタート

1. **環境セットアップ**
   ```bash
   cd /home/chinchilla/kaggle/pjt/cmi-detect-behavior-with-sensor-data
   
   # uvをインストール（未インストールの場合）
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # 仮想環境作成と依存関係インストール
   uv venv .venv
   uv sync
   
   # 仮想環境有効化
   source .venv/bin/activate
   
   # または、uvコマンド経由で実行
   uv run <command>
   ```

2. **データダウンロード**
   ```bash
   uv run kaggle competitions download -c cmi-detect-behavior-with-sensor-data
   unzip cmi-detect-behavior-with-sensor-data.zip -d data/raw/
   ```

3. **初期EDA**
   ```bash
   uv run jupyter lab
   # または
   make notebook
   ```

## 📊 Data Understanding

### 想定データ構成要素
- **時系列センサーデータ**: Helios手首装着デバイスからのデータ
- **IMUデータ**: 3軸加速度計、ジャイロスコープ、磁力計の測定値
- **近接センサーデータ**: 手の位置追跡
- **温度センサーデータ**: 位置精度向上のための温度測定値
- **ラベル**: 二値分類（BFRB行動 vs 通常ジェスチャー）

### データの課題
- **クラス不均衡**: BFRBは比較的稀な行動
- **時間的依存性**: センサーデータの順次性
- **個人差**: ユーザーごとに異なる行動パターン
- **ノイズ**: センサーデータ固有のノイズ
- **特徴量エンジニアリング**: 生センサー測定値から意味のある特徴量の抽出が必要

## 🎯 モデリング戦略

### アプローチ1: 従来ML + 特徴量エンジニアリング
- 時間窓から統計的特徴量を抽出
- 古典的MLアルゴリズム使用（RF、XGBoost、SVM）
- センサーデータからの工学的特徴量に焦点

### アプローチ2: 深層学習 - 時系列
- 順次モデリングのためのLSTM/GRUネットワーク
- 局所パターン検出のための1D CNN
- 注意機構のためのTransformerアーキテクチャ

### アプローチ3: アンサンブル手法
- 複数のモデルアーキテクチャの組み合わせ
- 異なるアプローチからの予測をスタック
- 堅牢な評価のためのクロスバリデーション

## 📈 評価指標

- コンペティションでは**カスタムメトリック**を使用（詳細はコンペページ参照）
- 二値分類指標の可能性:
  - **適合率/再現率**: BFRB検出のため
  - **AUC-ROC**: ランキング品質のため
  - **F1スコア**: バランス性能のため

## 🔄 ワークフロー

1. **データ探索** (`notebooks/exploratory/`)
   - データ構造と品質の理解
   - センサーパターンの可視化
   - クラス分布の分析

2. **特徴量エンジニアリング** (`src/features/`)
   - 時間領域特徴量（平均、標準偏差、歪度、尖度）
   - 周波数領域特徴量（FFT、スペクトル解析）
   - 時系列固有特徴量（自己相関、トレンド）

3. **モデル開発** (`src/models/`)
   - ベースラインモデル
   - 高度なアーキテクチャ
   - ハイパーパラメータチューニング

4. **評価** (`notebooks/evaluation/`)
   - クロスバリデーション戦略
   - モデル比較
   - エラー分析

5. **提出** (`models/submissions/`)
   - 最終モデル選択
   - 予測生成
   - 提出フォーマット

## 🛠️ ツール・ライブラリ

### コアMLスタック
- **pandas**: データ操作
- **numpy**: 数値計算
- **scikit-learn**: 従来MLアルゴリズム
- **xgboost/lightgbm**: 勾配ブースティング
- **pytorch/tensorflow**: 深層学習

### 時系列専用
- **tsfresh**: 自動特徴量抽出
- **tslearn**: 時系列MLアルゴリズム
- **scipy**: 信号処理

### 可視化・EDA
- **matplotlib/seaborn**: 静的プロット
- **plotly**: インタラクティブ可視化
- **pandas-profiling**: 自動EDAレポート

## 📝 実験追跡

`experiments/`ディレクトリで以下を追跡：
- モデル設定
- 訓練ログ
- 性能指標
- ハイパーパラメータ探索
- クロスバリデーション結果

## 🎯 成功指標

- **主要**: コンペティションリーダーボード順位
- **副次**: モデル解釈性と洞察
- **学習**: BFRB検出パターンの理解

## 📚 リソース・参考文献

- [コンペティションページ](https://www.kaggle.com/competitions/cmi-detect-behavior-with-sensor-data)
- [Heliosデバイス研究](https://matter.childmind.org/gesture-recognition-device.html)
- [BFRB情報](https://www.bfrb.org/)
- 時系列分類文献
- ウェアラブルセンサーデータ解析論文

## 🤝 貢献

1. 新実験用の機能ブランチを作成
2. 全てのモデリング決定を文書化
3. ノートブックを整理しコメントを充実
4. 新しい洞察でREADMEを更新

---

**最終更新**: 2025年6月19日
**コンペティション状況**: アクティブ（締切: 2025年9月2日）