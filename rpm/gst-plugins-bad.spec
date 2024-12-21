%define majorminor   1.0
%define gstreamer    gstreamer

%global _vpath_srcdir subprojects/gst-plugins-bad
%global _vpath_builddir subprojects/gst-plugins-bad/_build

Summary:     GStreamer streaming media framework "bad" plug-ins
Name:        %{gstreamer}%{majorminor}-plugins-bad
Version:     1.24.10
Release:     1
License:     LGPLv2+
URL:         http://gstreamer.freedesktop.org/
Source:      %{name}-%{version}.tar.xz
Patch1:      0001-Set-video-branch-to-NULL-after-finishing-video-recor.patch
Patch2:      0002-Keep-video-branch-in-NULL-state.patch
Patch3:      0003-jifmux-cope-with-missing-EOI-marker.patch
Patch4:      0004-Don-t-build-dxva-on-non-windows-platforms.patch
Patch5:      0005-Revert-jpegparse-bump-to-primary-rank.patch

%define sonamever %(echo %{version} | cut -d '+' -f 1)

Requires:      orc >= 0.4.18
BuildRequires: pkgconfig(gstreamer-plugins-base-1.0) >= %{sonamever}
BuildRequires: gstreamer1.0-tools
BuildRequires: check
BuildRequires: pkgconfig(nice) >= 0.1.14
BuildRequires: pkgconfig(libexif)
BuildRequires: pkgconfig(orc-0.4) >= 0.4.18
BuildRequires: pkgconfig(libgcrypt)
BuildRequires: pkgconfig(wayland-egl)
BuildRequires: pkgconfig(wayland-protocols) >= 1.15
BuildRequires: pkgconfig(glesv2)
BuildRequires: pkgconfig(aom)
BuildRequires: pkgconfig(egl)
BuildRequires: pkgconfig(opus)
BuildRequires: pkgconfig(libwebp)
BuildRequires: pkgconfig(libxml-2.0)
BuildRequires: pkgconfig(libssl)
BuildRequires: pkgconfig(libcrypto)
BuildRequires: pkgconfig(libsrtp2)
BuildRequires: pkgconfig(gobject-introspection-1.0)
BuildRequires: pkgconfig(libusb-1.0)
BuildRequires: pkgconfig(gudev-1.0)
BuildRequires: pkgconfig(pangocairo)
BuildRequires: pkgconfig(libopenjp2)
BuildRequires: pkgconfig(libgcrypt)
BuildRequires: pkgconfig(sbc)
BuildRequires: pkgconfig(libsrtp2)
BuildRequires: pkgconfig(sndfile)
BuildRequires: pkgconfig(libdrm)
%ifnarch %{ix86} x86_64
BuildRequires: libatomic
%endif
BuildRequires: meson
BuildRequires: gettext-devel

%description
GStreamer is a streaming media framework, based on graphs of elements which
operate on media data.

%package devel
Summary: Development files for the GStreamer media framework "bad" plug-ins
Requires: %{name} = %{version}-%{release}
Requires: gstreamer1.0-plugins-base-devel

%description devel
GStreamer is a streaming media framework, based on graphs of elements which
operate on media data.

This package contains the development files for the plug-ins that
are not tested well enough, or the code is not of good enough quality.

%package apps
Summary:    GStreamer Plugins Bad library applications
Requires:   %{gstreamer}1.0-plugins-base = %{version}

%description apps
GStreamer Plugins Bad library applications

%prep
%autosetup -p1 -n gstreamer1.0-plugins-bad-%{version}/gstreamer

%build

