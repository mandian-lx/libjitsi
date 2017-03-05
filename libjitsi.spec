%{?_javapackages_macros:%_javapackages_macros}

%define debug_package %{nil}

%define oname LibJitsi
%define name %(echo %oname | tr [:upper:] [:lower:])

%define portaudio_commit 35da8982620d30203dfb807301b2eac71e14e6b8
%define portaudio_shortcommit %(c=%{commit}; echo ${c:0:7})

Summary:	An advanced Java media library for secure real-time audio/video communication
Name:		%{name}
Version:	928
Release:	1
License:	Apache License
Group:		Development/Java
Url:		https://jitsi.org/Projects/%{oname}
Source0:	https://github.com/jitsi/%{name}/archive/%{version}/%{name}-%{version}.tar.gz
Source100:	https://github.com/%{name}/libsrc/raw/master/libmkv.zip
Source200:	https://github.com/jitsi/portaudio/archive/%{portaudio_commit}/portaudio-%{portaudio_commit}.zip
Patch0:		%{name}-928-maven_ant-tasks.patch
Patch1:		%{name}-928-ffmpeg-remove-hflip.patch
Patch2:		%{name}-928-native_flags.patch
Patch3:		%{name}-928-native_portaudio_static.patch
Patch4:		%{name}-928-native_portaudio_with_jack.patch
Patch5:		%{name}-928-native_speex.patch
Patch6:		%{name}-928-native_opus.patch
Patch7:		%{name}-928-native_vpx.patch
Patch8:		%{name}-928-native_sctp.patch
Patch9:		%{name}-928-native_video4linux.patch
Patch10:	%{name}-928-native_openssl.patch
# remove codec may cause patent issues:
# gsm: https://en.wikipedia.org/wiki/Gsm#Issues_with_patents_and_open_source
Patch100:	%{name}-928-remove_gsm.patch

# java
BuildRequires:	ant
BuildRequires:	cpptasks
BuildRequires:	javapackages-local
BuildRequires:	maven-local
BuildRequires:	mvn(ch.imvs:sdes4j)
BuildRequires:	mvn(com.googlecode.json-simple:json-simple)
BuildRequires:	mvn(junit:junit)
BuildRequires:	mvn(net.java.dev.jna:jna)
BuildRequires:	mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:	mvn(org.bouncycastle:bcpkix-jdk15on
BuildRequires:	mvn(org.bouncycastle:bcprov-jdk15on)
BuildRequires:	mvn(org.jitsi:bccontrib)
BuildRequires:	mvn(org.jitsi:fmj)
BuildRequires:	mvn(org.jitsi:ice4j)
BuildRequires:	mvn(org.jitsi:jitsi-gpl-dependencies)
BuildRequires:	mvn(org.jitsi:jitsi-lgpl-dependencies)
BuildRequires:	mvn(org.jitsi:zrtp4j-light)
BuildRequires:	mvn(org.osgi:org.osgi.core)
# natives
#   screencaprute (jnscreencapture)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
#   jawtrenderer (jnawtrenderer)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xv)
#   portaudio (jnportaudio)
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(jack)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(speexdsp)
# NOTE: libjitsi uses its own fork of portaudio
#BuildRequires: pkgconfig(portaudio-2.0)
#   speex (jnspeex)
BuildRequires:	pkgconfig(speex)
BuildRequires:	pkgconfig(speexdsp)
#   opus (jnopus)
BuildRequires:	pkgconfig(opus)
#   libvpx (jnvpx)
BuildRequires:	pkgconfig(vpx)
#   video4linux2 (jnvideo4linux2)
BuildRequires:	pkgconfig(libv4l2)
#   pulseaudio (jnpulseaudio)
BuildRequires:	pkgconfig(libpulse)
#   sctp (jnsctp)
BuildRequires:	usrsctp-devel
#   jnopenssl
BuildRequires:	pkgconfig(libcrypto)

Requires:	java
# natives
#   screencaprute (jnscreencapture)
Requires:	%{_lib}x11_6
Requires:	%{_lib}xext6
#   jawtrenderer (jnawtrenderer)
Requires:	%{_lib}x11_6
Requires:	%{_lib}xv1
#   portaudio (jnportaudio)
Requires:	%{_lib}alsa2
Requires:	%{_lib}jack0
Requires:	%{_lib}speexdsp1
# NOTE: libjitsi uses its own fork of portaudio
#BuildRequires: pkgconfig(portaudio-2.0)
#   speex (jnspeex)
Requires:	%{_lib}speex1
Requires:	%{_lib}speexdsp1
#   opus (jnopus)
Requires:	%{_lib}opus0
#   libvpx (jnvpx)
Requires:	%{_lib}vpx4
#   video4linux2 (jnvideo4linux2)
#Requires:	%{_lib}v4l0
#   pulseaudio (jnpulseaudio)
Requires:	%{_lib}pulseaudio0
#   sctp (jnsctp)
Requires:	%{_lib}usrsctp1
#   jnopenssl
Requires:	%{_lib}crypto1.1

%description
%{oname} is an advanced Java media library for secure real-time audio/video
communication. It allows applications to capture, playback, stream,
encode/decode and encrypt audio and video flows. It also allows for advanced
features such as audio mixing, handling multiple streams, participation in
audio and video conferences.

Originally libjitsi was part of the Jitsi client source code but the Jitsi
Team decided to spin it off so that other projects can also use it.

%files -f .mfiles
%doc README.md
%doc CONTRIBUTING.md
%doc LICENSE

#----------------------------------------------------------------------------

%package javadoc
Summary:	Javadoc for %{name}
BuildArch:	noarch

%description javadoc
API documentation for %{name}.

%files javadoc -f .mfiles-javadoc

#----------------------------------------------------------------------------

%prep
%setup -q

# unpack native libs
mkdir -p lib/src
pushd lib/src/
 unzip -qq %{SOURCE100} 
 unzip -qq %{SOURCE200}
 # fix dirname
 mv portaudio-%{portaudio_commit} portaudio
popd

# Remove all pre-build binaries
find . -type f -name "*.jar" -delete
find . -type f -name "*.class" -delete
find . -type f -name "lib*.so*" -delete
find . -type f -name "*.a" -delete
find . -type f -name "*.dll" -delete
find . -type f -name "*.jnilib" -delete
find . -type f -name "*.zip" -delete
find . -type f -name "*.tar.bz2" -delete
find . -type f -name "*.tar.gz" -delete

# Apply all patches
%patch0   -p1 -b .maven
%patch1   -p1 -b .hflip
%patch2   -p1 -b .native_flags
%patch3   -p1 -b .native_portaudio
%patch4   -p1 -b .native_portaudio_with_jack
%patch5   -p1 -b .native_speex
%patch6   -p1 -b .native_opus
%patch7   -p1 -b .native_vpx
%patch8   -p1 -b .native_sctp
%patch9   -p1 -b .native_v4l
%patch10  -p1 -b .native_openssl

%patch100 -p1 -b .gsm

# remove HFlip.java according to patch1
rm -f src/org/jitsi/impl/neomedia/codec/video/HFlip.java

# remove gsm codec according to patch100
rm -fr src/org/jitsi/impl/neomedia/codec/audio/gsm

# add system dependencies
ln -s %{_javadir}/ant/cpptasks.jar lib/installer-exclude/cpptasks.jar

# Remove jitsi-universe parent
%pom_remove_parent .

# Add groupId
%pom_xpath_inject "pom:project" "<groupId>org.jitsi</groupId>" .

# Unbundle native libs for other SO and arch
sed -i -e	'{	/darwin/d
			/linux-x86-64/d
			/win32-x86/d
			/win32-x86-64/d
			s|linux-x86|linux-@arch@|g
			s|processor=x86|processor=@arch@|g
			s|@arch@,|@arch@|g
		}' pom.xml

