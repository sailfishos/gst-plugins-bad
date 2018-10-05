%define majorminor   1.0
%define gstreamer    gstreamer

Summary:     GStreamer streaming media framework "bad" plug-ins
Name:        %{gstreamer}%{majorminor}-plugins-bad
Version:     1.14.1
Release:     1
License:     LGPLv2+
Group:       Applications/Multimedia
URL:         http://gstreamer.freedesktop.org/
Source:      http://gstreamer.freedesktop.org/src/gst-plugins-bad/gstreamer1.0-plugins-bad-%{version}.tar.xz
Patch1:      0001-Set-video-branch-to-NULL-after-finishing-video-recor.patch
Patch2:      0002-Keep-video-branch-in-NULL-state.patch
Patch3:      0003-photography-add-missing-vmethods.patch
Patch4:      0004-camerabin-install-GST_PHOTOGRAPHY_PROP_EXPOSURE_MODE.patch
Patch5:      0005-Downgrade-mpeg4videoparse-to-prevent-it-from-being-p.patch

%define sonamever %(echo %{version} | cut -d '+' -f 1)

Requires:      orc >= 0.4.18
BuildRequires: pkgconfig(gstreamer-plugins-base-1.0) >= %{sonamever}
BuildRequires: check
BuildRequires: pkgconfig(nice) >= 0.1.14
BuildRequires: pkgconfig(libexif)
BuildRequires: pkgconfig(orc-0.4) >= 0.4.18
BuildRequires: pkgconfig(libgcrypt)
BuildRequires: pkgconfig(wayland-egl)
BuildRequires: pkgconfig(glesv2)
BuildRequires: pkgconfig(egl)
BuildRequires: pkgconfig(opus)
BuildRequires: pkgconfig(libwebp)
BuildRequires: pkgconfig(libxml-2.0)
BuildRequires: pkgconfig(libssl)
BuildRequires: pkgconfig(libcrypto)
BuildRequires: pkgconfig(libsrtp2)
BuildRequires: python
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
BuildRequires: gettext-devel

%description
GStreamer is a streaming media framework, based on graphs of elements which
operate on media data.

%package devel
Summary: Development files for the GStreamer media framework "bad" plug-ins
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: gstreamer1.0-plugins-base-devel

%description devel
GStreamer is a streaming media framework, based on graphs of elements which
operate on media data.

This package contains the development files for the plug-ins that
are not tested well enough, or the code is not of good enough quality.

%prep
%setup -q -n gstreamer1.0-plugins-bad-%{version}/gst-plugins-bad
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
NOCONFIGURE=1 ./autogen.sh
%configure \
  --with-package-name='SailfishOS GStreamer Bad Plug-ins' \
  --with-package-origin='http://jolla.com' \
  --enable-debug \
  --disable-static \
  --enable-shared \
  --disable-introspection \
  --disable-gtk-doc \
  --disable-examples \
  --enable-gtk-doc-html=no \
  --enable-gtk-doc-pdf=no \
  --disable-nls \
  --enable-orc \
  --enable-gles2 \
  --enable-x11=no \
  --disable-adpcmdec --disable-adpcmenc --disable-asfmux \
  --disable-audiovisualizers --disable-bayer \
  --disable-cdxaparse --disable-coloreffects --disable-dataurisrc \
  --disable-dccp --disable-debugutils --disable-dvbsuboverlay \
  --disable-dvdspu --disable-faceoverlay --disable-festival --disable-fieldanalysis \
  --disable-freeverb --disable-frei0r --disable-gaudieffects \
  --disable-geometrictransform --disable-hdvparse --disable-inter --disable-interlace \
  --disable-ivfparse --disable-jp2kdecimator --disable-librfb \
  --disable-liveadder --disable-mpegdemux --disable-mpegtsmux \
  --disable-mpegpsmux --disable-mve --disable-mxf \
  --disable-nuvdemux --disable-patchdetect --disable-pcapparse \
  --disable-pnm --disable-real --disable-removesilence --disable-sdi \
  --disable-sdp --disable-segmentclip --disable-siren --disable-smooth \
  --disable-speed --disable-subenc --disable-stereo --disable-tta \
  --disable-videofilters --disable-videomeasure --disable-videosignal \
  --disable-vmnc --disable-y4m --disable-fbdev --disable-vcd \
  --disable-id3tag --disable-linsys --disable-gsettings --disable-dvb \
  --disable-decklink --disable-accurip --disable-audiofxbad --disable-ivtc \
  --disable-midi --disable-yadif --disable-mpegtsmux \
  --disable-accurip --disable-autoconvert --disable-gdp \
  --disable-qt --disable-curl --disable-bz2 --disable-dash --disable-smoothstreaming 

make %{?jobs:-j%jobs}

%install
%make_install

# Clean out files that should not be part of the rpm.
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
rm -fr $RPM_BUILD_ROOT%{_datadir}/gtk-doc

