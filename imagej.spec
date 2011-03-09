Name:           imagej
Version:        1.45b
Release:        %mkrel 2
Summary:        Image Processing and Analysis in Java

Group:          Sciences/Biology
License:        Public Domain
URL:            http://rsbweb.nih.gov/ij/index.html
Source0:        http://rsbweb.nih.gov/ij/download/src/ij145b-src.zip
Source1:        %{name}.desktop
Source2:        http://rsbweb.nih.gov/ij/macros/macros.zip
Source3:        http://rsb.info.nih.gov/ij/download/linux/unix-script.txt
# don't copy .class files for Mac OS
patch0:         %{name}-%{version}-patch0.patch
# modify imagej.sh for fedora compatibility
patch1:         %{name}-%{version}-patch1.patch
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


BuildRequires:  ant
BuildRequires:	desktop-file-utils

# Requires:       jpackage-utils
# java-devel not java for plugins build
Requires:       java >= 1.6.0

%description
ImageJ is a public domain Java image processing program. It can display,        
edit, analyze a wide variety of image data, including image sequences. Imagej   
can be used for quantitative analysis of engineering and scientific image data.

%package javadoc
Summary:        Javadocs for %{name}
Group:          Development Documentation
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -c -n "%{name}-%{version}" 
# patch build.xml
%patch0 -p0 -b .patch0
# unzip macros.zip
unzip -qq -u %{SOURCE2} 
# erase binary and useless files 
rm -rf macros/.FBC*
rm macros/build.xml
rm -rf __MACOSX
#get and patch unix-script.txt
cp %{SOURCE3} ./imagej.sh
%patch1 -p1 -b .patch1

find -name '*.class' -exec rm -f '{}' \;
find -name '*.jar' -exec rm -f '{}' \;

%build
cd source
ant build javadocs
cd ..

%install
rm -rf $RPM_BUILD_ROOT

# install jar
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p source/ij.jar   \
$RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar


# install javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -rp api  \
$RPM_BUILD_ROOT%{_javadocdir}/%{name}

# install icon
mkdir -p $RPM_BUILD_ROOT%{_datadir}/pixmaps
cp -p source/build/microscope.gif $RPM_BUILD_ROOT%{_datadir}/pixmaps

# install data files
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -p source/build/about.jpg $RPM_BUILD_ROOT%{_datadir}/%{name}/about.jpg
cp -p source/build/IJ_Props.txt $RPM_BUILD_ROOT%{_datadir}/%{name}/IJ_Props.txt

#install macros
chmod 644 macros/About\ Startup\ Macros 
find ./macros -name \*.txt -type f -exec chmod 644 {} \;
find ./macros -type d -exec chmod 755 {} \;
cp -rp macros $RPM_BUILD_ROOT%{_datadir}/%{name}


#install luts
mkdir $RPM_BUILD_ROOT%{_datadir}/%{name}/luts 

# install script
mkdir -p $RPM_BUILD_ROOT%{_bindir}
chmod +x imagej.sh
cp -p imagej.sh $RPM_BUILD_ROOT%{_bindir}/%{name}

# directory for plugins
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}/plugins
cp source/plugins/JavaScriptEvaluator.source $RPM_BUILD_ROOT%{_datadir}/%{name}/plugins/JavaScriptEvaluator.java

# desktop file
desktop-file-install --vendor=""                     \
       --dir=%{buildroot}%{_datadir}/applications/   \
       %{SOURCE1}

%post

#update icon cache
#touch --no-create %{_datadir}/icons/hicolor
#if [ -x %{_bindir}/gtk-update-icon-cache ]; then
#  %{_bindir}/gtk-update-icon-cache -q %{_datadir}/icons/hicolor;
#fi
#update-desktop-database &> /dev/null || :

%postun
# update icon cache
#touch --no-create %{_datadir}/icons/hicolor
#if [ -x %{_bindir}/gtk-update-icon-cache ]; then
#  %{_bindir}/gtk-update-icon-cache -q %{_datadir}/icons/hicolor;
#fi
#update-desktop-database &> /dev/null || :


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_javadir}/*
%{_datadir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/microscope.gif
%{_bindir}/%{name}
%doc source/aREADME.txt source/release-notes.html source/applet.html

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}


