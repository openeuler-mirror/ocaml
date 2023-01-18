Name:           ocaml
Version:        4.13.1
Release:        5
Summary:        OCaml compiler and programming environment
License:        LGPL-2.1-only
URL:            http://www.ocaml.org
Source0:        https://github.com/ocaml/ocaml/archive/%{version}.tar.gz

Patch0001:      0001-Don-t-add-rpaths-to-libraries.patch	
Patch0002:      0002-configure-Allow-user-defined-C-compiler-flags.patch	
Patch0003:      0003-configure-Remove-incorrect-assumption-about-cross-co.patch
Patch0004:      0004-Update-dependencies.patch
Patch0005:      0005-Bug-fix-equal_private-was-being-used-in-too-many-pla.patch

BuildRequires:  gcc binutils-devel ncurses-devel gdbm-devel  gawk perl-interpreter 
BuildRequires:  util-linux chrpath autoconf annobin make

Requires:       gcc util-linux   %{_vendor}-rpm-config

Provides:       bundled(md5-plumb) ocaml(runtime) = %{version}
Provides:       ocaml(compiler) = %{version}
Provides:       %{name}-runtime
Obsoletes:      %{name}-runtime
Provides:       %{name}-ocamldoc
Obsoletes:      %{name}-ocamldoc

%global __ocaml_requires_opts -c -f '%{buildroot}%{_bindir}/ocamlrun %{buildroot}%{_bindir}/ocamlobjinfo.byte'
%global __ocaml_provides_opts -f '%{buildroot}%{_bindir}/ocamlrun %{buildroot}%{_bindir}/ocamlobjinfo.byte'

%description
OCaml is a high-level, strongly-typed, functional and object-oriented
programming language from the ML family of languages. This package
includes runtime environment, X11 support ,Documentation generator
and emacs.


%package devel
Summary:    Development files for %{name}
Requires:   ocaml = %{version}-%{release}

Provides:   %{name}-source
Provides:   %{name}-compiler-libs
Obsoletes:  %{name}-source
Obsoletes:  %{name}-compiler-libs

%description devel
Development file for %{name}, includes source code for OCaml libraries
and compiler-libs for development of some OCaml applications.


%package  help
Summary:  Help files for %{name}
Requires: ocaml = %{version}-%{release}


Provides:  %{name}-docs
Obsoletes: %{name}-docs

%description help
Help files for %{name}

%prep
%autosetup -n %{name}-%{version} -p1
autoconf --force

%build

%configure \
    OC_CFLAGS="$CFLAGS" \
    OC_LDFLAGS="$LDFLAGS" \
    --libdir=%{_libdir}/ocaml \
    --host=`./build-aux/config.guess`
%make_build world
%make_build opt
%make_build opt.opt

%check
cd testsuite
make -j1 all ||:

%install
make install DESTDIR=$RPM_BUILD_ROOT
perl -pi -e "s|^%{buildroot}||" %{buildroot}%{_libdir}/ocaml/ld.conf

echo %{version} > %{buildroot}%{_libdir}/ocaml/%{_vendor}-ocaml-release

