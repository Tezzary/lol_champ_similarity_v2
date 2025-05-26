#used to offload the program to my rasberry pi, as population of the database takes a long time but is not computationally intensive
git add .
git commit -m "to pi"
git push
scp .env raspberrypi:~/lol_champ_similarity_v2/
ssh raspberrypi "
    cd lol_champ_similarity_v2
    git pull
    killall python3
    nohup python3 -u populatedb.py > output.log 2>&1 & disown
    echo 'Running on Raspberry Pi...'
    tail -f output.log

"