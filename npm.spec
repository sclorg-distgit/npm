%{?scl:%scl_package npm}
%{!?scl:%global pkg_name %{name}}

%{?nodejs_find_provides_and_requires}

Name:       %{?scl_prefix}npm
Version:    2.14.13
Release:    6%{?dist}
Summary:    Node.js Package Manager
License:    Artistic 2.0
Group:      Development/Tools
URL:        http://npmjs.org/
#stripped sources are created by script,
#we remove badly licensed web fonts from documentation
#http://registry.npmjs.org/%%{npm_name}/-/%%{npm_name}-%%{version}.tgz
Source0:    npm-2.14.13-stripped.tar.gz
BuildRoot:  %{_tmppath}/%{pkg_name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch
ExclusiveArch: %{nodejs_arches} noarch
BuildRequires: %{?scl_prefix}nodejs-devel
%{?scl:Requires: %{scl}-runtime}


%{?scl:Obsoletes: %{scl}-nodejs-npmconf}

%description
npm is a package manager for node.js. You can use it to install and publish your
node programs. It manages dependencies and does other cool stuff.

%prep
%setup -q -n package

%nodejs_fixdep request '>2.16 <3'
%nodejs_fixdep columnify 1.3.2
%nodejs_fixdep lockfile '>= 1.0.0'
%nodejs_fixdep readable-stream '>= 2.0.2'
%nodejs_fixdep once '>= 1.3.0'
%nodejs_fixdep github-url-from-username-repo '>= 1.0.0'
%nodejs_fixdep abbrev '>= 1.0.5'
%nodejs_fixdep write-file-atomic '>= 1.1.2'
%nodejs_fixdep fstream-npm '>= 1.0.1'
%nodejs_fixdep block-stream '>= 0.0.7'
%nodejs_fixdep readable-stream '>= 2.0.2'
%nodejs_fixdep uid-number '>= 0.0.5'
%nodejs_fixdep retry '>= 0.6.0'
%nodejs_fixdep cmd-shim '>= 2.0.0'
%nodejs_fixdep read '>= 1.0.5'
%nodejs_fixdep fs-write-stream-atomic '>= 1.0.3'
%nodejs_fixdep inherits '>= 2.0.0'
%nodejs_fixdep npm-user-validate '>= 0.1.1'
%nodejs_fixdep dezalgo '>= 1.0.2'
%nodejs_fixdep ini '>= 1.2.0'
%nodejs_fixdep mkdirp '>= 0.5.0'
%nodejs_fixdep fstream '>= 1.0.3'
%nodejs_fixdep fs-vacuum '>= 1.2.6'

#remove bundled modules
rm -rf node_modules

#add a missing shebang
sed -i -e '1i#!/usr/bin/env node' bin/read-package-json.js

# delete windows stuff
rm bin/npm.cmd bin/node-gyp-bin/node-gyp.cmd

%build
#nothing to do

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{nodejs_sitelib}/npm
cp -pr bin lib cli.js package.json %{buildroot}%{nodejs_sitelib}/npm/

mkdir -p %{buildroot}%{_bindir}
ln -sf ../lib/node_modules/npm/bin/npm-cli.js %{buildroot}%{_bindir}/npm

# ghosted global config files
mkdir -p %{buildroot}%{_sysconfdir}
touch %{buildroot}%{_sysconfdir}/npmrc
touch %{buildroot}%{_sysconfdir}/npmignore

# install to mandir
mkdir -p %{buildroot}%{_mandir}
cp -pr man/* %{buildroot}%{_mandir}/

ln -sf %{_defaultdocdir}/%{name}-%{version}/doc %{buildroot}%{nodejs_sitelib}/npm/doc
ln -sf %{_defaultdocdir}/%{name}-%{version}/html %{buildroot}%{nodejs_sitelib}/npm/html
ln -sf %{_defaultdocdir}/%{name}-%{version}/man %{buildroot}%{nodejs_sitelib}/npm/man

%nodejs_symlink_deps

# probably needs network, need to investigate further
#%%check
#%%__nodejs test/run.js
#%%tap test/tap/*.js

%pretrans -p <lua>
require 'posix'
require 'os'
if (posix.stat("%{nodejs_sitelib}/npm/man", "type") == "directory") and (posix.stat("%{nodejs_sitelib}/npm/man", "type") ~= "link") then
  posix.rmdir("%{nodejs_sitelib}/npm/man")
end

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{nodejs_sitelib}/npm
%ghost %{_sysconfdir}/npmrc
%ghost %{_sysconfdir}/npmignore
%{_bindir}/npm
%{_mandir}/man*/*
%doc AUTHORS man doc html README.md LICENSE

%changelog
* Mon Nov 30 2015 Tomas Hrcka <thrcka@redhat.com> - 2.14.13-6
- Rebase to new upstream version
- https://github.com/npm/npm/releases/tag/v2.14.13

* Wed Sep 16 2015 Tomas Hrcka <thrcka@redhat.com> - 1.4.28-5
- Resolves RHBZ#1082002

* Thu Jul 23 2015 Tomas Hrcka <thrcka@redhat.com> - 1.4.28-4
- Remove macros for fixing deps

* Tue Jan 13 2015 Tomas Hrcka <thrcka@redhat.com> - 1.4.28-3
- Replace != with ~= in lua scriptlet

* Tue Jan 13 2015 Tomas Hrcka <thrcka@redhat.com> - 1.4.28-2
- Fix path to lua interpreter

* Mon Jan 12 2015 Tomas Hrcka <thrcka@redhat.com> - 1.4.28-1
- New upstream release 1.4.28
- Pretrans scriptlet changed to lua RHBZ#1149196 
- Remove fix_dep on semver package since we have update

* Fri May 02 2014 Tomas Hrcka <thrcka@redhat.com> - 1.3.24-5
- Add %pretrans scriptlet RHBZ #1092162

* Mon Mar 31 2014 Tomas Hrcka <thrcka@redhat.com> - 1.3.24-4
- Removed patch for help pages
- Added link to manpages in man dir of npm
- Fix link to doc dir

* Thu Mar 27 2014 Tomas Hrcka <thrcka@redhat.com> - 1.3.24-3
- Add patch to fix help pages path when npm help is used without man

* Wed Mar 26 2014 Tomas Hrcka <thrcka@redhat.com> - 1.3.24-2
- Remove patches for system path to man pages, fixed upstream

* Mon Feb 03 2014 Tomas Hrcka <thrcka@redhat.com> - 1.3.24-1
- New upstream release 1.3.24

* Wed Jan 08 2014 Tomas Hrcka <thrcka@redhat.com> - 1.3.6-4.2
- invoke fix_dep macro for cmd-shim with version 1.1 and above

* Mon Oct 14 2013 Tomas Hrcka <thrcka@redhat.com> - 1.3.6-4.1
 - new upstream release
 - remove patches that are already in upstream release

* Thu Aug 08 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.3.6-4
 - remove unnecessary symlink to mandir
  fixes upgrade path from certain older versions of npm

* Tue Jul 30 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.3.6-2
 - license changed from MITNFA to Artistic 2.0

* Tue Jul 30 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.3.6-1
 - new upstream release 1.3.6

* Mon Jul 22 2013 Tomas Hrcka thrcka@redhat.com - 1.2.17-9
 - RHBZ #983930 CVE-2013-4116 Insecure temporary directory generation

* Mon Jul 22 2013 Tomas Hrcka  <thrcka@redhat.com> - 1.2.17-8
 - patch for font deletion was replaced by script that strip webfons from tarball

* Thu Jul 18 2013 Tomas Hrcka  <thrcka@redhat.com> - 1.2.17-7
 - Removed badly licensed fonts from html documentation

* Fri Jul 12 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.3.3-1
- new upstream release 1.3.3
- fixes insecure temporary directory generation (CVE-2013-4116; RHBZ#983917)

* Tue Jul 02 2013 Tomas Hrcka  <thrcka@redhat.com> - 1.2.17-6
 - replaced manpath to use system paths
 - replaced previous patch to fix gz extension
* Sun Jun 23 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.3.0-1
- new upstream release 1.3.0
- use system paths for manual pages and documentation (RHBZ#953051)

* Sat Jun 22 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.2.17-6
- restrict to compatible arches

* Sun Jun 02 2013 Tomas Hrcka <thrcka@redhat.com> - 1.2.17-5.2
 - patch that add .gz extension when help.j calls 'man' fix RHBZ#965439
 
* Tue May 07 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.2.17-5.1
 - Add runtime dependency on scl-runtime

* Wed Apr 17 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.2.17-5
- Fix manpage names so that npm help finds them

* Mon Apr 15 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.2.17-4.1
- Fix documentation symlink
- Use new requires/provides macro

* Mon Apr 15 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.2.17-4
- add EPEL dependency generation macro

* Mon Apr 15 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.2.17-3
- rebuilt

* Mon Apr 15 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.2.17-2
- revert a change that adds a dep (that only affects Windows anyway)
- fix bogus date in changelog warning

* Fri Apr 12 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.2.17-2
- Add support for software collections

* Wed Apr 03 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.2.17-1
- new upstream release 1.2.17

* Wed Mar 13 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.2.14-2
- fix dependencies

* Mon Mar 11 2013 Stephen Gallagher <sgallagh@redhat.com> - 1.2.14-1
- New upstream release 1.2.14
- Bring npm up to the latest to match the Node.js 0.10.0 release

* Wed Feb 13 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.2.10-2
- fix dep for updated read-package-json

* Sat Feb 09 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.2.10-1
- new upstream release 1.2.10

* Sat Jan 19 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.2.1-2
- fix rpmlint warnings

* Fri Jan 18 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.2.1-1
- new upstream release 1.2.1
- fix License tag

* Thu Jan 10 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.2.0-1
- new upstream release 1.2.0

* Tue Jan 08 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.70-2
- add missing build section

* Mon Dec 31 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.70-1
- new upstream release 1.1.70

* Wed May 02 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.19-1
- New upstream release 1.1.19

* Wed Apr 18 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.18-1
- New upstream release 1.1.18

* Fri Apr 06 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.16-1
- New upstream release 1.1.16

* Mon Apr 02 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.15-1
- New upstream release 1.1.15

* Thu Mar 29 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.14-1
- New upstream release 1.1.14

* Wed Mar 28 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.13-2
- new dependencies fstream-npm, uid-number, and fstream-ignore (indirectly)

* Wed Mar 28 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.13-1
- new upstream release 1.1.13

* Thu Mar 22 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.12-1
- new upstream release 1.1.12

* Thu Mar 15 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.9-1
- new upstream release 1.1.9

* Sun Mar 04 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.4-1
- new upstream release 1.1.4

* Sat Feb 25 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.2-1
- new upstream release 1.1.2

* Sat Feb 11 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.1-2
- fix node_modules symlink

* Thu Feb 09 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.1-1
- new upstream release 1.1.1

* Sun Jan 29 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.0-2.3
- new upstream release 1.1.0-3

* Sat Jan 21 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.0-2.2
- missing Group field for EL5

* Sat Jan 21 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.0-1.2
- new upstream release 1.1.0-2

* Thu Nov 17 2011 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.106-1
- new upstream release 1.0.106
- ship manpages again

* Thu Nov 10 2011 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.105-1
- new upstream release 1.0.105
- use relative symlinks instead of absolute
- fixes /usr/bin/npm symlink on i686

* Mon Nov 07 2011 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.104-1
- new upstream release 1.0.104
- adds node 0.6 support

* Wed Oct 26 2011 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.101-2
- missing Requires on nodejs-request
- Require compilers too so native modules build properly

* Tue Oct 25 2011 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.101-1
- new upstream release
- use symlink /usr/lib/node_modules -> /usr/lib/nodejs instead of patching

* Thu Aug 25 2011 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.26-2
- rebuilt with fixed nodejs_fixshebang macro from nodejs-devel-0.4.11-3

* Tue Aug 23 2011 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.26-1
- initial package
