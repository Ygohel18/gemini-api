## Gemini Output as OpenAI

Change api key in .env file

```
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
pip install uvicorn

# Change folder path in user.service
sudo cp ./user.service /lib/systemd/system/ygohel18.gemini.api.service

sudo systemctl daemon-reload
sudo systemctl start ygohel18.gemini.api
sudo systemctl enable ygohel18.gemini.api

# Change site url in nginx.conf
sudo cp ./nginx.conf /etc/nginx/sites-available/yoursite

sudo ln -s /etc/nginx/sites-available/yoursite /etc/nginx/sites-enabled/

sudo nginx -t
sudo systemctl restart nginx
```