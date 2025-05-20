git add .
git commit -m "to pi"
git push
ssh raspberrypi "
    cd lol_champ_similarity_v2
    git pull
    python3 request.py
"
scp raspberrypi/lolchamp_similarity_v2/database.db database.db