# Intro
Here are 2 options for solving the problem.

**Please look to my developer notes for implementation details**
(https://github.com/ArezKhalimi/eyeo_log_handler/blob/master/exp.pdf)

1) Solution in logstash + filebeat + (MongoDB or Elashsearch) **Recommended for a real project**
2) Implementation using python (demo of writing code)

# MVP ELK build
* [install logstash](https://www.elastic.co/guide/en/logstash/current/installing-logstash.html)
* [install filebeat](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-installation-configuration.html#:~:text=Step%201%3A%20Install%20Filebeatedit&text=To%20install%20the%20OSS%20distribution,%2Ftap%2Ffilebeat%2Doss%20.&text=Download%20the%20Filebeat%20Windows%20zip,%3E%2Dwindows%20directory%20to%20Filebeat%20.)
* run filebeat
> make filebeat_run
* run logstash
> logstash_run

**!!! this version presents the output to the console !!!** 

# Python
* [install mongoDB](https://docs.mongodb.com/manual/installation/)
* create database and set into **MONGO_URI** variable insite `log_handler.py`
* install required libs into python enviroment
> make build_py
* run any file
> python log_handler.py -f <file_path>
