Name:           imagej
Version:        1.52r
Release:        Name:           imagej
Version:        1.52r
Release:        1
Summary:        Image Processing and Analysis in Java

Group:          Sciences/Computer science
License:        Public Domain
URL:            http://rsbweb.nih.gov/ij/index.html
Source0:        http://rsbweb.nih.gov/ij/download/src/ij152r-src.zip
Source1:        %{name}.desktop
Source2:        http://rsbweb.nih.gov/ij/macros/macros.zip
Source3:        http://rsb.info.nih.gov/ij/download/linux/unix-script.txt
Source4:        imagej.png

# don't copy .class files 
Patch0:         %{name}-%{version}-patch0.patch
# modify imagej.sh for fedora compatibility
Patch1:         %{name}-%{version}-patch1.patch
BuildArch:      noarch

BuildRequires:  ant
BuildRequires:  desktop-file-utils
BuildRequires:	java-rpmbuild

# java-devel not java for plugins build
Requires:       java = 1.8.0

%description
ImageJ is a public domain Java image processing program. It can display,
edit, analyze a wide variety of image data, including image sequences. Imagej
can be used for quantitative analysis of engineering and scientific image data.

%package        javadoc
Summary:        Javadocs for %{name}
Group:          Documentation
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
%ant build javadocs
Summary:        Image Processing and Analysis in Java

Group:          Sciences/Computer science
License:        Public Domain
URL:            http://rsbweb.nih.gov/ij/index.html
Source0:        http://rsbweb.nih.gov/ij/download/src/ij152r-src.zip
Source1:        %{name}.desktop
Source2:        http://rsbweb.nih.gov/ij/macros/macros.zip
Source3:        http://rsb.info.nih.gov/ij/download/linux/unix-script.txt
Source4:        imagej.png

# don't copy .class files 
# Patch0:         %{name}-%{version}-patch0.patch
# modify imagej.sh for fedora compatibility
# Patch1:         %{name}-%{version}-patch1.patch
BuildArch:      noarch

BuildRequires:  ant
BuildRequires:  desktop-file-utils
BuildRequires:	java-rpmbuild

# java-devel not java for plugins build
Requires:       java >= 1.8.0

%description
ImageJ is a public domain Java image processing program. It can display,
edit, analyze a wide variety of image data, including image sequences. Imagej
can be used for quantitative analysis of engineering and scientific image data.

%package        javadoc
Summary:        Javadocs for %{name}
Group:          Documentation
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -c -n "%{name}-%{version}" 
# patch build.xml
# %patch0 -p0 -b .patch0
# unzip macros.zip
unzip -qq -u %{SOURCE2} 
# erase binary and useless files 
rm -rf macros/.FBC*
rm macros/build.xml
rm -rf __MACOSX
#get and patch unix-script.txt
cp %{SOURCE3} ./imagej.sh
# %patch1 -p1 -b .patch1

find -name '*.class' -exec rm -f '{}' \;
find -name '*.jar' -exec rm -f '{}' \;

%build
cd source
%ant build javadocs
cd ..

%install
# install jar
mkdir -p %{buildroot}%{_javadir}
cp -p source/ij.jar   \
%{buildroot}%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar

# install javadoc
mkdir -p %{buildroot}%{_javadocdir}/%{name}
cp -rp api  \
%{buildroot}%{_javadocdir}/%{name}

# install icon
mkdir -p %{buildroot}%{_datadir}/pixmaps
cp -p %{SOURCE4} %{buildroot}%{_datadir}/pixmaps

# install data files
mkdir -p %{buildroot}%{_datadir}/%{name}
cp -p source/build/about.jpg %{buildroot}%{_datadir}/%{name}/about.jpg
cp -p source/build/IJ_Props.txt %{buildroot}%{_datadir}/%{name}/IJ_Props.txt

#install macros
chmod 644 macros/About\ Startup\ Macros 
find ./macros -name \*.txt -type f -exec chmod 644 {} \;
find ./macros -type d -exec chmod 755 {} \;
cp -rp macros %{buildroot}%{_datadir}/%{name}

#install luts
mkdir %{buildroot}%{_datadir}/%{name}/luts 

# install script
mkdir -p %{buildroot}%{_bindir}
chmod +x imagej.sh
cp -p imagej.sh %{buildroot}%{_bindir}/%{name}

# directory for plugins
mkdir -p %{buildroot}%{_datadir}/%{name}/plugins
cp source/plugins/JavaScriptEvaluator.source %{buildroot}%{_datadir}/%{name}/plugins/JavaScriptEvaluator.java

# desktop file
desktop-file-install --vendor=""                     \
       --dir=%{buildroot}%{_datadir}/applications/   \
       %{SOURCE1}

%files
%{_javadir}/*
%{_datadir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%{_bindir}/%{name}
%doc source/aREADME.txt source/release-notes.html source/applet.html

%files javadoc
%{_javadocdir}/%{name}
