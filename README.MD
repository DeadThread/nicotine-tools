# Nicotine Tools

A collection of plugins for [Nicotine+](https://nicotine-plus.github.io/nicotine-plus/), the open-source Soulseek client.

## Plugins

### Rescan Timer

Automatically rescans shared folders every 6 hours (configurable).

## Installation

Clone this repository directly into your Nicotine+ plugins directory:

```bash
# Windows
cd "%APPDATA%\nicotine\plugins"
git clone https://github.com/DeadThread/nicotine-tools.git
cd nicotine-tools

# Linux/macOS  
cd ~/.nicotine/plugins
git clone https://github.com/DeadThread/nicotine-tools.git
cd nicotine-tools
```

Then copy the plugin to your plugins directory:

```bash
# Copy the rescan_timer plugin
cp -r plugins/rescan_timer ../rescan_timer
```

Or manually copy the `plugins/rescan_timer` folder to your Nicotine+ plugins directory.

## Usage

1. Restart Nicotine+
2. Go to Settings → Plugins
3. Enable "Rescan Timer"
4. Look for "Rescanning shares..." messages in your log every 6 hours

## Configuration

To change the interval, edit `RESCAN_INTERVAL_MINUTES` in `rescan_timer/__init__.py`:

```python
RESCAN_INTERVAL_MINUTES = 360  # 360 = 6 hours, 60 = 1 hour, etc.
```

## Requirements

- Nicotine+ 3.0.0+