#!/usr/bin/python

import os, re, sys
from io import open

def list_whence():
    with open('WHENCE', encoding='utf-8') as whence:
        for line in whence:
            match = re.match(r'(?:File|Source):\s*"(.*)"', line)
            if match:
                yield match.group(1)
                continue
            match = re.match(r'(?:File|Source):\s*(\S*)', line)
            if match:
                yield match.group(1)
                continue
            match = re.match(r'Licen[cs]e: (?:.*\bSee (.*) for details\.?|(\S*))\n',
                             line)
            if match:
                if match.group(1):
                    for name in re.split(r', | and ', match.group(1)):
                        yield name
                    continue
                if match.group(2):
                    # Just one word - may or may not be a filename
                    if not re.search(r'unknown|distributable', match.group(2),
                                     re.IGNORECASE):
                        yield match.group(2)
                        continue

def list_git():
    with os.popen('git ls-files') as git_files:
        for line in git_files:
            yield line.rstrip('\n')

def main():
    ret = 0
    whence_list = list(list_whence())
    known_files = set(name for name in whence_list if not name.endswith('/')) | \
                  set(['check_whence.py', 'configure', 'Makefile',
                       'README', 'copy-firmware.sh', 'WHENCE'])

    # TODO(https://crbug.com/1020597): exception list of files not yet listed
    # properly in WHENCE. Please remove from this list as you fix up WHENCE.
    known_files |= set([
        'ath10k/QCA6174/hw3.0/firmware-sdio-6.bin',
        'ath10k/QCA6174/hw3.0/notice_ath10k_firmware-sdio-6.txt',
        'ath10k/WCN3990/hw1.0/board-2.bin',
        'brcm/brcmfmac4356-pcie.txt',
        'brcm/brcmfmac4371-pcie.bin',
        'brcm/brcmfmac4371-pcie.txt',
        'intel/eve-only-ibt-hw-37.8.10-fw-22.50.19.14.f.bseq',
        'intel/fw_sst_0f28.bin',
        'intel/fw_sst_0f28.bin-48kHz_i2s_master',
        'intel/fw_sst_0f28.bin-i2s_master',
        'intel/fw_sst_0f28.bin-i2s_slave',
        'intel/fw_sst_0f28.bin-tdm_master',
        'intel/fw_sst_0f28.bin-tdm_slave',
        'intel/ibt-19-0-0.ddc',
        'intel/ibt-19-0-0.sfi',
        'intel/ibt-19-0-1.ddc',
        'intel/ibt-19-0-1.sfi',
        'iwlwifi-9000-pu-b0-jf-b0-43.ucode',
        'iwlwifi-9000-pu-b0-jf-b0-46.ucode',
        'iwlwifi-9260-th-b0-jf-b0-41.ucode',
        'iwlwifi-9260-th-b0-jf-b0-43.ucode',
        'iwlwifi-9260-th-b0-jf-b0-46.ucode',
        'iwlwifi-Qu-b0-jf-b0-43.ucode',
        'iwlwifi-Qu-c0-hr-b0-50.ucode',
        'iwlwifi-Qu-c0-hr-b0-53.ucode',
        'iwlwifi-QuZ-a0-hr-b0-48.ucode',
        'iwlwifi-QuZ-a0-hr-b0-50.ucode',
        'iwlwifi-QuZ-a0-hr-b0-53.ucode',
        'iwlwifi-cc-a0-46.ucode',
        'iwlwifi-cc-a0-50.ucode',
        'iwlwifi-cc-a0-53.ucode',
        'qca/nvm_00440302_eu.bin',
        'qca/nvm_00440302_i2s.bin',
        'qca/nvm_00440302_i2s_eu.bin',
        ])

    known_prefixes = set(name for name in whence_list if name.endswith('/'))
    git_files = set(list_git())

    known_files |= set(['OWNERS',
                        'PRESUBMIT.cfg',
                        'README.chromium.md',
                       ])

    for name in sorted(list(known_files - git_files)):
        sys.stderr.write('E: %s listed in WHENCE does not exist\n' % name)
        ret = 1

    for name in sorted(list(git_files - known_files)):
        # Ignore subdirectory changelogs and GPG detached signatures
        if (name.endswith('/ChangeLog') or
            (name.endswith('.asc') and name[:-4] in known_files)):
            continue

        # Ignore unknown files in known directories
        for prefix in known_prefixes:
            if name.startswith(prefix):
                break
        else:
            sys.stderr.write('E: %s not listed in WHENCE\n' % name)
            ret = 1
    return ret

if __name__ == '__main__':
    sys.exit(main())
