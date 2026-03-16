# pipecmd
Pipe-friendly data transformation: upper/lower/sort/grep/replace/join/hash/freq and more.
```bash
cat file.txt | python pipecmd.py upper
cat file.txt | python pipecmd.py grep "error" | python pipecmd.py freq
ls | python pipecmd.py sort | python pipecmd.py number
cat words.txt | python pipecmd.py dedup | python pipecmd.py count
```
## Zero dependencies. Python 3.6+.
