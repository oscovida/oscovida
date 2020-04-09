all: index.html about.html rsync

index.html: index.md
		pandoc -t html -o index.html index.md


about.html: about.md
		pandoc -t html -o about.html about.md


rsync:
	  rsync -auv index.html about.html ../wwwroot
	  mkdir -p ../wwwroot/figures
	  rsync -auv figures/* ../wwwroot/figures
