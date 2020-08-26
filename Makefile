filebeat_run:
	filebeat -e -c $(CURDIR)/xfilebeat.yml -d "publish"
logstash_run:
	logstash -f $(CURDIR)/apachelog-pipeline.conf --config.reload.automatic
build_py:
	pip3 install --upgrade pip && \
	pip3 install --no-cache-dir -r requirements.txt
