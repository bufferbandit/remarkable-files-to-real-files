# Git pull doesn't work that well on the remarkable (ssl error or something). So download a zip and unzip it
rm -rf r2f && wget -qO- https://github.com/bufferbandit/remarkable-files-to-real-files/archive/refs/heads/master.zip | busybox unzip - && mv remarkable-files-to-real-files-master r2f
