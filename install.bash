#!/usr/bin/bash
#
#
SHARE_DIR=/usr/share/pomochrono

mkdir -p $SHARE_DIR
cp *.py $SHARE_DIR
chmod 0755 $SHARE_DIR/pomochrono.py
#cp *.pyc $SHARE_DIR
cp *.oga $SHARE_DIR
cp *.png $SHARE_DIR
ln -sf $SHARE_DIR/pomochrono.py /usr/bin/pomochrono