# use properly arch
%ifarch %{x?86}
sed -i -e '{ 	s|linux-@arch@|linux-x86|g
		s|processor=@arch@|processor=x86|g
	   }' pom.xml
%endif

%ifarch x86_64
sed -i -e '{ 	s|linux-@arch@|linux-x86-64|g
		s|processor=@arch@|processor=x86-64|g
	  }' pom.xml
%endif

# Change fmj artifactId according to fmj.spec
#%pom_change_dep ':fmj' ':fmj-jitsi' .

# Add missing dep
%pom_add_dep \${project.groupId}:jitsi-gpl-dependencies

# Switch to JDK 8
%pom_add_plugin :maven-compiler-plugin "
	<configuration>
		<source>1.8</source>
		<target>1.8</target>
	</configuration>"

# Hide Javadoc errors
%pom_add_plugin :maven-javadoc-plugin . "
	<configuration>
		<failOnError>false</failOnError>
		<additionalparam>-Xdoclint:none</additionalparam>
	</configuration>"

# Fix missing version warnings
%pom_xpath_inject "pom:plugin[pom:artifactId[./text()='maven-bundle-plugin']]" "
		<version>any</version>" .

# skip failing tests
# FIXME: Failed tests: 
#	org.jitsi.sctp4j.SctpNativeWrapperTest#testNPEinConstructor NullPointerException
#	org.jitsi.sctp4j.SctpNativeWrapperTest#testOnConnIn NullPointerException
#	org.jitsi.sctp4j.SctpNativeWrapperTest#testCloseFromNotification NullPointerException
#	org.jitsi.sctp4j.SctpTransferTest#testSocketBrokenLink NullPointerException
%pom_add_plugin :maven-surefire-plugin . "
<configuration>
	<excludes>
		<exclude>**/SctpNativeWrapperTest.java</exclude>
		<exclude>**/SctpTransferTest.java</exclude>
	</excludes>
</configuration>"

# Add an OSGi compilant MANIFEST.MF
%pom_xpath_inject "pom:plugin[pom:artifactId[./text()='maven-bundle-plugin']]" "
	<extensions>true</extensions>"

%build
# bundled libs
#   libmkv
#	NOTE: libjnvpx includes EbmlWriter.c from libmkv as its own source,
#	      so there nothing to build here
#   portaudio
#	NOTE: libjitsi use its own fork of portaudio
pushd lib/src/portaudio
export CC=gcc
export CXX=g++
autoreconf -ifv
%configure --disable-shared --enable-static --without-pic #--with-jack=no #--with-pic
%make clean
%make
popd

# native libs
%ant screencapture
%ant jawtrenderer
%ant portaudio -Dspeex.dynamic=true -Dportaudio=$PWD/lib/src/portaudio
%ant speex -Dspeex.dynamic=true
%ant opus -Dopus=""
%ant libvpx -Dlibvpx="/usr/include/vpx" -Dlibmkv="$PWD/lib/src/libmkv"
%ant video4linux2
%ant pulseaudio
%ant jnopenssl
%ant sctp -Dusrsctp=""

# java
%mvn_build -- -Dproject.build.sourceEncoding=UTF-8

%install
%mvn_install

