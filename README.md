# Dockerを用いたフルスタック開発の練習

## コンテナの立ち上げ
起動  
docker-compose up  
修正を強制反映してビルドしなおすとき  
docker-compose up --build
終了  
docker-compose down  
## 工夫した点
ファイル保存用のフォルダをアプリ起動時に作成、さらにアプリ起動中に何らかのエラーでフォルダが消えても保存できるように、エンドポイントにも作成するようにした  
ファイルを保存するときに非同期でチャンクごとに分けて保存するようにしてスレッド、メモリを占有しない設計にした  
ファイルサイズチェックを二重(content_length, seek(0,2))にすることでより早く不正なファイルをはじくことができるようにして、堅牢なファイルサイズのバリデーションを行えるようにした

## 学んだこと　　
backend/uploads/ フォルダの中身は無視する  
backend/uploads/*   
ただし、.gitkeep ファイルだけは無視しないようにする  
!backend/uploads/.gitkeep  
Headerからファイルのサイズを取得できる,fastAPIが自動でヘッダーのContent-Lengthから読み取ってくれる　　

## docker-compose.yml作成前の動作確認
docker build -t my-backend .  
-t my-backend (my-backend)という名前のタグをつける,後で呼び出すときにタグがないとランダムなIDになって不便  

docker run -p 8000:8000 my-backend  
-p 8000:8000 自分のPC(ホスト)とdockerコンテナの8000番をつなぐ  
my-backend どのイメージを起動するか指定   

http://localhost:8000/docs　このURLでswaggerが開ける
