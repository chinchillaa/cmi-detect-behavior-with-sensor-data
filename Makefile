# CMI - センサーデータによる行動検出 - Makefile

.PHONY: help install setup-env download-data clean lint test notebook train evaluate submit

# デフォルトターゲット
help:
	@echo "利用可能なコマンド:"
	@echo "  install      - Python依存関係をインストール (uv sync)"
	@echo "  install-dev  - 開発用依存関係も含めてインストール"
	@echo "  install-deep - 深層学習依存関係も含めてインストール"
	@echo "  setup-env    - uv仮想環境を作成"
	@echo "  download-data - Kaggleからコンペデータをダウンロード"
	@echo "  clean        - 生成ファイルとキャッシュをクリーンアップ"
	@echo "  lint         - コードリンティングを実行"
	@echo "  test         - ユニットテストを実行"
	@echo "  notebook     - Jupyterノートブックサーバーを起動"
	@echo "  train        - モデル学習パイプラインを実行"
	@echo "  evaluate     - モデルを評価"
	@echo "  submit       - 提出ファイルを生成"
	@echo "  eda          - 初期探索的データ分析を実行"

# 環境セットアップ
install:
	uv sync

install-dev:
	uv sync --extra dev

install-deep:
	uv sync --extra deep_learning

setup-env:
	uv venv .venv
	@echo "環境の有効化: source .venv/bin/activate"
	@echo "または: uv run <command> で仮想環境内でコマンド実行"

# データ管理
download-data:
	@echo "コンペデータをダウンロード中..."
	kaggle competitions download -c cmi-detect-behavior-with-sensor-data
	unzip -o cmi-detect-behavior-with-sensor-data.zip -d data/raw/
	rm cmi-detect-behavior-with-sensor-data.zip
	@echo "データをdata/raw/にダウンロードしました"

# データ処理
process-data:
	uv run python src/data/make_dataset.py

# モデル学習
train:
	uv run python src/models/train_model.py

# 評価
evaluate:
	uv run python src/models/evaluate_model.py

# 予測生成
predict:
	uv run python src/models/predict_model.py

# 提出ファイル作成
submit: predict
	uv run python src/models/create_submission.py
	@echo "提出ファイルをmodels/submissions/に作成しました"

# 開発
notebook:
	uv run jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root

eda:
	uv run jupyter nbconvert --to notebook --execute notebooks/exploratory/01_initial_eda.ipynb --output-dir=reports/

# コード品質
lint:
	uv run black src/ tests/
	uv run isort src/ tests/
	uv run flake8 src/ tests/

test:
	uv run pytest tests/ -v

# クリーンアップ
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf dist/
	rm -rf build/

clean-data:
	rm -rf data/interim/*
	rm -rf data/processed/*
	@echo "中間データと処理済みデータをクリーンアップしました"

clean-models:
	rm -rf models/trained/*
	rm -rf models/checkpoints/*
	@echo "保存モデルとチェックポイントをクリーンアップしました"

clean-all: clean clean-data clean-models
	rm -rf reports/figures/*
	@echo "全ての生成ファイルをクリーンアップしました"

# Docker（必要に応じて）
docker-build:
	docker build -t cmi-bfrb-detection .

docker-run:
	docker run -it --rm -v $(PWD):/workspace cmi-bfrb-detection

# Gitフック
setup-git-hooks:
	pre-commit install
	@echo "Gitフックをインストールしました"

# 完全パイプライン
pipeline: process-data train evaluate submit
	@echo "完全パイプラインが完了しました"

# 新規ユーザー向けクイックスタート
quickstart: setup-env download-data eda
	@echo "クイックスタートが完了しました。'make notebook'を実行して探索を開始してください！"