chrpath --delete %{buildroot}%{_libdir}/ocaml/stublibs/*.so


find %{buildroot} -name .ignore -delete
find %{buildroot} \( -name '*.cmt' -o -name '*.cmti' \) -a -delete

rm -f $RPM_BUILD_ROOT%{_libdir}/ocaml/eventlog_metadata

%files
%license LICENSE
%{_bindir}/ocaml
%{_bindir}/ocamlcmt
%{_bindir}/ocamldebug
%{_bindir}/ocamlyacc

# symlink to either .byte or .opt version
%{_bindir}/ocamlc
%{_bindir}/ocamlcp
%{_bindir}/ocamldep
%{_bindir}/ocamllex
%{_bindir}/ocamlmklib
%{_bindir}/ocamlmktop
%{_bindir}/ocamlobjinfo
%{_bindir}/ocamloptp
%{_bindir}/ocamlprof

# bytecode versions
%{_bindir}/ocamlc.byte
%{_bindir}/ocamlcp.byte
%{_bindir}/ocamldep.byte
%{_bindir}/ocamllex.byte
%{_bindir}/ocamlmklib.byte
%{_bindir}/ocamlmktop.byte
%{_bindir}/ocamlobjinfo.byte
%{_bindir}/ocamloptp.byte
%{_bindir}/ocamlprof.byte

# native code versions
%{_bindir}/ocamlc.opt
%{_bindir}/ocamlcp.opt
%{_bindir}/ocamldep.opt
%{_bindir}/ocamllex.opt
%{_bindir}/ocamlmklib.opt
%{_bindir}/ocamlmktop.opt
%{_bindir}/ocamlobjinfo.opt
%{_bindir}/ocamloptp.opt
%{_bindir}/ocamlprof.opt

%{_bindir}/ocamlopt
%{_bindir}/ocamlopt.byte
%{_bindir}/ocamlopt.opt

%{_libdir}/ocaml/camlheader
%{_libdir}/ocaml/camlheader_ur
%{_libdir}/ocaml/expunge
%{_libdir}/ocaml/extract_crc
%{_libdir}/ocaml/ld.conf
%{_libdir}/ocaml/Makefile.config
%{_libdir}/ocaml/*.a
%{_libdir}/ocaml/*.cmxs
%{_libdir}/ocaml/*.cmxa
%{_libdir}/ocaml/*.cmx
%{_libdir}/ocaml/*.o
%{_libdir}/ocaml/libasmrun_shared.so
%{_libdir}/ocaml/*.mli
%{_libdir}/ocaml/libcamlrun_shared.so
%{_libdir}/ocaml/threads/*.mli
%{_libdir}/ocaml/threads/*.a
%{_libdir}/ocaml/threads/*.cmxa
%{_libdir}/ocaml/threads/*.cmx
%{_libdir}/ocaml/caml

#runtime
%doc README.adoc Changes
%{_bindir}/ocamlrun
%{_bindir}/ocamlrund
%{_bindir}/ocamlruni
%dir %{_libdir}/ocaml
%{_libdir}/ocaml/*.cmo
%{_libdir}/ocaml/*.cmi
%{_libdir}/ocaml/*.cma
%{_libdir}/ocaml/stublibs
%{_libdir}/ocaml/camlheaderi
%{_libdir}/ocaml/camlheaderd
%dir %{_libdir}/ocaml/threads
%{_libdir}/ocaml/threads/*.cmi
%{_libdir}/ocaml/threads/*.cma
%{_libdir}/ocaml/%{_vendor}-ocaml-release


#ocamldoc
%doc ocamldoc/Changes.txt
%{_bindir}/ocamldoc*
%{_libdir}/ocaml/ocamldoc

%files devel
# source
%license LICENSE
%{_libdir}/ocaml/*.ml

# compiler-libs
%dir %{_libdir}/ocaml/compiler-libs
%{_libdir}/ocaml/compiler-libs/*.mli
%{_libdir}/ocaml/compiler-libs/*.cmi
%{_libdir}/ocaml/compiler-libs/*.cmo
%{_libdir}/ocaml/compiler-libs/*.cma
%{_libdir}/ocaml/compiler-libs/*.a
%{_libdir}/ocaml/compiler-libs/*.cmxa
%{_libdir}/ocaml/compiler-libs/*.cmx
%{_libdir}/ocaml/compiler-libs/*.o


%files help
%{_mandir}/man1/*
%{_mandir}/man3/*

%changelog
* Tue Jan 18 2023 xingxing<xingxing@xfusion.com> - 4.13.1-5
- Bug fix equal private was being used in too many pla

* Mon Jan 09 2023 xingxing<xingxing@xfusion.com> - 4.13.1-4
- Update dependencies

* Thu Nov 17 2022 wulei <wulei80@h-partners.com> - 4.13.1-3
- Replace openEuler with %{_vendor}

* Wed Nov 9 2022 liyanan <liyanan32@h-partners.com>  - 4.13.1-2
- Change source

* Tue Jan 18 2022 yangping <yangping69@huawei.com> - 4.13.1-1
- Update software to 4.13.1

* Wed Aug 11 2021 lingsheng <lingsheng@huawei.com> - 4.07.0-8
- Fix build error with Glibc 2.34

* Fri Jul 30 2021 sunguoshuai <sunguoshuai@huawei.com> - 4.07.0-7
- compile with -fcommon to support gcc 10

* Wed Jan 22 2020 yanzhihua <yanzhihua4@huawei.com> - 4.07.0-6
- modify patching method

* Mon Jan 13 2020 openEuler Buildteam <buildteam@openeuler.org> - 4.07.0-5
- update software package

* Thu Dec 12 2019 openEuler BuildTeam<buildteam@openeuler.org> - 4.07.0-4
- Add requires_opts and provides_opts

* Mon Dec 09 2019 openEuler BuildTeam<buildteam@openeuler.org> - 4.07.0-3
- Package Init


