# Zalando
Zalando is crawlar dealing the crawling of https://www.zalando.com/. Use by anyone within the organization

## Installation
```bash
pip install beautifulsoup4

pip install selenium

pip install PyVirtualDisplay

sudo apt-get update

sudo apt-get install google-chrome-stable

wget https://chromedriver.storage.googleapis.com/79.0.3945.36/chromedriver_linux64.zip

//if you are not using aanaconda run these command
    unzip chromedriver_linux64.zip
    sudo mv chromedriver /usr/bin/chromedriver
    sudo chown root:root /usr/bin/chromedriver
    sudo chmod +x /usr/bin/chromedriver
    chromedriver --version
//if you are using aanaconda run these command
    unzip chromedriver_linux64.zip
    sudo mv chromedriver /usr/local/bin/chromedriver
    sudo chown root:root /usr/local/bin/chromedriver
    sudo chmod +x  /usr/local/bin/chromedriver
    chromedriver --version

```
## Docker Installation
```bash
docker build -t yourname/zalando:v1 .
docker run -it -v /home/Your_path/zalando:/zalando -t yourname/zalando:v1
```
## How to use
```bash
python get_pro_links.py
python get_pro_desc.py
```
