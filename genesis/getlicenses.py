import subprocess
import sys
import shlex

def runcmd(cmd):
    return subprocess.check_output(shlex.split(cmd)).decode('utf8').split('\n')

def getsrpm(rpm):
    rpminfo = runcmd(f'rpm -qi {rpm}')
    for inf in rpminfo:
        if inf.startswith('Source RPM'):
            srpm = inf.split(':', 1)[1].strip()
            return srpm

srpmtorpm = {}
rpmtosrpm = {}
allrpmlist = runcmd('rpm -qa')
for rpm in allrpmlist:
    if not rpm:
        continue
    srpm = getsrpm(rpm)
    rpmtosrpm[rpm] = srpm
    if srpm in srpmtorpm:
        srpmtorpm[srpm].add(rpm)
    else:
        srpmtorpm[srpm] = {rpm}

with open(sys.argv[1]) as rpmlist:
    rpmlist = rpmlist.read().split('\n')
licenses = set([])
licensesbyrpm = {}
for rpm in rpmlist:
    if not rpm:
        continue
    srpm = rpmtosrpm[rpm]
    if srpm.startswith('linux-firmware'):
        continue
    for relrpm in srpmtorpm[srpm]:
        if relrpm.startswith('libss-'):
            continue
        liclist = runcmd(f'rpm -qL {relrpm}')
        for lic in liclist:
            if not lic:
                continue
            if lic == '(contains no files)':
                continue
            licensesbyrpm[rpm] = lic
            licenses.add(lic)
for lic in sorted(licenses):
    print(lic)
manualrpms = [
    'ipmitool',
    'almalinux-release',
    'libaio',
    'hwdata',
    'snmp',
    'libnl3',
    'libbpf',  # this is covered by kernel, but need to make a directory explaining. libbpf is literally just a copy of the kernel source rpm
    'sqlite',  # public domain
    'linux-firmware',  #all pertinent licenses are stripped out
    'xfsprogs',  # manually added by hand below (not in rpm)
    'tmux',  # use the extracttmuxlicenses on the source to generate NOTICE below
]
manuallicenses = [
    '/usr/share/licenses/lz4/LICENSE.BSD',
    # cp /usr/share/doc/lz4-libs/LICENSE /usr/share/licenses/lz4/LICENSE.BSD
    #'lz4-1.8.3]# cp LICENSE  /usr/share/licenses/lz4/LICENSE'
    # net-snmp has a bundled openssl, but the build does not avail itself of that copy
    '/usr/share/licenses/perl-libs/LICENSE', # ./dist/ExtUtils-CBuilder/LICENSE from perl srpm
    '/usr/share/licenses/lz4/LICENSE',
    '/usr/share/licenses/lm_sensors/COPYING',
    '/usr/share/doc/libunistring/README',
    '/usr/share/doc/hostname/COPYRIGHT',
    '/usr/share/doc/hwdata/COPYING',
    '/usr/share/doc/zstd/README.md',
    '/usr/share/doc/hwdata/LICENSE',
    '/usr/share/doc/ipmitool/COPYING',
    '/usr/share/doc/libaio/COPYING',
    '/usr/share/doc/net-snmp/COPYING',
    '/usr/share/doc/libnl3/COPYING',
    '/usr/share/licenses/xfsprogs/GPL-2.0',
    '/usr/share/licenses/xfsprogs/LGPL-2.1',
    '/usr/share/licenses/tmux/NOTICE',
    '/usr/share/licenses/kernel-extra/exceptions/Linux-syscall-note',
    '/usr/share/licenses/kernel-extra/other/Apache-2.0',
    '/usr/share/licenses/kernel-extra/other/CC-BY-SA-4.0',
    '/usr/share/licenses/kernel-extra/other/CDDL-1.0',
    '/usr/share/licenses/kernel-extra/other/GPL-1.0',
    '/usr/share/licenses/kernel-extra/other/Linux-OpenIB',
    '/usr/share/licenses/kernel-extra/other/MPL-1.1',
    '/usr/share/licenses/kernel-extra/other/X11',
    '/usr/share/licenses/kernel-extra/preferred/BSD-2-Clause',
    '/usr/share/licenses/kernel-extra/preferred/BSD-3-Clause',
    '/usr/share/licenses/kernel-extra/preferred/BSD-3-Clause-Clear',
    '/usr/share/licenses/kernel-extra/preferred/GPL-2.0',
    '/usr/share/licenses/kernel-extra/preferred/LGPL-2.0',
    '/usr/share/licenses/kernel-extra/preferred/LGPL-2.1',
    '/usr/share/licenses/kernel-extra/preferred/MIT',
    '/usr/share/licenses/util-linux/COPYING.GPLv3', # extract from parse-date.c, from srpm
    '/usr/share/licenses/kmod/tools/COPYING', # GPL not LGPL, must extract from kmod srpm
    '/usr/share/licenses/krb5-libs/NOTICE', # copy it verbatim from LICENSE, exact same file
    '/usr/share/doc/less/README',
    '/usr/share/licenses/libcap-ng-utils/COPYING',
    '/usr/share/licenses/libdb/copyright', # from libdb, db-5.3.28, lang/sql/odbc/debian/copyright
    '/usr/share/licenses/libgcrypt/LICENSES.ppc-aes-gcm', # libgcrypt license to carry forward
    '/usr/share/licenses/libgcrypt/LICENSES', # OCB is covered by several.. OCB license 
    '/usr/share/licenses/libgcrypt/README'
]
for lic in manuallicenses:
    print(lic)
for rpm in rpmlist:
    if not rpm:
        continue
    for manualrpm in manualrpms:
        if manualrpm in rpm:
            break
    else:
        if rpm not in licensesbyrpm:
            raise Exception('Unresolved license info for ' + rpm)
            print("UH OH: " + rpm)
            

