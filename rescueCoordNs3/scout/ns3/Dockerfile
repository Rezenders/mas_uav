FROM ubuntu:bionic

RUN apt-get update && apt-get install -y \
    git vim python python-dev python-pip bzr qt5-default mercurial gcc g++ gir1.2-goocanvas-2.0 \
	python-gi python-gi-cairo python-pygraphviz python3-gi python3-gi-cairo \
	python3-pygraphviz gir1.2-gtk-3.0 ipython ipython3  gsl-bin libgsl-dev \
	libgsl23 libgslcblas0 libgtk2.0-0 libgtk2.0-dev \
    && rm -rf /var/lib/apt/lists/

RUN pip install PyBindGen
RUN mkdir /repos && cd repos && hg clone http://code.nsnam.org/ns-3-allinone
WORKDIR /repos/ns-3-allinone
RUN ./download.py -n ns-3-dev && ./build.py
WORKDIR /repos/ns-3-allinone/ns-3-dev
RUN ./waf configure --enable-examples && ./waf
