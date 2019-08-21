FROM python:slim

COPY . zna/

RUN set -ex; \
	cd zna && pip install -r requirements.txt; \
	python zju_news_alerts warmup;

WORKDIR /zna

CMD ["python", "-u", "zju_news_alerts", "serve"]

