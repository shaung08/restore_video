nohup python3 /home/restore_video/backend/backend.py > /home/restore_video/log 2>&1 &
cd /home/restore_video/frontend 
nohup npm start > /home/restore_video/log 2>&1 &