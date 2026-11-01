# 网易云音乐 GPUI · NetEase Music GPUI

**版本 / Version:** `{{version}}` · **构建 / Build:** `{{tag}}` · **日期 / Date:** {{date}} · **提交 / Commit:** [`{{short_sha}}`]({{commit_url}})

> 每日自动构建，把上游 `AMagicPear/netease-music-gpui` 的最新改动带进这个 fork。
> Daily automated build that carries the latest upstream changes from `AMagicPear/netease-music-gpui` into this fork.

## 下载 / Downloads

{{artifacts}}

Windows 压缩包附带 `.sha256` 校验文件；其余平台的包内含可执行文件与 `assets` 资源目录。
The Windows archive ships a `.sha256` checksum file; the other packages contain the executable and the `assets` directory.

## 安装与运行 / Install and Run

- **macOS** — 解压 `netease-music-macos-*.zip`，把 `NetEase Music.app` 拖进「应用程序」文件夹。
  Unzip the archive and drag `NetEase Music.app` into your Applications folder.
- **Windows** — 完整解压 `netease-music-gpui-windows-x64-*.zip`，再运行 `netease-music-gpui.exe`。
  Extract the whole archive, then run `netease-music-gpui.exe`.
- **Linux** — 解压 `netease-music-gpui-linux-x64.tar.gz`，运行 `netease-music-gpui`。
  Untar the archive and run `netease-music-gpui`.

启动后点击顶部头像或昵称，用网易云音乐 App 扫码登录。
Click the avatar in the top bar and sign in by scanning the QR code with the NetEase Cloud Music app.

## 本次变更 / Changes

{{changes}}

## 已知限制 / Known Limitations

- 高音质取决于账号权限与歌曲资源，接口可能返回较低音质、试听片段，或因权限与下架状态无法播放。
  Audio quality depends on the account privileges and on what the service returns; the API may serve lower
  qualities or preview clips, and some tracks may be unavailable.
- 播放队列暂不支持排序和删除；部分页面仍是占位实现。
  The play queue cannot be reordered or pruned yet, and some screens are still placeholders.
- macOS 产物只做了本地 ad-hoc 签名，没有 Apple 公证，首次打开可能需要在「系统设置 → 隐私与安全性」中放行。
  The macOS build is ad-hoc signed and not notarized by Apple, so macOS may ask you to allow it on first launch.

## 关于 / About

用 Rust 和 [GPUI](https://gpui.rs/) 复刻网易云音乐桌面界面的练手项目。
A learning project that rebuilds the NetEase Cloud Music desktop interface with Rust and [GPUI](https://gpui.rs/).

这是练习项目，与网易官方客户端无关。
This is a practice project and is not affiliated with the official client.
