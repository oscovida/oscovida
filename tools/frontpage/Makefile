# general strategy:
#
# markdown files index.md and about.md are the source files
#
# create html from these files.



all: index.html about.html rsync

index.html: index.md
		pandoc -t html -o index.html index.md


about.html: about.md
		pandoc -t html -o about.html about.md


rsync:
	  mkdir -p ../wwwroot/figures
	  rsync -auv index.html about.html ../wwwroot
	  rsync -auv figures/* ../wwwroot/figures
	  @echo" Copied files into ../wwwroot"

clean:
	  # delete derived files
	  rm -rf about.html index.html

