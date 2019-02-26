# (oe) undefining these makes the build _real_ quick.
%undefine __find_provides
%undefine __find_requires

Summary:	Joomla Open Source (CMS)
Name:		joomla
Version:	3.9.3
Release:	1
License:	GPLv2+
Group:		System/Servers
URL:		http://www.joomla.org/
Source0:	Joomla_%{version}-Stable-Full_Package.tar.bz2
Source1:	joomla-16x16.png
Source2:	joomla-32x32.png
Source3:	joomla-48x48.png
#Patch0:		joomla-htaccess.patch.bz2
Requires:	apache-mod_php
Requires:	php-mysql
Requires:	php-xml
Requires:	php-gd
Requires:	joomla-administrator
BuildArch:	noarch

%description
Joomla! is a Content Management System (CMS) created by the same award-winning
team that brought the Mambo CMS to its current state of stardom.

%package	administrator
Summary:	Administrative web interface for Joomla Open Source (CMS)
Group:		System/Servers
Requires:	%{name} = %{version}-%{release}

%description	administrator
Administrative web interface for Joomla Open Source (CMS)

%prep

%setup -q -c
#patch0

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
install -d %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d
install -d %{buildroot}%{_sysconfdir}/%{name}
install -d %{buildroot}%{_var}/www/%{name}
cp -aRf * %{buildroot}%{_var}/www/%{name}/

# provide an empty configuration.php file
touch %{buildroot}%{_var}/www/%{name}/configuration.php

# apache config
cat > %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf << EOF

Alias /%{name} %{_var}/www/%{name}

<Directory %{_var}/www/%{name}>
    Require all granted
</Directory>

<Directory %{_var}/www/%{name}/installation>
    Require local
    ErrorDocument 403 "Access denied per %{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf"
</Directory>

EOF

cat htaccess.txt >> %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf

cat > %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d/%{name}-administrator.conf << EOF

<Directory %{_var}/www/%{name}/administrator>
    Require local
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
%{_var}/www/joomla/installation/.
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
rm -f %{buildroot}%{_var}/www/%{name}/htaccess.txt %{buildroot}%{_var}/www/%{name}/joomla-*.png

