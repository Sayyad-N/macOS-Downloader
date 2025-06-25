# macOS Recovery & Installer Download Tool

**Author:** SayyadN  
**Version:** 2  
**Date:** 25-6-2025

A comprehensive Python tool for downloading macOS recovery images, installers, and EFI folders for Hackintosh setups.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Command Line Arguments](#command-line-arguments)
- [Actions](#actions)
- [Examples](#examples)
- [EFI Support](#efi-support)
- [Technical Details](#technical-details)
- [Credits](#credits)
- [Troubleshooting](#troubleshooting)

## 🔍 Overview

This tool provides a complete solution for downloading and managing macOS recovery images and installers. It's particularly useful for:

- Creating macOS recovery media
- Downloading official macOS installers
- Validating MLB (Main Logic Board) serial numbers
- Finding compatible EFI configurations for Hackintosh setups
- Automated verification of downloaded images

## ✨ Features

- **Recovery Image Download**: Download official macOS recovery images from Apple servers
- **Installer Download**: Get full macOS installer applications
- **MLB Validation**: Verify and guess compatible Mac models for MLB serial numbers
- **EFI Information**: Get processor-specific EFI recommendations
- **Image Verification**: Automatic chunklist verification for downloaded images
- **Progress Tracking**: Real-time download progress with visual indicators
- **Multiple macOS Versions**: Support for macOS versions from Snow Leopard to Sequoia

## 📋 Prerequisites

### Required Files
The tool requires these files in the same directory:
- `macos.py` (main script)
- `boards.json` (Mac board database)
- `build-image.sh` (build script)

### Required Python Packages
```bash
pip install xattr cpuinfo plistlib
```

### System Requirements
- **macOS**: Required for full functionality (uses system tools like `hdiutil`)
- **Python 3**: Python 2 is not supported
- **Root Access**: Required for package installation operations

## 🚀 Installation (Works Well with macOS)

1. **Clone or download** all required files to a directory
2. **Install dependencies**:
   ```bash
   pip install xattr cpuinfo
   ```
3. **Make executable** (if needed):
   ```bash
   chmod +x macos.py
   ```

## 💻 Usage

### Basic Syntax
```bash
sudo python3 macos.py [action] [options]
```

**Note**: Root privileges are required for most operations.

## 🎛️ Command Line Arguments

### Actions (Required)
- `download` - Download recovery images or installers
- `selfcheck` - Verify MLB validation system
- `verify` - Validate a specific MLB serial number
- `guess` - Find compatible Mac models for an MLB

### Core Options
| Option | Description | Default |
|--------|-------------|---------|
| `-o, --outdir` | Output directory | `com.apple.recovery.boot` |
| `-n, --basename` | Base filename for downloads | (empty) |
| `-b, --board-id` | Mac board identifier | `Mac-27AD2F918AE68F61` |
| `-m, --mlb` | Main Logic Board serial | `00000000000000000` |
| `-e, --code` | 4-character EEEE code | (empty) |
| `-os, --os-type` | OS type (`default` or `latest`) | `default` |

### Additional Options
| Option | Description |
|--------|-------------|
| `-diag, --diagnostics` | Download diagnostics instead of recovery |
| `-v, --verbose` | Enable verbose output |
| `-db, --board-db` | Path to boards database | `boards.json` |
| `--efi` | Show EFI information and download links |
| `--seedprogram` | Use specific seed program |
| `--catalogurl` | Custom catalog URL |
| `--workdir` | Working directory | `.` |
| `--compress` | Create compressed disk image |
| `--raw` | Keep raw sparse image |
| `--ignore-cache` | Ignore cached downloads |

### macOS Recovery Commands

| Version           | Command |
|------------------|---------|
| 1. Lion (10.7) | `python3 macrecovery.py -b Mac-2E6FAB96566FE58C -m 00000000000F25Y00 download` |
|                  | `python3 macrecovery.py -b Mac-C3EC7CD22292981F -m 00000000000F0HM00 download` |
| 2. Mountain Lion (10.8) | `python3 macrecovery.py -b Mac-7DF2A3B5E5D671ED -m 00000000000F65100 download` |
| 3. Mavericks (10.9) | `python3 macrecovery.py -b Mac-F60DEB81FF30ACF6 -m 00000000000FNN100 download` |
| 4. Yosemite (10.10) | `python3 macrecovery.py -b Mac-E43C1C25D4880AD6 -m 00000000000GDVW00 download` |
| 5. El Capitan (10.11) | `python3 macrecovery.py -b Mac-FFE5EF870D7BA81A -m 00000000000GQRX00 download` |
| 6. Sierra (10.12) | `python3 macrecovery.py -b Mac-77F17D7DA9285301 -m 00000000000J0DX00 download` |
| 7. High Sierra (10.13) | `python3 macrecovery.py -b Mac-7BA5B2D9E42DDD94 -m 00000000000J80300 download` |
|                   | `python3 macrecovery.py -b Mac-BE088AF8C5EB4FA2 -m 00000000000J80300 download` |
| 8. Mojave (10.14) | `python3 macrecovery.py -b Mac-7BA5B2DFE22DDD8C -m 00000000000KXPG00 download` |
| 9. Catalina (10.15) | `python3 macrecovery.py -b Mac-00BE6ED71E35EB86 -m 00000000000000000 download` |
| 10. Big Sur (11) | `python3 macrecovery.py -b Mac-42FD25EABCABB274 -m 00000000000000000 download` |
| 11. Monterey (12) | `python3 macrecovery.py -b Mac-FFE5EF870D7BA81A -m 00000000000000000 download` |
| 12. Ventura (13) | `python3 macrecovery.py -b Mac-4B682C642B45593E -m 00000000000000000 download` |
| 13. Sonoma (14) | `python3 macrecovery.py -b Mac-226CB3C6A851A671 -m 00000000000000000 download` |
| 14. Sequoia (15) | `python3 macrecovery.py -b Mac-937A206F2EE63C01 -m 00000000000000000 download` |


## 🎯 Actions

### 1. Download Action
Downloads macOS recovery images or full installers.

```bash
# Download latest recovery for default Mac
sudo python3 macos.py download

# Download with specific board ID
sudo python3 macos.py download -b Mac-E43C1C25D4880AD6

# Download latest version
sudo python3 macos.py download -os latest

# Download diagnostics
sudo python3 macos.py download -diag
```

### 2. Self-Check Action
Validates the MLB validation system against Apple servers.

```bash
sudo python3 macos.py selfcheck -v
```

### 3. Verify Action
Checks if a specific MLB serial number is valid.

```bash
# Verify specific MLB
sudo python3 macos.py verify -m F5K105303J9K3F71M

# Verify with board ID
sudo python3 macos.py verify -m F5K105303J9K3F71M -b Mac-E43C1C25D4880AD6
```

### 4. Guess Action
Attempts to find compatible Mac models for an MLB.

```bash
# Guess compatible models
sudo python3 macos.py guess -m F5K105303J9K3F71M

# Anonymous lookup
sudo python3 macos.py guess -m 000000000F9K3F700
```

## 📖 Examples

### Basic Recovery Download
```bash
sudo python3 macos.py download
```

### Download for Specific Mac Model
```bash
sudo python3 macos.py download -b Mac-7BA5B2D9E42DDD94 -o ~/Downloads/Recovery
```

### Download Latest macOS
```bash
sudo python3 macos.py download -os latest -v
```

### Verify Custom MLB
```bash
sudo python3 macos.py verify -m 123456789ABCDEFGH
```

### Download EFI
```bash
python3 macos.py --efi
```

## 🖥️ EFI Support

The tool includes built-in EFI folder recommendations:

### Processor Detection
- Automatically detects your CPU model
- Provides generation-specific recommendations
- Shows Intel processor generations (Nehalem to Meteor Lake)

### EFI Download
- Direct link to Olarila EFI collection
- Processor-specific configurations
- Hackintosh compatibility guides

### Intel Generations Supported
- i5-1xxx (Nehalem)
- i5-2xxx (Sandy Bridge)  
- i5-3xxx (Ivy Bridge)
- i5-4xxx (Haswell)
- i5-5xxx (Broadwell)
- i5-6xxx (Skylake)
- i5-7xxx (Kaby Lake)
- i5-8xxx (Coffee Lake)
- i5-9xxx (Coffee Lake Refresh)
- i5-10xxx (Comet Lake/Ice Lake)
- i5-11xxx (Tiger Lake/Rocket Lake)
- i5-12xxx (Alder Lake)
- i5-13xxx (Raptor Lake)
- i5-14xxx/Core 5xxx (Meteor Lake/Core Ultra)

## AMD CPUs not Supported Official by Apple (only Intel)

## 🔧 Technical Details

### Supported macOS Versions
The tool supports downloading from these macOS versions:
- macOS 10.13 High Sierra (17)
- macOS 10.14 Mojave (18)
- macOS 10.15 Catalina (19)
- macOS 11 Big Sur (20)
- macOS 12 Monterey (21)
- macOS 13 Ventura (22)
- macOS 14 Sonoma (23)
- macOS 15 Sequoia (24)

### File Verification
- **Chunklist Verification**: Automatic verification using Apple's chunklist system
- **Digital Signatures**: RSA signature validation with Apple's public key
- **Hash Verification**: SHA-256 chunk verification
- **Progress Tracking**: Real-time verification progress

### MLB Format
- **Standard Format**: 17-character alphanumeric string
- **EEEE Code**: 4-character code conversion support
- **Anonymous Format**: Zero-padded anonymous MLB support

##  Credits

This tool builds upon excellent work from:
- **macrecovery_open_core**: [OpenCore Team](https://tinyurl.com/bdfkbw43)
- **olarila_efis**: [Olarila EFI Collection](https://tinyurl.com/rkr3w93n)
- **Special Thanks**: Tim Sutton, Greg Neagle, and vit9696

## 🐛 Troubleshooting

### Common Issues

#### 1. "This tool requires the Python xattr module"
```bash
pip install xattr
```

#### 2. "This command requires root"
Always run with `sudo` for download operations.

#### 3. "One or more required files are missing"
Ensure all required files are in the same directory:
- `macos.py`
- `boards.json`
- `build-image.sh`

#### 4. Download Failures
- Check internet connection
- Try with `--ignore-cache` flag
- Verify board ID is correct

#### 5. "Invalid chunklist"
- Re-download the files
- Check available disk space
- Verify network stability during download

### Debug Mode
Use `-v` or `--verbose` flag for detailed debug information:
```bash
sudo python3 macos.py download -v
```

### Network Issues
If downloads fail, try:
```bash
# Ignore cache and retry
sudo python3 macos.py download --ignore-cache

# Use different working directory
sudo python3 macos.py download --workdir /tmp/macos_download
```

## 📝 Notes

- **Apple Servers**: This tool connects directly to Apple's official servers
- **Authenticity**: All downloads are verified against Apple's digital signatures
- **Legal**: Only downloads publicly available Apple software
- **Compatibility**: Designed for legitimate macOS recovery and installation needs

## 🔗 Resources

- **OpenCore Guide**: [Dortania's OpenCore Install Guide](https://dortania.github.io/OpenCore-Install-Guide/)
- **EFI Files**: [Olarila EFI Repository](https://tinyurl.com/rkr3w93n)
- **macOS Compatibility**: [Apple Support - macOS Compatibility](https://support.apple.com/en-us/HT201475)

---

For issues or contributions, please ensure you have the latest version of all required files and dependencies.
