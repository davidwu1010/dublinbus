if [ $# != 1 ]; then
    echo "USAGE: sh start.sh env"
    echo "e.g.: sh start.sh production"
    exit 1
fi

if ! ps -ef | grep "weather_spider.py" | grep -v "grep"  >/dev/null;then
    echo "start weather_spider.py"
    python weather_spider.py $1 
    exit 1
else
    echo "weather_spider.py already start"
fi