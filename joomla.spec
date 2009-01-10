# (oe) undefining these makes the build _real_ quick.
%undefine __find_provides
%undefine __find_requires

Summary:	Joomla Open Source (CMS)
Name:		joomla
Version:	1.5.9
Release:	%mkrel 1
License:	GPLv2+
Group:		System/Servers
URL:		http://www.joomla.org/
Source0:	http://downloads.joomlacode.org/frsrelease/3/0/9/30991/Joomla_%version-Stable-Full_Package.tar.bz2
Source1:	joomla-16x16.png
Source2:	joomla-32x32.png
Source3:	joomla-48x48.png
BuildRequires:	apache-base >= 2.0.54
BuildRequires:	file
Requires(pre):	apache-mod_php php-mysql php-gd php-xml
Requires:	apache-mod_php php-mysql php-gd php-xml
Requires:	joomla-administrator
BuildArch:	noarch
Provides:	mambo
Obsoletes:	mambo
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Joomla! is a Content Management System (CMS) created by the same award-winning
team that brought the Mambo CMS to its current state of stardom.

%package	administrator
Summary:	Administrative web interface for Joomla Open Source (CMS)
Group:		System/Servers
Requires(pre):	%{name} = %{version}-%{release}
Requires:	%{name} = %{version}-%{release}

%description	administrator
Administrative web interface for Joomla Open Source (CMS)

%prep

%setup -q -c -n %{name}-%{version}

# clean up CVS stuff
for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -r $i; fi >&/dev/null
done

# fix dir perms
find . -type d | xargs chmod 755

# fix file perms
find . -type f | xargs chmod 644

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

cp %{SOURCE1} .
cp %{SOURCE2} .
cp %{SOURCE3} .

%build

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d
install -d %{buildroot}%{_sysconfdir}/%{name}
install -d %{buildroot}/var/www/%{name}
cp -aRf * %{buildroot}/var/www/%{name}/

# provide an empty configuration.php file
touch %{buildroot}/var/www/%{name}/configuration.php

# apache config
cat > %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d/01_%{name}.conf << EOF

Alias /%{name} /var/www/%{name}

<Directory /var/www/%{name}>
    Allow from All
</Directory>

<Directory /var/www/%{name}/installation>
    Order Deny,Allow
    Deny from All
    Allow from 127.0.0.1
    ErrorDocument 403 "Access denied per %{_sysconfdir}/httpd/conf/webapps.d/01_%{name}.conf"
</Directory>

EOF

cat htaccess.txt >> %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d/01_%{name}.conf

cat > %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d/02_%{name}-administrator.conf << EOF

<Directory /var/www/%{name}/administrator>
    Allow from All
</Directory>

#<LocationMatch /%{name}/administrator>
#    Options FollowSymLinks
#    RewriteEngine on
#    RewriteCond %{SERVER_PORT} !^443$
#    RewriteRule ^.*$ https://%{SERVER_NAME}%{REQUEST_URI} [L,R]
#</LocationMatch>

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
%_post_webapp

%postun
%_postun_webapp

%post administrator
%_post_webapp
%if %mdkversion < 200900
%update_menus
%endif

%postun administrator
%_postun_webapp
%if %mdkversion < 200900
%clean_menus
%endif

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/conf/webapps.d/01_%{name}.conf
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
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/conf/webapps.d/02_%{name}-administrator.conf
/var/www/%{name}/administrator
%dir %attr(0755,apache,root) /var/www/%{name}/administrator/backups
%dir %attr(0755,apache,root) /var/www/%{name}/administrator/components
%dir %attr(0755,apache,root) /var/www/%{name}/administrator/modules
%dir %attr(0755,apache,root) /var/www/%{name}/administrator/templates
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_datadir}/applications/*.desktop
