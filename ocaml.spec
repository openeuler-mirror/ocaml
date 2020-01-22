Name:           ocaml
Version:        4.07.0
Release:        6 
Summary:        OCaml compiler and programming environment
License:        QPL and (LGPLv2+ with exceptions)
URL:            http://www.ocaml.org
Source0:        http://caml.inria.fr/pub/distrib/ocaml-4.07/ocaml-%{version}.tar.xz

Patch0002:      0002-ocamlbyteinfo-ocamlplugininfo-Useful-utilities-from-.patch
Patch0003:      0003-configure-Allow-user-defined-C-compiler-flags.patch

BuildRequires:  gcc binutils-devel ncurses-devel gdbm-devel emacs gawk perl-interpreter
BuildRequires:  util-linux libICE-devel libSM-devel libX11-devel libXaw-devel libXext-devel
BuildRequires:  libXft-devel libXmu-devel libXrender-devel libXt-devel chrpath

Requires:       gcc util-linux libX11-devel emacs(bin)

Provides:       bundled(md5-plumb) ocaml(runtime) = %{version}
Provides:       ocaml(compiler) = %{version}
Provides:       %{name}-runtime
Obsoletes:      %{name}-runtime
Provides:       %{name}-x11
Obsoletes:      %{name}-x11
Provides:       %{name}-ocamldoc
Obsoletes:      %{name}-ocamldoc
Provides:       %{name}-emacs
Obsoletes:      %{name}-emacs

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
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

Provides:  %{name}-docs
Obsoletes: %{name}-docs

%description help
Help files for %{name}

%prep
%autosetup -n %{name}-%{version} -p1

%build
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing" \
./configure \
    -bindir %{_bindir} \
    -libdir %{_libdir}/ocaml \
    -x11lib %{_libdir} \
    -x11include %{_includedir} \
    -mandir %{_mandir}/man1 \
    -no-curses
%make_build world
%make_build opt
%make_build opt.opt
make -C emacs ocamltags

includes="-nostdlib -I stdlib -I utils -I parsing -I typing -I bytecomp -I asmcomp -I driver -I otherlibs/unix -I otherlibs/str -I otherlibs/dynlink"
boot/ocamlrun ./ocamlc $includes dynlinkaux.cmo ocamlbyteinfo.ml -o ocamlbyteinfo

%check
cd testsuite
make -j1 all

%install
make install \
     BINDIR=%{buildroot}%{_bindir} \
     LIBDIR=%{buildroot}%{_libdir}/ocaml \
     MANDIR=%{buildroot}%{_mandir}
perl -pi -e "s|^%{buildroot}||" %{buildroot}%{_libdir}/ocaml/ld.conf

(
    # install emacs files
    cd emacs;
    make install \
         BINDIR=%{buildroot}%{_bindir} \
         EMACSDIR=%{buildroot}%{_datadir}/emacs/site-lisp
    make install-ocamltags BINDIR=%{buildroot}%{_bindir}
)

echo %{version} > %{buildroot}%{_libdir}/ocaml/openEuler-ocaml-release

chrpath --delete %{buildroot}%{_libdir}/ocaml/stublibs/*.so

install -m 0755 ocamlbyteinfo %{buildroot}%{_bindir}

find %{buildroot} -name .ignore -delete
find %{buildroot} \( -name '*.cmt' -o -name '*.cmti' \) -a -delete

%files
%license LICENSE
%{_bindir}/ocaml
%{_bindir}/ocamlbyteinfo
%{_bindir}/ocamlcmt
%{_bindir}/ocamldebug
%{_bindir}/ocaml-instr-graph
%{_bindir}/ocaml-instr-report
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
%{_libdir}/ocaml/objinfo_helper
%{_libdir}/ocaml/vmthreads/*.mli
%{_libdir}/ocaml/vmthreads/*.a
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
%{_libdir}/ocaml/VERSION
%{_libdir}/ocaml/*.cmo
%{_libdir}/ocaml/*.cmi
%{_libdir}/ocaml/*.cma
%{_libdir}/ocaml/stublibs
%{_libdir}/ocaml/target_camlheaderd
%{_libdir}/ocaml/target_camlheaderi
%dir %{_libdir}/ocaml/vmthreads
%{_libdir}/ocaml/vmthreads/*.cmi
%{_libdir}/ocaml/vmthreads/*.cma
%dir %{_libdir}/ocaml/threads
%{_libdir}/ocaml/threads/*.cmi
%{_libdir}/ocaml/threads/*.cma
%{_libdir}/ocaml/openEuler-ocaml-release

#x11
%{_libdir}/ocaml/graphicsX11.cmi
%{_libdir}/ocaml/graphicsX11.mli

#ocamldoc
%doc ocamldoc/Changes.txt
%{_bindir}/ocamldoc*
%{_libdir}/ocaml/ocamldoc

#emacs
%doc emacs/README
%{_datadir}/emacs/site-lisp/*
%{_bindir}/ocamltags

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
* Thu Jan 22 2020 yanzhihua <yanzhihua4@huawei.com> - 4.07.0-6
- modify patching method

* Mon Jan 13 2020 openEuler Buildteam <buildteam@openeuler.org> - 4.07.0-5
- update software package

* Thu Dec 012 2019 openEuler BuildTeam<buildteam@openeuler.org> - 4.07.0-4
- Add requires_opts and provides_opts

* Mon Dec 09 2019 openEuler BuildTeam<buildteam@openeuler.org> - 4.07.0-3
- Package Init
