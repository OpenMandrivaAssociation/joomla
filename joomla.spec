# (oe) undefining these makes the build _real_ quick.
%undefine __find_provides
%undefine __find_requires

Summary:	Joomla Open Source (CMS)
Name:		joomla
Version:	2.5.3
Release:	%mkrel 1
License:	GPLv2+
Group:		System/Servers
URL:		http://www.joomla.org/
Source0:	Joomla_%{version}-Stable-Full_Package.tar.gz
Source1:	joomla-16x16.png
Source2:	joomla-32x32.png
Source3:	joomla-48x48.png
Patch0:		joomla-htaccess.patch.bz2
Requires:	apache-mod_php
Requires:	php-mysql
Requires:	php-xml
Requires:	php-gd
%if %mdkversion < 201010
Requires(post):   rpm-helper
Requires(postun):   rpm-helper
%endif
Requires:	joomla-administrator
BuildArch:	noarch
Provides:	mambo
Obsoletes:	mambo
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
Joomla! is a Content Management System (CMS) created by the same award-winning
team that brought the Mambo CMS to its current state of stardom.

%package	administrator
Summary:	Administrative web interface for Joomla Open Source (CMS)
Group:		System/Servers
Requires:	%{name} = %{version}-%{release}
%if %mdkversion < 201010
Requires(post):   rpm-helper
Requires(postun):   rpm-helper
%endif

%description	administrator
Administrative web interface for Joomla Open Source (CMS)

%prep

%setup -q -c -n %{name}-%{version}
#%patch0

# clean up CVS stuff
for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -r $i; fi >&/dev/null
done

# fix dir perms
find . -type d | xargs chmod 755

# fix file perms
find . -type f | xargs chmod 644

cp %{SOURCE1} .
cp %{SOURCE2} .
cp %{SOURCE3} .

%build

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d
install -d %{buildroot}%{_sysconfdir}/%{name}
install -d %{buildroot}/var/www/%{name}
cp -aRf * %{buildroot}/var/www/%{name}/

# provide an empty configuration.php file
touch %{buildroot}/var/www/%{name}/configuration.php

# apache config
cat > %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf << EOF

Alias /%{name} /var/www/%{name}

<Directory /var/www/%{name}>
    Allow from all
</Directory>

<Directory /var/www/%{name}/installation>
    Order deny,allow
    Deny from all
    Allow from 127.0.0.1
    ErrorDocument 403 "Access denied per %{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf"
</Directory>

EOF

cat htaccess.txt >> %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf

cat > %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d/%{name}-administrator.conf << EOF

<Directory /var/www/%{name}/administrator>
    Order deny,allow
    Deny from all
    Allow from 127.0.0.1
    ErrorDocument 403 "Access denied per %{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf"
</Directory>
EOF

cat > README.urpmi <<EOF
Once this package is installed, there are a few configuration items which need
to be performed before the application is usable.  First, you need to install
Mysql database and corresponding php modules:

# urpmi mysql php-mysql

Then, you need to establish a username and password to connect to your
MySQL database as, and make both MySQL and Joomla aware of this.
Let's start by creating the database and the username / password
inside MySQL first:

  # mysql
  mysql> create database joomla;
  Query OK, 1 row affected (0.00 sec)

  mysql> grant all privileges on joomla.* to joomla identified by 'joomla';
  Query OK, 0 rows affected (0.00 sec)

  mysql> flush privileges;
  Query OK, 0 rows affected (0.00 sec)

  mysql> exit
  Bye
  #

Under certain curcumstances, you may need to run variations of the "grant"
command:
mysql> grant all privileges on joomla.* to joomla@localhost identified by 'joomla';
   OR
mysql> grant all privileges on joomla.* to joomla@'%' identified by 'joomla';

This has created an empty database called 'joomla', created a user named
'joomla' with a password of 'joomla', and given the 'joomla' user total
permission over the 'joomla' database.  Obviously, you'll want to select a
different password, and you may want to choose different database and user
names depending on your installation.  The specific values you choose are
not constrained, they simply need to be consistent between the database and the
config file.

Once that's done and the database server and web server have been started, 
 in your favourite web browser, enter following URL :
http://localhost/joomla/  and 
follow the instructions given to you on the pages you see to set up the 
database tables. Then, when required, removed the directory 
/var/www/joomla/installation/.
EOF

# Mandriva Icons
install -d %{buildroot}%{_iconsdir}
install -d %{buildroot}%{_miconsdir}
install -d %{buildroot}%{_liconsdir}

install -m0644 joomla-16x16.png %{buildroot}%{_miconsdir}/%{name}.png
install -m0644 joomla-32x32.png %{buildroot}%{_iconsdir}/%{name}.png
install -m0644 joomla-48x48.png %{buildroot}%{_liconsdir}/%{name}.png

# install menu entry.

# XDG menu
install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Joomla Administrator
Comment=Administrative web interface for Joomla Open Source (CMS)
Exec=%{_bindir}/www-browser http://localhost/%{name}/administrator/
Icon=%{name}
Terminal=false
Type=Application
Categories=X-MandrivaLinux-Internet-WebEditors;Network;WebDevelopment;
EOF

# cleanup
rm -f %{buildroot}/var/www/%{name}/htaccess.txt %{buildroot}/var/www/%{name}/joomla-*.png

%post
%if %mdkversion < 201010
%_post_webapp
%endif

%postun
%if %mdkversion < 201010
%_postun_webapp
%endif

%post administrator
%if %mdkversion < 201010
%_post_webapp
%endif
%if %mdkversion < 200900
%update_menus
%endif

%postun administrator
%if %mdkversion < 201010
%_postun_webapp
%endif
%if %mdkversion < 200900
%clean_menus
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README.urpmi
%config(noreplace) %{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf
%exclude /var/www/%{name}/administrator
/var/www/%{name}
%config(noreplace) %attr(0644,apache,root) /var/www/%{name}/configuration.php
%dir %attr(0755,apache,root) /var/www/%{name}/cache
%dir %attr(0755,apache,root) /var/www/%{name}/components
%dir %attr(0755,apache,root) /var/www/%{name}/images
%dir %attr(0755,apache,root) /var/www/%{name}/images/banners
%dir %attr(0755,apache,root) /var/www/%{name}/images/stories
%dir %attr(0755,apache,root) /var/www/%{name}/language
%dir %attr(0755,apache,root) /var/www/%{name}/media
%dir %attr(0755,apache,root) /var/www/%{name}/modules
%dir %attr(0755,apache,root) /var/www/%{name}/templates

%files administrator
%defattr(-, root, root)
%config(noreplace) %{_sysconfdir}/httpd/conf/webapps.d/%{name}-administrator.conf
/var/www/%{name}/administrator
%dir %attr(0755,apache,root) /var/www/%{name}/administrator/backups
%dir %attr(0755,apache,root) /var/www/%{name}/administrator/components
%dir %attr(0755,apache,root) /var/www/%{name}/administrator/modules
%dir %attr(0755,apache,root) /var/www/%{name}/administrator/templates
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_datadir}/applications/*.desktop
