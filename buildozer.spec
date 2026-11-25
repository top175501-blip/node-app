[app]
title = Node App
package.name = nodeapp
package.domain = org.nodeapp
source.dir = .
source.include_exts = py
version = 0.1
requirements = python3,kivy==2.3.0,websockets==12.0
orientation = portrait
fullscreen = 0
android.permissions = INTERNET,FOREGROUND_SERVICE,WAKE_LOCK
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.archs = arm64-v8a
android.accept_sdk_license = True
p4a.branch = v2024.01.21

[buildozer]
log_level = 2
warn_on_root = 1
