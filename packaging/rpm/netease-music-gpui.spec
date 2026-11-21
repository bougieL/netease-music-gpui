# RPM spec for the Linux build of NetEase Music GPUI.
#
# The package payload is prepared by scripts/build_rpm.py: it packs the
# prebuilt bundle (executable + assets/) together with the desktop entry and
# the icons into a source tarball, then builds this spec with rpmbuild.
# The Version below is rewritten from Cargo.toml at build time, so the literal
# only matters when reading this file.

Name:           netease-music-gpui
Version:        0.1.1
Release:        1%{?dist}
Summary:        NetEase Music desktop client written in Rust with GPUI
License:        MIT
URL:            https://github.com/bougieL/netease-music-gpui
Source0:        %{name}-%{version}.tar.gz
# The executable is prebuilt, so there is nothing to split debug symbols from.
%global debug_package %{nil}
# The app needs an audio backend (ALSA) and a Vulkan loader for its renderer.
# Package names are used instead of the sonames because Fedora only provides
# the (64bit) suffixed file dependencies.
Requires:       alsa-lib
Requires:       vulkan-loader

%description
A practice project that reimplements the NetEase Music desktop client with
Rust and GPUI. It supports QR code login, recommendations, personal playlists,
the play queue, heart mode, lyrics and comments.

This is a practice project and is not affiliated with the official client.

%prep
%setup -q -n %{name}-%{version}

# Nothing is compiled here: the executable is built by cargo and copied in
# by scripts/build_rpm.py.

%install
# %setup already moved into the unpacked source directory.
# The app resolves its resources relative to the executable, so the binary and
# assets/ must stay in the same directory.
install -d %{buildroot}%{_libdir}/%{name}
install -m 0755 netease-music-gpui \
    %{buildroot}%{_libdir}/%{name}/netease-music-gpui
cp -a assets %{buildroot}%{_libdir}/%{name}/assets
install -d %{buildroot}%{_datadir}/applications
install -m 0644 netease-music-gpui.desktop \
    %{buildroot}%{_datadir}/applications/%{name}.desktop
install -d %{buildroot}%{_datadir}/icons/hicolor/128x128/apps
install -m 0644 netease-music-gpui-128.png \
    %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{name}.png
install -d %{buildroot}%{_datadir}/icons/hicolor/256x256/apps
install -m 0644 netease-music-gpui-256.png \
    %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
install -d %{buildroot}%{_bindir}
# Relative symlink, as packaging guidelines ask for. The library directory is
# %{_libdir} (lib64 on most distributions), and the link lives in %{_bindir}.
ln -s ../$(basename %{_libdir})/%{name}/%{name} %{buildroot}%{_bindir}/%{name}

%post
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database -q %{_datadir}/applications || :
fi
if command -v gtk-update-icon-cache >/dev/null 2>&1; then
    gtk-update-icon-cache -q -t -f %{_datadir}/icons/hicolor || :
fi

%postun
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database -q %{_datadir}/applications || :
fi
if command -v gtk-update-icon-cache >/dev/null 2>&1; then
    gtk-update-icon-cache -q -t -f %{_datadir}/icons/hicolor || :
fi

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_libdir}/%{name}/netease-music-gpui
%{_libdir}/%{name}/assets
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/128x128/apps/%{name}.png
%{_datadir}/icons/hicolor/256x256/apps/%{name}.png

%changelog
* Sat Nov 21 2026 Bougie <36102904+bougieL@users.noreply.github.com> - 0.1.1-1
- Initial RPM packaging.
