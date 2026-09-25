awk '{print $3}' data/app.log \
    | sort \
    | uniq -c \
    | sort -nr \
    | head -10