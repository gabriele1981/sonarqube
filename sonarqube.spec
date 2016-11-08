# Project installation directory WITH trailing slash.
%define _project_dir /opt/sonarqube
%define _property_dir /opt/sonarqube/conf

# Figure out server database password
#%define _db_pass $(cat /root/passappl.sql)
#%define _property_db_password Ds00@c9i

Name:      sonarqube
Version:   %{version}
Release:   %{release}
Summary:   SonarQube

Group:     Applicatie/File
License:   NA
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-root

# Enable/Disable Automatic Dependency Processing
AutoReqProv: 0

%description
SonarQube 5.3 
# based on rh-mysql56 and java-1.8.0-openjdk.x86_64.

%prep

%build

%install
# Clean the buildroot.
rm -rf %{buildroot}

# Place files there.
install -d -m0755 %{buildroot}%{_project_dir}

# Now copy files to target machine and target dir.
cp -rp ../SOURCES/* %{buildroot}%{_project_dir}

%files
%attr(777, root, root) %{_project_dir}/*

%pre

%post
# Only execute this part on the very first install of the RPM.
#if [ $1 -eq 1 ]; then

# replace password
#sed -i -e s/%{_property_db_password}/%{_db_pass}/g %{_property_dir}/sonar.properties

# Setup sonar script as a service in systemd
mv %{_project_dir}/sonar.service /etc/systemd/system/sonar.service
chmod 644 /etc/systemd/system/sonar.service

# Symlink sonar log files into /var/log/sonar directory
mkdir /var/log/sonar
ln -s /opt/sonarqube-6.0/logs/* /var/log/sonar/

# Start sonar
systemctl start sonar.service
fi

# Start sonar
systemctl restart sonar.service

# Start mysql
systemctl restart mariadb

%changelog

%preun
# If the last version of this package is removed, remove all files and site settings.
if [ $1 == 0 ] ; then
    rm -rf %{_project_dir}
fi

$postun

exit 0
