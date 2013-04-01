#!/bin/bash
#
# This is a script to remove unwanted elements from a gst-plugins-bad tarball.
# To keep one element not removed, just append its name to ALLOWED.
# Please note that when you append new element name to ALLOWED, you might
# need to add dependency package name to the .spec file.
#

SOURCE="gst-plugins-bad-0.10.23.tar.bz2"
NEW_SOURCE=`echo $SOURCE | sed 's/bad-/bad-free-/'`
DIRECTORY=`echo $SOURCE | sed 's/\.tar\.bz2//'`
NEW_DIRECTORY=`echo $DIRECTORY | sed 's/bad-/bad-free-/'`

ALL=

ALLOWED="
valve
liveadder
rtpmux
dtmf
sdp
autoconvert
camerabin
camerabin2
debugutils
h264parse
jpegformat
rawparse
selector
qtmux
metadata
timidity
audioparsers
shm
videomaxrate
real
vp8
"

error()
{
	MESSAGE=$1
	echo $MESSAGE
	exit 1
}

is_allowed()
{
	ELEMENT=$1
	for i in $ALLOWED ; do
		if test x$ELEMENT = x$i ; then
			return 0;
		fi
	done
	return 1;
}

rm -rf $DIRECTORY
tar xjf $SOURCE || error "Cannot unpack $SOURCE"
pushd $DIRECTORY > /dev/null || error "Cannot open directory \"$DIRECTORY\""
echo
cd gst
ALL=`ls | grep -v Makefile`
cd ../ext
ALL="$ALL `ls | grep -v Makefile`"
cd ../sys
ALL="$ALL `ls | grep -v Makefile`"
cd ../
echo All elements: $ALL
echo
echo ALLOWED elements: $ALLOWED
echo
for subdir in gst ext sys; do
	for dir in $subdir/* ; do
		if ! [ -d $dir ] ; then
			continue;
		fi
		ELEMENT=`basename $dir`
		if ( is_allowed $ELEMENT ) ; then
			continue;
		fi

		echo "Process element $ELEMENT:"

		echo "     Removing directory $dir"
		rm -r $dir || error "Cannot remove $dir"
		if grep -q "AG_GST_CHECK_PLUGIN($ELEMENT)" configure.ac ; then
			echo "     Removing check for $ELEMENT in configure.ac"
			grep -v "AG_GST_CHECK_PLUGIN($ELEMENT)" configure.ac > configure.ac.new && mv configure.ac.new configure.ac
		fi

		echo "     Removing Makefile generation for $ELEMENT in configure.ac"
		grep -v "$dir/Makefile" configure.ac > configure.ac.new && mv configure.ac.new configure.ac

		echo "     Removing $ELEMENT in $subdir/Makefile.am"
		grep -v "$ELEMENT" $subdir/Makefile.am > $subdir/Makefile.am.new && mv $subdir/Makefile.am.new $subdir/Makefile.am

		# Work around special element: mpegtsmux and real, vdpau and gsettings
		if test $ELEMENT = mpegtsmux ; then
			grep -v "gst/mpegtsmux/tsmux/Makefile" configure.ac > configure.ac.new && mv configure.ac.new configure.ac
		fi
		if test $ELEMENT = vdpau ; then
			grep -v "sys/vdpau/gstvdp/Makefile" configure.ac > configure.ac.new && mv configure.ac.new configure.ac
			grep -v "sys/vdpau/basevideodecoder/Makefile" configure.ac > configure.ac.new && mv configure.ac.new configure.ac
		fi
		if test $ELEMENT = gsettings ; then
			grep -v "ext/gsettings/org.freedesktop.gstreamer.default-elements.gschema.xml" configure.ac > configure.ac.new && mv configure.ac.new configure.ac
		fi
		if test $ELEMENT = real ; then
			grep -v "AG_GST_DISABLE_PLUGIN(real)" configure.ac > configure.ac.new && mv configure.ac.new configure.ac
		fi

		echo "     Removing documentation for $ELEMENT in docs/plugins/Makefile.am"
		if grep -q "$ELEMENT" docs/plugins/Makefile.am ; then
			grep -v $dir docs/plugins/Makefile.am > docs/plugins/Makefile.am.new && mv docs/plugins/Makefile.am.new docs/plugins/Makefile.am
		fi
		echo
	done

	echo Remove blank line following trailing backslah from $subdir/Makefile.am

	vim -c ":%s/\\\\\n\\n/\\r\\r/g" -c "x" $subdir/Makefile.am
	vim -c ":$,$ s/\\\\\n/\\r/" -c "x" $subdir/Makefile.am
done

# Avoid blank line following trailing backslash
file=docs/plugins/Makefile.am
vim -c ":%s/\\\\\n\\n/\\r\\r/" -c "x" $file
vim -c ":$,$ s/\\\\\n/\\r/" -c "x" $file

# Workaround for DCCP disable issue
sed 's/AC_SUBST(DCCP_LIBS)/echo/g' configure.ac > configure.ac.new && mv configure.ac.new configure.ac

sed 's/AG_GST_DISABLE_PLUGIN(dccp)/echo/g' configure.ac > configure.ac.new && mv configure.ac.new configure.ac

# Re-config
autoreconf

popd > /dev/null

rm -fr $NEW_DIRECTORY
mv $DIRECTORY $NEW_DIRECTORY

tar cjf $NEW_SOURCE $NEW_DIRECTORY
#rm -fr $NEW_DIRECTORY
echo "$NEW_SOURCE is created successfully."

