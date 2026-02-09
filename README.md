# Dockerを用いたフルスタック開発の練習


## docker-compose.yml作成前の動作確認
docker build -t my-backend .  
-t my-backend (my-backend)という名前のタグをつける,後で呼び出すときにタグがないとランダムなIDになって不便  

docker run -p 8000:8000 my-backend  
-p 8000:8000 自分のPC(ホスト)とdockerコンテナの8000番をつなぐ  
my-backend どのイメージを起動するか指定   

http://localhost:8000/docs　このURLでswaggerが開ける

## docker-compose.yml作成後の実行
起動  
docker-compose up  
修正を強制反映してビルドしなおすとき  
docker-compose up --build
終了  
docker-compose down  