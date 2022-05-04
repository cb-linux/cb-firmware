# About the linux-firmware project

Please be aware that this project is not just a local Chrome OS project.
It is actually intended to (roughly) match up with the upstream git
repository hosted at:

https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/

As such we shouldn't just dump random binary files here.  The flow should be
like the [Chrome OS kernel upstream process].  In other words:
* First, submit firmware to the upstream linux-firmware repo.
* Second, pick the firmware to the Chrome OS tree, tagging it UPSTREAM.

If we have to (due to an urgent bugfix) we can make local (CHROMIUM) changes
here but the policy is that things that get put here are on their way
to the upstream linux-firmware project.

Also, matching the kernel policies, changes to files like OWNERS or this
README should be marked CHROMIUM indicating that they're not ever going
upstream.

See also the [README] file here, which comes from upstream.

## The WHENCE file

Presumably if you're landing your firmware in the upstream linux-firmware
repository then upstream will make sure to remind folks to update the [WHENCE]
file.  You should make sure that you get relevant updates to the [WHENCE] file
when you pick your firmware.  If we need to do a local change, please make
sure to confirm that the [WHENCE] file still makes sense.

Of special note is that the [WHENCE] says what license the binary was released
under.  See below.

NOTE: Run 'make check' to check that WHENCE is consistent with the
repository contents.

## Licenses

When picking firmware, please confirm that the license is still right / sane.
Licenses here have been copied to chromiumos-overlay:

https://chromium.googlesource.com/chromiumos/overlays/chromiumos-overlay/+/refs/heads/master/licenses/

You should confirm that:
* The license here still matches the one in chromiumos-overlay.
* The license here still matches upstream if you're picking a new firmware
  from upstream (use the [upstream WHENCE] to find the right license).

To figure out what license matches with the firmware, refer to the
[linux-firmware ebuild file].  Figure out what `LINUX_FIRMWARE` flag chooses
your firmware and then figure out what license the ebuild file matches it up
with.

## How firmware gets installed

Firmware is installed via the [linux-firmware ebuild file].  Board overlays
specify `LINUX_FIRMWARE` in their make.defaults (or equivalent) and that tells
the ebuild what to install.

## Try to install only firmware you need

When thinking about getting firmware installed, remember that disk space
is at a premium.  Board overlays should specify exactly which firmware
they need.  In other words, say that you need firmware for a "Marvell
8897 SDIO WiFi" part, don't say you need firmware for "Marvell WiFi" or
(even worse) that you need firmware for "Marvell".

## Will we ever do a wholesale rebase to ToT linux-firmware?

Probably not.  See <https://crbug.com/770230#c10>.  Specifically:

We will likely not do a wholesale uprev of the linux-firmware.git.
Right now we are only picking a very small number of firmware files
to install and we'll manage those manually.  If this changes and we
find some reason to install a whole pile of firmware files that are
uprevving all the time, we can re-evaluate.

## What about files that aren't appropriate for upstream linux-firmware?

If you have firmware that is not appropriate for the upstream
linux-firmware project then this isn't the repository you're looking for.
In such a case you should find another place to put your firmware (probably
in BCS since git isn't ideal for storing binaries) and have your own ebuild
that installs the firmware.

Before trying to find another place for your firmware, however, please
remember that there's a pretty big benefit to getting firmware landed
in the upstream linux-firmware project.  Notably we _want_ upstream to be
testing / using the same firmware that Chrome OS is using.  This makes it
more likely for our systems to keep working across kernel uprevs and also
more likely that someone upstream will fix a problem and we'll get the fix
through stable merges.

[Chrome OS kernel upstream process]: https://chromium.googlesource.com/chromiumos/docs/+/master/kernel_development.md#UPSTREAM_BACKPORT_FROMLIST_and-you
[linux-firmware ebuild file]: https://chromium.googlesource.com/chromiumos/overlays/chromiumos-overlay/+/refs/heads/master/sys-kernel/linux-firmware/linux-firmware-9999.ebuild
[README]: ./README
[upstream WHENCE]: https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/tree/WHENCE
[WHENCE]: ./WHENCE

