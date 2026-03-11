# History Cleanup Plan

## 目的
- Git 履歴から秘密情報とローカル業務ファイルを完全に除去する
- リポジトリを公開可能な状態へ近づける

## 除去対象
- `src/.env`
- `src/input/`
- `src/output/`
- `src/__pycache__/`

## 理由
- `src/.env` に Gemini API キーが含まれていた可能性がある
- `src/input/` に業務インプットが含まれていた
- `src/output/` に業務アウトプットが含まれていた
- `src/__pycache__/` は公開不要な生成物

## 手順
1. 現在の `main` をバックアップブランチへ退避する
2. Git 履歴から除去対象パスを削除する
3. ローカルで履歴確認を行う
4. `origin/main` へ force push する
5. ユーザー側で Gemini API キーを失効・再発行する

## 注意
- 履歴書き換えにより commit hash は変わる
- 既存 clone は通常 pull で追従できなくなる
- GitHub 上の古い commit 参照は無効になる

## 実施結果
- `main` の履歴から `src/.env` は除去済み
- `main` の履歴から `src/input/` は除去済み
- `main` の履歴から `src/output/` は除去済み
- `main` の履歴から `src/__pycache__/` は除去済み
- `origin/main` へ force push 実施済み
- ローカルの `refs/original` と reflog も掃除済み
