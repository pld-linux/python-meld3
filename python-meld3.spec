#
# Conditional build:
%bcond_without	tests	# do not perform "make test"

%define 	module	meld3
Summary:	HTML/XML templating system for Python
Name:		python-%{module}
Version:	0.6.10
Release:	1
License:	ZPL v2.1
Group:		Development/Languages
URL:		http://www.plope.com/software/meld3/
Source0:	http://pypi.python.org/packages/source/m/meld3/meld3-%{version}.tar.gz
# Source0-md5:	42e58624e9d427be7659d7a28e2b0b6f
# The current meld3 tarball leaves this out by mistake
# https://github.com/Supervisor/meld3/raw/0.6.7/meld3/cmeld3.c -- AKA:
# https://github.com/Supervisor/meld3/raw/bafd959fc2e389f46786a6b3174d50f9963fe967/meld3/cmeld3.c
BuildRequires:	python-devel
BuildRequires:	python-elementtree
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
Requires:	python-elementtree
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
meld3 is an HTML/XML templating system for Python 2.3+ which keeps
template markup and dynamic rendering logic separate from one another.
See <http://www.entrian.com/PyMeld> for a treatise on the benefits of
this pattern.

%prep
%setup -q -n meld3-%{version}

%build
export USE_MELD3_EXTENSION_MODULES=True
CC="%{__cc}" \
CFLAGS="%{rpmcflags}" \
%{__python} setup.py build

%if %{with tests}
%{__python} meld3/test_meld3.py
%endif

%install
rm -rf $RPM_BUILD_ROOT
export USE_MELD3_EXTENSION_MODULES=True
%{__python} setup.py install \
	--skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean

%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/meld3/test_*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.txt COPYRIGHT.txt LICENSE.txt CHANGES.txt
%dir %{py_sitedir}/%{module}
%{py_sitedir}/%{module}/*.py[co]
%attr(755,root,root) %{py_sitedir}/meld3/cmeld3.so
%{py_sitedir}/%{module}-%{version}*.egg-info