# remove waylandsink. It does not run because we do not support all the interfaces it needs.
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstwaylandsink.so
rm -f $RPM_BUILD_ROOT%{_libdir}/libgstwayland-%{majorminor}.so*

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post devel -p /sbin/ldconfig
%postun devel -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/gstreamer-%{majorminor}/libgstjpegformat.so
%{_libdir}/gstreamer-%{majorminor}/libgstshm.so
%{_libdir}/gstreamer-%{majorminor}/libgstvideoparsersbad.so
%{_libdir}/gstreamer-%{majorminor}/libgstcompositor.so
%{_libdir}/gstreamer-%{majorminor}/libgsthls.so
%{_libdir}/gstreamer-%{majorminor}/libgstmpegtsdemux.so
%{_libdir}/gstreamer-%{majorminor}/libgstopusparse.so
%{_libdir}/gstreamer-%{majorminor}/libgstaiff.so
%{_libdir}/gstreamer-%{majorminor}/libgstnetsim.so
%{_libdir}/gstreamer-%{majorminor}/libgstrtponvif.so
%{_libdir}/gstreamer-%{majorminor}/libgstvideoframe_audiolevel.so
%{_libdir}/gstreamer-%{majorminor}/libgstdtls.so
#%{_libdir}/gstreamer-%{majorminor}/libgstdashdemux.so
#%{_libdir}/gstreamer-%{majorminor}/libgstsmoothstreaming.so
%{_libdir}/gstreamer-%{majorminor}/libgsttimecode.so
%{_libdir}/gstreamer-%{majorminor}/libgstwebp.so
%{_libdir}/gstreamer-%{majorminor}/libgstaudiobuffersplit.so
%{_libdir}/gstreamer-%{majorminor}/libgstaudiolatency.so
%{_libdir}/gstreamer-%{majorminor}/libgstaudiomixmatrix.so
%{_libdir}/gstreamer-%{majorminor}/libgstcamerabin.so
%{_libdir}/gstreamer-%{majorminor}/libgstipcpipeline.so
%{_libdir}/gstreamer-%{majorminor}/libgstlegacyrawparse.so
%{_libdir}/gstreamer-%{majorminor}/libgstopenglmixers.so
%{_libdir}/gstreamer-%{majorminor}/libgstproxy.so
%{_libdir}/gstreamer-%{majorminor}/libgstsrtp.so
%{_libdir}/gstreamer-%{majorminor}/libgstwebrtc.so
%{_libdir}/libgstphotography-%{majorminor}.so.*
%{_libdir}/libgstcodecparsers-%{majorminor}.so.*
%{_libdir}/libgstinsertbin-%{majorminor}.so.*
%{_libdir}/libgsturidownloader-%{majorminor}.so.*
%{_libdir}/libgstbasecamerabinsrc-%{majorminor}.so.*
%{_libdir}/libgstmpegts-%{majorminor}.so.*
%{_libdir}/libgstbadvideo-%{majorminor}.so.*
%{_libdir}/libgstadaptivedemux-%{majorminor}.so.*
%{_libdir}/libgstbadaudio-%{majorminor}.so.*
%{_libdir}/libgstplayer-%{majorminor}.so.*
%{_libdir}/libgstisoff-%{majorminor}.so.*
%{_libdir}/libgstwebrtc-%{majorminor}.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libgstphotography-%{majorminor}.so
%{_libdir}/libgstinsertbin-%{majorminor}.so
%{_libdir}/libgstcodecparsers-%{majorminor}.so
%{_libdir}/libgstmpegts-%{majorminor}.so
%{_libdir}/libgsturidownloader-%{majorminor}.so
%{_libdir}/libgstbasecamerabinsrc-%{majorminor}.so
%{_libdir}/libgstbadvideo-%{majorminor}.so
%{_libdir}/libgstadaptivedemux-%{majorminor}.so
%{_libdir}/libgstbadaudio-%{majorminor}.so
%{_libdir}/libgstplayer-%{majorminor}.so
%{_libdir}/libgstisoff-%{majorminor}.so
%{_libdir}/libgstwebrtc-%{majorminor}.so
%{_includedir}/gstreamer-%{majorminor}/gst/interfaces/photography-enumtypes.h
%{_includedir}/gstreamer-%{majorminor}/gst/interfaces/photography.h
%{_includedir}/gstreamer-%{majorminor}/gst/codecparsers/gsth264parser.h
%{_includedir}/gstreamer-%{majorminor}/gst/codecparsers/gsth265parser.h
%{_includedir}/gstreamer-%{majorminor}/gst/codecparsers/gstjpegparser.h
%{_includedir}/gstreamer-%{majorminor}/gst/codecparsers/gstjpeg2000sampling.h
%{_includedir}/gstreamer-%{majorminor}/gst/codecparsers/gstmpeg4parser.h
%{_includedir}/gstreamer-%{majorminor}/gst/codecparsers/gstmpegvideometa.h
%{_includedir}/gstreamer-%{majorminor}/gst/codecparsers/gstmpegvideoparser.h
%{_includedir}/gstreamer-%{majorminor}/gst/codecparsers/gstvc1parser.h
%{_includedir}/gstreamer-%{majorminor}/gst/codecparsers/gstvp8parser.h
%{_includedir}/gstreamer-%{majorminor}/gst/codecparsers/gstvp8rangedecoder.h
%{_includedir}/gstreamer-%{majorminor}/gst/codecparsers/gstvp9parser.h
%{_includedir}/gstreamer-%{majorminor}/gst/insertbin/gstinsertbin.h
%{_includedir}/gstreamer-%{majorminor}/gst/basecamerabinsrc/gstbasecamerasrc.h
%{_includedir}/gstreamer-%{majorminor}/gst/basecamerabinsrc/gstcamerabin-enum.h
%{_includedir}/gstreamer-%{majorminor}/gst/basecamerabinsrc/gstcamerabinpreview.h
%{_includedir}/gstreamer-%{majorminor}/gst/mpegts/gst-atsc-section.h
%{_includedir}/gstreamer-%{majorminor}/gst/mpegts/gst-dvb-descriptor.h
%{_includedir}/gstreamer-%{majorminor}/gst/mpegts/gst-dvb-section.h
%{_includedir}/gstreamer-%{majorminor}/gst/mpegts/gstmpegtsdescriptor.h
%{_includedir}/gstreamer-%{majorminor}/gst/mpegts/gstmpegtssection.h
%{_includedir}/gstreamer-%{majorminor}/gst/mpegts/mpegts.h
%{_includedir}/gstreamer-%{majorminor}/gst/mpegts/gstmpegts-enumtypes.h
%{_includedir}/gstreamer-%{majorminor}/gst/mpegts/gst-scte-section.h
%{_includedir}/gstreamer-%{majorminor}/gst/uridownloader/gstfragment.h
%{_includedir}/gstreamer-%{majorminor}/gst/uridownloader/gsturidownloader.h
%{_includedir}/gstreamer-%{majorminor}/gst/uridownloader/gsturidownloader_debug.h
%{_includedir}/gstreamer-%{majorminor}/gst/player/gstplayer-g-main-context-signal-dispatcher.h
%{_includedir}/gstreamer-%{majorminor}/gst/player/gstplayer-media-info.h
%{_includedir}/gstreamer-%{majorminor}/gst/player/gstplayer-signal-dispatcher.h
%{_includedir}/gstreamer-%{majorminor}/gst/player/gstplayer-types.h
%{_includedir}/gstreamer-%{majorminor}/gst/player/gstplayer-video-overlay-video-renderer.h
%{_includedir}/gstreamer-%{majorminor}/gst/player/gstplayer-video-renderer.h
%{_includedir}/gstreamer-%{majorminor}/gst/player/gstplayer-visualization.h
%{_includedir}/gstreamer-%{majorminor}/gst/player/gstplayer.h
%{_includedir}/gstreamer-%{majorminor}/gst/player/player.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/gstvideoaggregator.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/gstvideoaggregatorpad.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/audio-bad-prelude.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/gstnonstreamaudiodecoder.h
%{_includedir}/gstreamer-%{majorminor}/gst/basecamerabinsrc/basecamerabinsrc-prelude.h
%{_includedir}/gstreamer-%{majorminor}/gst/codecparsers/codecparsers-prelude.h
%{_includedir}/gstreamer-%{majorminor}/gst/interfaces/photography-prelude.h
%{_includedir}/gstreamer-%{majorminor}/gst/isoff/gstisoff.h
%{_includedir}/gstreamer-%{majorminor}/gst/mpegts/mpegts-prelude.h
%{_includedir}/gstreamer-%{majorminor}/gst/player/player-prelude.h
%{_includedir}/gstreamer-%{majorminor}/gst/uridownloader/uridownloader-prelude.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/video-bad-prelude.h
%{_includedir}/gstreamer-%{majorminor}/gst/webrtc/dtlstransport.h
%{_includedir}/gstreamer-%{majorminor}/gst/webrtc/icetransport.h
%{_includedir}/gstreamer-%{majorminor}/gst/webrtc/rtcsessiondescription.h
%{_includedir}/gstreamer-%{majorminor}/gst/webrtc/rtpreceiver.h
%{_includedir}/gstreamer-%{majorminor}/gst/webrtc/rtpsender.h
%{_includedir}/gstreamer-%{majorminor}/gst/webrtc/rtptransceiver.h
%{_includedir}/gstreamer-%{majorminor}/gst/webrtc/webrtc-enumtypes.h
%{_includedir}/gstreamer-%{majorminor}/gst/webrtc/webrtc.h
%{_includedir}/gstreamer-%{majorminor}/gst/webrtc/webrtc_fwd.h
%{_libdir}/pkgconfig/gstreamer-plugins-bad-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-codecparsers-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-insertbin-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-mpegts-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-bad-audio-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-bad-video-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-player-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-webrtc-%{majorminor}.pc