# OBS inserts --auto-features=enabled to verify that every plugin is
# specified one way or the other. Add this below for testing.
%meson \
  -Dpackage-name='SailfishOS GStreamer package plugins (bad set)' \
  -Dpackage-origin='http://sailfishos.org/' -Dorc=enabled \
  -Dintrospection=enabled -Dexamples=disabled -Ddoc=disabled -Dnls=disabled \
  -Daccurip=disabled -Dadpcmdec=disabled -Dadpcmenc=disabled -Daom=disabled \
  -Daes=disabled -Daom=enabled -Damfcodec=disabled -Dasfmux=disabled -D=assrender=disabled \
  -Daudiofxbad=disabled -Daudiovisualizers=disabled -Dautoconvert=disabled \
  -Dbayer=disabled -Dbluez=disabled -Dbs2b=disabled -Dbz2=disabled \
  -Dchromaprint=disabled -Dcoloreffects=disabled -Dcurl=disabled -Ddash=disabled \
  -Daja=disabled -Ddc1394=disabled -Dcodec2json=disabled -Dcodecalpha=disabled \
  -Ddebugutils=enabled -Ddecklink=disabled -D=directfb=disabled -Ddirectshow=disabled \
  -Ddts=disabled -Ddvb=disabled -Ddvbsuboverlay=disabled -Ddvdspu=disabled \
  -Dfaac=disabled -Dfaad=disabled -Dfaceoverlay=disabled -Dfbdev=disabled \
  -Dfdkaac=disabled -Dfestival=disabled -Dfieldanalysis=disabled \
  -Dflite=disabled -Dfluidsynth=disabled -Dfreeverb=disabled -Dfrei0r=disabled \
  -Dgs=disabled -Dgaudieffects=disabled -Dgdp=disabled -Dgeometrictransform=disabled \
  -Dgme=disabled -Dgsm=disabled -Dgtk3=disabled -Did3tag=disabled -Dinter=disabled \
  -Disac=disabled -Dinterlace=disabled -Diqa=disabled -Divfparse=disabled \
  -Divtc=disabled -Djp2kdecimator=disabled -Dladspa=disabled -Dlc3=disabled \
  -Dldac=disabled -Dlibde265=disabled -Dlibrfb=disabled -Dlv2=disabled \
  -Dmidi=disabled -Dmodplug=disabled -Dmpeg2enc=disabled -Dmpegpsmux=disabled \
  -Dmpegtsmux=disabled -Dmplex=disabled -Dmsdk=disabled -Dmusepack=disabled \
  -Dmxf=disabled -Dneon=disabled -Donnx=disabled \
  -Dopenal=disabled -Dopenaptx=disabled -Dopencv=disabled -Dopenexr=disabled \
  -Dopenh264=disabled -Dopenmpt=disabled -Dopenni2=disabled -Dopensles=disabled \
  -Dpcapparse=disabled -Dpnm=disabled -Dqroverlay=disabled -Dqsv=disabled \
  -Dqt6d3d11=disabled \
  -Dremovesilence=disabled -Dresindvd=disabled -Drsvg=disabled -Drtmp=disabled \
  -Dsctp=enabled -Dsdp=disabled -Dsegmentclip=disabled -Dsiren=disabled \
  -Dsmooth=disabled -Dsmoothstreaming=disabled -Dsoundtouch=disabled \
  -Dspandsp=disabled -Dspeed=disabled -Dsrt=disabled -Dsubenc=disabled -Dsvtav1=disabled \
  -Dteletext=disabled -Dtinyalsa=disabled -Dvideofilters=disabled \
  -Dvideosignal=disabled -Dvmnc=disabled -Dvoaacenc=disabled \
  -Dvoamrwbenc=disabled -Dvulkan=disabled -Dwasapi=disabled -Dwasapi2=disabled \
  -Dwebrtcdsp=disabled -Dwildmidi=disabled -Dwpe=disabled -Dx11=disabled \
  -Dx265=disabled -Dy4m=disabled -Dzbar=disabled -Dcolormanagement=disabled \
  -Dmagicleap=disabled -Dva=disabled -Davtp=disabled -Dmicrodns=disabled \
  -Dsvthevcenc=disabled -Dzxing=disabled

%meson_build

%install
%meson_install

# Clean out files that should not be part of the rpm.
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a

# remove waylandsink. It does not run because we do not support all the interfaces it needs.
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstwaylandsink.so
rm -f $RPM_BUILD_ROOT%{_libdir}/libgstwayland-%{majorminor}.so*

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post devel -p /sbin/ldconfig
%postun devel -p /sbin/ldconfig

