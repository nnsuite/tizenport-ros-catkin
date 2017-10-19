Name:           ros-kinetic-catkin
Version:        0.7.7
Release:        0
Summary:        ROS catkin package
Group:          Development/Libraries
License:        BSD
URL:            http://www.ros.org/wiki/catkin
Source0:        %{name}-%{version}.tar.gz
Source1001:     %{name}.manifest
Source1002:     macros

Requires:       cmake
Requires:       python-argparse
Requires:       python-catkin_pkg >= 0.1.21
Requires:       python-empy
Requires:       python-nose
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  gtest-devel
BuildRequires:  python-argparse
BuildRequires:  python-catkin_pkg
BuildRequires:  python-empy
BuildRequires:  python-nose

%define         ros_distro kinetic
%define         ros_root /usr/lib/ros
%define         install_path %{ros_root}/%{ros_distro}
%define         rpmhome %{_prefix}/lib/rpm

%description
Low-level build system macros and infrastructure for ROS.

%prep
%setup -q
cp %{SOURCE1001} .

%build
mkdir build && cd build
cmake .. \
        -DCMAKE_INSTALL_PREFIX="%{install_path}" \
        -DCMAKE_PREFIX_PATH="%{install_path}" \
        -DSETUPTOOLS_DEB_LAYOUT=OFF \

make %{?_smp_mflags}

%install
pushd build
make install DESTDIR=%{buildroot}
popd

mkdir -p %{buildroot}%{rpmhome}/macros.d
install -m 644 %{SOURCE1002} %{buildroot}%{rpmhome}/macros.d/macros.catkin

%post
# For catkin build for other ROS package, environment setup script is provided on version-independent path.
ln -sf %{install_path}/setup.sh /usr/setup.sh

%postun
if [ $1 = 0 ] ; then
  rm -f /usr/setup.sh
fi

%files -f build/install_manifest.txt
%manifest %{name}.manifest
%defattr(-,root,root)
%{install_path}/.catkin
%{install_path}/.rosinstall
%{install_path}/bin/*
%{install_path}/lib/python2.7/site-packages/*
%{rpmhome}/macros.d/macros.catkin

%changelog 
