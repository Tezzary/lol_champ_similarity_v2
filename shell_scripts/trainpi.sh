#used to offload the program to my rasberry pi, as population of the database takes a long time but is not computationally intensive
git add .
git commit -m "to pi"
git push
scp .env raspberrypi:~/lol_champ_similarity_v2/
ssh raspberrypi "
    cd lol_champ_similarity_v2
    git pull
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    nohup python3 embedding.py > embedding_output.log 2>&1 & disown
    echo 'Running on Raspberry Pi...'
    tail -f embedding_output.log
"