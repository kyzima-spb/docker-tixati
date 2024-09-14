#!/usr/bin/env bash

version="$1"
dest="${2:-.}"
i=0
files=(
  amd64.deb
  x86_64.rpm
  x86_64.manualinstall.tar.gz
  i686.deb
  i686.rpm
  i686.manualinstall.tar.gz
  win64-install.exe
  win32-install.exe
)

for name in "${files[@]}"; do
  i=$((i % 3 + 1))
  
  filename="$([[ $name =~ \.deb$ ]] && echo "_${version}-1_${name}" || echo "-${version}-1.${name}")"

  wget -P "$dest" "https://download${i}.tixati.com/download/tixati${filename}"
done