%files
%license subprojects/gst-plugins-bad/COPYING
%{_libdir}/gstreamer-%{majorminor}/libgstaiff.so
%{_libdir}/gstreamer-%{majorminor}/libgstanalyticsoverlay.so
%{_libdir}/gstreamer-%{majorminor}/libgstaom.so
%{_libdir}/gstreamer-%{majorminor}/libgstaudiobuffersplit.so
%{_libdir}/gstreamer-%{majorminor}/libgstaudiolatency.so
%{_libdir}/gstreamer-%{majorminor}/libgstaudiomixmatrix.so
%{_libdir}/gstreamer-%{majorminor}/libgstcamerabin.so
%{_libdir}/gstreamer-%{majorminor}/libgstclosedcaption.so
%{_libdir}/gstreamer-%{majorminor}/libgstcodectimestamper.so
%{_libdir}/gstreamer-%{majorminor}/libgstdebugutilsbad.so
%{_libdir}/gstreamer-%{majorminor}/libgstdtls.so
%{_libdir}/gstreamer-%{majorminor}/libgstdvbsubenc.so
%{_libdir}/gstreamer-%{majorminor}/libgsthls.so
%{_libdir}/gstreamer-%{majorminor}/libgstinsertbin.so
%{_libdir}/gstreamer-%{majorminor}/libgstipcpipeline.so
%{_libdir}/gstreamer-%{majorminor}/libgstjpegformat.so
%{_libdir}/gstreamer-%{majorminor}/libgstkms.so
%{_libdir}/gstreamer-%{majorminor}/libgstlegacyrawparse.so
%{_libdir}/gstreamer-%{majorminor}/libgstmpegpsdemux.so
%{_libdir}/gstreamer-%{majorminor}/libgstmpegtsdemux.so
%{_libdir}/gstreamer-%{majorminor}/libgstmse.so
%{_libdir}/gstreamer-%{majorminor}/libgstnetsim.so
%{_libdir}/gstreamer-%{majorminor}/libgstnvcodec.so
%{_libdir}/gstreamer-%{majorminor}/libgstopenjpeg.so
%{_libdir}/gstreamer-%{majorminor}/libgstopusparse.so
%{_libdir}/gstreamer-%{majorminor}/libgstproxy.so
%{_libdir}/gstreamer-%{majorminor}/libgstrist.so
%{_libdir}/gstreamer-%{majorminor}/libgstrtmp2.so
%{_libdir}/gstreamer-%{majorminor}/libgstrtpmanagerbad.so
%{_libdir}/gstreamer-%{majorminor}/libgstrtponvif.so
%{_libdir}/gstreamer-%{majorminor}/libgstsbc.so
%{_libdir}/gstreamer-%{majorminor}/libgstsctp.so
%{_libdir}/gstreamer-%{majorminor}/libgstshm.so
%{_libdir}/gstreamer-%{majorminor}/libgstsndfile.so
%{_libdir}/gstreamer-%{majorminor}/libgstsrtp.so
%{_libdir}/gstreamer-%{majorminor}/libgstswitchbin.so
%{_libdir}/gstreamer-%{majorminor}/libgsttimecode.so
%{_libdir}/gstreamer-%{majorminor}/libgsttranscode.so
%{_libdir}/gstreamer-%{majorminor}/libgstttmlsubs.so
%{_libdir}/gstreamer-%{majorminor}/libgstunixfd.so
%{_libdir}/gstreamer-%{majorminor}/libgstuvcgadget.so
%{_libdir}/gstreamer-%{majorminor}/libgstuvch264.so
%{_libdir}/gstreamer-%{majorminor}/libgstv4l2codecs.so
%{_libdir}/gstreamer-%{majorminor}/libgstvideoframe_audiolevel.so
%{_libdir}/gstreamer-%{majorminor}/libgstvideoparsersbad.so
%{_libdir}/gstreamer-%{majorminor}/libgstwebp.so
%{_libdir}/gstreamer-%{majorminor}/libgstwebrtc.so
%{_libdir}/libgstadaptivedemux-%{majorminor}.so.*
%{_libdir}/libgstanalytics-%{majorminor}.so.*
%{_libdir}/libgstbadaudio-%{majorminor}.so.*
%{_libdir}/libgstbasecamerabinsrc-%{majorminor}.so.*
%{_libdir}/libgstcodecparsers-%{majorminor}.so.*
%{_libdir}/libgstcodecs-%{majorminor}.so.*
%{_libdir}/libgstcuda-%{majorminor}.so.*
%{_libdir}/libgstinsertbin-%{majorminor}.so.*
%{_libdir}/libgstisoff-%{majorminor}.so.*
%{_libdir}/libgstmpegts-%{majorminor}.so.*
%{_libdir}/libgstmse-%{majorminor}.so.*
%{_libdir}/libgstphotography-%{majorminor}.so.*
%{_libdir}/libgstplay-%{majorminor}.so.*
%{_libdir}/libgstplayer-%{majorminor}.so.*
%{_libdir}/libgstsctp-%{majorminor}.so.*
%{_libdir}/libgsturidownloader-%{majorminor}.so.*
%{_libdir}/libgstwebrtc-%{majorminor}.so.*
%{_libdir}/libgstwebrtcnice-%{majorminor}.so.*
%{_libdir}/libgsttranscoder-%{majorminor}.so.*
%{_libdir}/girepository-1.0/CudaGst-1.0.typelib
%{_libdir}/girepository-1.0/GstAnalytics-1.0.typelib
%{_libdir}/girepository-1.0/GstBadAudio-1.0.typelib
%{_libdir}/girepository-1.0/GstCodecs-1.0.typelib
%{_libdir}/girepository-1.0/GstCuda-1.0.typelib
%{_libdir}/girepository-1.0/GstInsertBin-1.0.typelib
%{_libdir}/girepository-1.0/GstMpegts-1.0.typelib
%{_libdir}/girepository-1.0/GstMse-1.0.typelib
%{_libdir}/girepository-1.0/GstPlay-1.0.typelib
%{_libdir}/girepository-1.0/GstPlayer-1.0.typelib
%{_libdir}/girepository-1.0/GstTranscoder-1.0.typelib
%{_libdir}/girepository-1.0/GstWebRTC-1.0.typelib
%dir %{_datadir}/gstreamer-%{majorminor}/encoding-profiles
%{_datadir}/gstreamer-%{majorminor}/encoding-profiles/device/*.gep
%{_datadir}/gstreamer-%{majorminor}/encoding-profiles/file-extension/*.gep
%{_datadir}/gstreamer-%{majorminor}/encoding-profiles/online-services/*.gep

%files devel
%{_libdir}/libgstadaptivedemux-%{majorminor}.so
%{_libdir}/libgstanalytics-%{majorminor}.so
%{_libdir}/libgstbadaudio-%{majorminor}.so
%{_libdir}/libgstbasecamerabinsrc-%{majorminor}.so
%{_libdir}/libgstcodecparsers-%{majorminor}.so
%{_libdir}/libgstcodecs-%{majorminor}.so
%{_libdir}/libgstcuda-%{majorminor}.so
%{_libdir}/libgstinsertbin-%{majorminor}.so
%{_libdir}/libgstisoff-%{majorminor}.so
%{_libdir}/libgstmpegts-%{majorminor}.so
%{_libdir}/libgstmse-%{majorminor}.so
%{_libdir}/libgstphotography-%{majorminor}.so
%{_libdir}/libgstplay-%{majorminor}.so
%{_libdir}/libgstplayer-%{majorminor}.so
%{_libdir}/libgstsctp-%{majorminor}.so
%{_libdir}/libgsttranscoder-%{majorminor}.so
%{_libdir}/libgsturidownloader-%{majorminor}.so
%{_libdir}/libgstwebrtc-%{majorminor}.so
%{_libdir}/libgstwebrtcnice-%{majorminor}.so
%{_includedir}/gstreamer-%{majorminor}/gst/analytics/*.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/*.h
%{_includedir}/gstreamer-%{majorminor}/gst/basecamerabinsrc/*.h
%{_includedir}/gstreamer-%{majorminor}/gst/codecparsers/*.h
%{_includedir}/gstreamer-%{majorminor}/gst/cuda/*.h
%{_includedir}/gstreamer-%{majorminor}/gst/insertbin/gstinsertbin.h
%{_includedir}/gstreamer-%{majorminor}/gst/interfaces/photography*.h
%{_includedir}/gstreamer-%{majorminor}/gst/isoff/gstisoff.h
%{_includedir}/gstreamer-%{majorminor}/gst/mpegts/*.h
%{_includedir}/gstreamer-%{majorminor}/gst/mse/*.h
%{_includedir}/gstreamer-%{majorminor}/gst/play/*.h
%{_includedir}/gstreamer-%{majorminor}/gst/player/gstplayer*.h
%{_includedir}/gstreamer-%{majorminor}/gst/player/player*.h
%{_includedir}/gstreamer-%{majorminor}/gst/sctp/*.h
%{_includedir}/gstreamer-%{majorminor}/gst/transcoder/*.h
%{_includedir}/gstreamer-%{majorminor}/gst/uridownloader/*.h
%{_includedir}/gstreamer-%{majorminor}/gst/wayland/*.h
%{_includedir}/gstreamer-%{majorminor}/gst/webrtc/*.h
%{_includedir}/gstreamer-%{majorminor}/gst/webrtc/nice/*.h
%{_libdir}/pkgconfig/gstreamer-analytics-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-bad-audio-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-codecparsers-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-cuda-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-insertbin-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-mpegts-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-mse-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-photography-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-play-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-player-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-plugins-bad-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-sctp-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-transcoder-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-wayland-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-webrtc-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-webrtc-nice-%{majorminor}.pc
%{_datadir}/gir-1.0/CudaGst-1.0.gir
%{_datadir}/gir-1.0/GstAnalytics-1.0.gir
%{_datadir}/gir-1.0/GstBadAudio-1.0.gir
%{_datadir}/gir-1.0/GstCodecs-1.0.gir
%{_datadir}/gir-1.0/GstCuda-1.0.gir
%{_datadir}/gir-1.0/GstInsertBin-1.0.gir
%{_datadir}/gir-1.0/GstMpegts-1.0.gir
%{_datadir}/gir-1.0/GstMse-1.0.gir
%{_datadir}/gir-1.0/GstPlay-1.0.gir
%{_datadir}/gir-1.0/GstPlayer-1.0.gir
%{_datadir}/gir-1.0/GstTranscoder-1.0.gir
%{_datadir}/gir-1.0/GstWebRTC-1.0.gir

%files apps
%{_bindir}/gst-transcoder-%{majorminor}
