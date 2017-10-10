Name:           ros-kinetic-catkin
Version:        0.7.7
Release:        0
Summary:        ROS catkin package
Group:          Development/Libraries
License:        BSD
URL:            http://www.ros.org/wiki/catkin
Source0:        %{name}-%{version}.tar.gz
Source1001:     %{name}.manifest

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
%define         ros_root /opt/ros
%define         install_path %{ros_root}/%{ros_distro}
%define         src_name catkin

%description
Low-level build system macros and infrastructure for ROS.

%prep
%setup -q
cp %{SOURCE1001} .

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/usr/setup.sh" ]; then . "/usr/setup.sh"; fi
mkdir build && cd build
cmake .. \
        -DCMAKE_INSTALL_PREFIX="%{install_path}" \
        -DCMAKE_PREFIX_PATH="%{install_path}" \
        -DSETUPTOOLS_DEB_LAYOUT=OFF \
#        -DCATKIN_BUILD_BINARY_PACKAGE="1" \

make %{?_smp_mflags}

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/usr/setup.sh" ]; then . "/usr/setup.sh"; fi
pushd build
make install DESTDIR=%{buildroot}
popd

%files -f build/install_manifest.txt
%manifest %{name}.manifest
%defattr(-,root,root)
%{install_path}/.catkin
%{install_path}/.rosinstall
%{install_path}/bin/*
%{install_path}/lib/python2.7/site-packages/*

%changelog 