%files
%doc README.urpmi
%config(noreplace) %{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf
#exclude %{_var}/www/%{name}/administrator
%dir %{_var}/www/%{name}
%{_var}/www/%{name}/includes
%{_var}/www/%{name}/installation
%{_var}/www/%{name}/libraries
%{_var}/www/%{name}/logs
%{_var}/www/%{name}/plugins
%{_var}/www/%{name}/tmp
%{_var}/www/%{name}/xmlrpc
%{_var}/www/%{name}/CHANGELOG.php
%{_var}/www/%{name}/COPYRIGHT.php
%{_var}/www/%{name}/CREDITS.php
%{_var}/www/%{name}/INSTALL.php
%{_var}/www/%{name}/LICENSE.php
%{_var}/www/%{name}/LICENSES.php
%{_var}/www/%{name}/index*.php
%{_var}/www/%{name}/configuration.php-dist
%{_var}/www/%{name}/robots.txt
%defattr(0644,apache,root,0755)
%config(noreplace) %{_var}/www/%{name}/configuration.php
%{_var}/www/%{name}/cache
%{_var}/www/%{name}/components
%{_var}/www/%{name}/images
%{_var}/www/%{name}/language
%{_var}/www/%{name}/media
%{_var}/www/%{name}/modules
%{_var}/www/%{name}/templates

%files administrator
%config(noreplace) %{_sysconfdir}/httpd/conf/webapps.d/%{name}-administrator.conf
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_datadir}/applications/*.desktop
%defattr(0644,apache,root,0755)
%{_var}/www/%{name}/administrator


%changelog
* Tue Jul 27 2010 Jerome Martin <jmartin@mandriva.org> 1.5.20-1mdv2011.0
+ Revision: 561199
- Version 1.5.20

* Wed Apr 28 2010 Jerome Martin <jmartin@mandriva.org> 1.5.17-1mdv2010.1
+ Revision: 540489
- Update to version 1.5.17
 - Add README.urpmi

* Tue Feb 23 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1.5.15-2mdv2010.1
+ Revision: 510408
- rely on filetrigger for reloading apache configuration begining with 2010.1, rpm-helper macros otherwise
- don't duplicate spec-helper job
- restrict access to administrative interface
- web file configuration renaming
- spec cleanup

* Wed Dec 02 2009 Funda Wang <fwang@mandriva.org> 1.5.15-1mdv2010.1
+ Revision: 472652
- new version 1.5.15

* Fri Oct 23 2009 Oden Eriksson <oeriksson@mandriva.com> 1.5.14-3mdv2010.0
+ Revision: 459032
- P1: php-5.3.x fixes

  + Jerome Martin <jmartin@mandriva.org>
    - Fixed bug #40934

* Fri Oct 09 2009 Jerome Martin <jmartin@mandriva.org> 1.5.14-2mdv2010.0
+ Revision: 456339
- rebuild

* Sat Aug 01 2009 Frederik Himpe <fhimpe@mandriva.org> 1.5.14-1mdv2010.0
+ Revision: 406972
- Update to new version 1.5.14

* Thu Jul 23 2009 Frederik Himpe <fhimpe@mandriva.org> 1.5.13-1mdv2010.0
+ Revision: 399040
- Update to new version 1.5.13

* Fri Jun 05 2009 Frederik Himpe <fhimpe@mandriva.org> 1.5.11-1mdv2010.0
+ Revision: 383125
- Update to new version 1.5.11
- Use tar.bz2 source package instead of zip, remove source URL because it
  changes for every new version anyway

* Tue Mar 31 2009 Oden Eriksson <oeriksson@mandriva.com> 1.5.10-1mdv2009.1
+ Revision: 362832
- 1.5.10 (multiple security fixes)

* Sat Jan 10 2009 Funda Wang <fwang@mandriva.org> 1.5.9-1mdv2009.1
+ Revision: 327993
- New verrsion 1.5.9

* Wed Nov 12 2008 Funda Wang <fwang@mandriva.org> 1.5.8-1mdv2009.1
+ Revision: 302415
- New version 1.5.8

* Wed Sep 10 2008 Funda Wang <fwang@mandriva.org> 1.5.7-1mdv2009.0
+ Revision: 283426
- New version 1.5.7

* Wed Aug 13 2008 Funda Wang <fwang@mandriva.org> 1.5.6-1mdv2009.0
+ Revision: 271449
- New version 1.5.6

* Mon Jul 28 2008 Funda Wang <fwang@mandriva.org> 1.5.5-1mdv2009.0
+ Revision: 250795
- New version 1.5.5

* Tue Jul 08 2008 Funda Wang <fwang@mandriva.org> 1.5.4-1mdv2009.0
+ Revision: 232677
- New version 1.5.4

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Wed Apr 30 2008 Funda Wang <fwang@mandriva.org> 1.5.3-1mdv2009.0
+ Revision: 199416
- New version 1.5.3

* Sat Feb 09 2008 Funda Wang <fwang@mandriva.org> 1.5.1-1mdv2008.1
+ Revision: 164459
- New version 1.5.1

* Sat Jan 26 2008 Funda Wang <fwang@mandriva.org> 1.5.0-1mdv2008.1
+ Revision: 158336
- remove missing files
- New version 1.5.0

* Mon Jan 21 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.13-3mdv2008.1
+ Revision: 155803
- second sec fix release (really 1.0.14-RC1)

  + Thierry Vignaud <tv@mandriva.org>
    - drop old menu
    - kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Tue Aug 28 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0.13-2mdv2008.0
+ Revision: 72690
- added a security fix
- nuke wrong xdg stuff

* Sun Aug 19 2007 Colin Guthrie <cguthrie@mandriva.org> 1.0.13-1mdv2008.0
+ Revision: 67006
- New upstream version: 1.0.13


* Mon Jan 01 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0.12-1mdv2007.0
+ Revision: 103005
- 1.0.12
- drop upstream patches; P0

* Mon Dec 11 2006 Oden Eriksson <oeriksson@mandriva.com> 1.0.11-5mdv2007.1
+ Revision: 94787
- make the main package require the administrator subpackage (fixes #27602)

* Mon Oct 30 2006 Oden Eriksson <oeriksson@mandriva.com> 1.0.11-4mdv2007.1
+ Revision: 73682
- also add the patch...
- added P0 to make admin.mambots.php work
- rebuild
- Import joomla

* Fri Sep 08 2006 Oden Eriksson <oeriksson@mandriva.com> 1.0.11-2
- use the www-browser script

* Thu Aug 31 2006 Oden Eriksson <oeriksson@mandriva.com> 1.0.11-1
- 1.0.11 (Major security fixes)
- fix xdg menu

* Tue Jun 13 2006 Oden Eriksson <oeriksson@mandriva.com> 1.0.9-2mdv2007.0
- relocate it to /var/www/joomla and add a apache config file
- add a menu entry, icons, etc...

* Mon Jun 12 2006 Oden Eriksson <oeriksson@mandriva.com> 1.0.9-1mdv2007.0
- 1.0.9:
  o 12 Low Level Security Fixes
  o 160+ General bug fixes
  o Several Performance enhancements

* Fri Mar 10 2006 Oden Eriksson <oeriksson@mandriva.com> 1.0.8-1mdk
- 1.0.8:
  o 37 Security Fixes
  o 70+ General bug fixes
  o Several Performance enhancements

* Mon Feb 06 2006 Oden Eriksson <oeriksson@mandriva.com> 1.0.7-2mdk
- make the installation a little easier... (#21038)

* Tue Jan 03 2006 Oden Eriksson <oeriksson@mandriva.com> 1.0.7-1mdk
- use the Joomla fork instead (#20909)

* Tue Jan 03 2006 Oden Eriksson <oeriksson@mandriva.com> 4.5.3h-1mdk
- 4.5.3h

* Sun Apr 03 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 4.5.2.1-1mdk
- added P0 (security fix) and bump version

* Sun Apr 03 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 4.5.2-1mdk
- 4.5.2
- strip away annoying ^M

* Fri Oct 29 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.5.1a-1mdk
- 4.5.1a

* Thu Jun 24 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.5-2mdk
- added the 1.0.7-1.0.8 diff

* Tue May 11 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.5-1mdk
- initial package

