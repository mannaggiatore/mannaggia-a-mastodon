FROM alpine

RUN \
	apk add --no-cache python3 py3-cffi py3-six py3-requests py3-cryptography && \
	pip3 install Mastodon.py
COPY mannaggia.py mastodon-mannaggia.py santi_e_beati.txt /
RUN chmod +x /mannaggia.py /mastodon-mannaggia.py

WORKDIR /

ENTRYPOINT ["python3", "/mastodon-mannaggia.py"]


