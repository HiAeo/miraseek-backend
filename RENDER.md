# MiraSeek Backend

## 环境变量

在 Render 中设置以下环境变量：

```
SUPABASE_URL=https://lzlqbgcebaneaoidmjrg.supabase.co
SUPABASE_KEY=sb_publishable_E6V1zaK8NRvcywJ4qdW_cg_vDORXnxo
SECRET_KEY=miraseek-production-secret-key-2024
```

## 构建命令

```bash
pip install -r requirements.txt
```

## 启动命令

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

## 本地开发

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```
