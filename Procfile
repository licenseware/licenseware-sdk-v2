web: uwsgi --http 0.0.0.0:5000 -w main:app --processes 4
worker: dramatiq workers.controller:broker -p4 --use-spawn