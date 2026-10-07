# Headphone Sound Monitor

A small Python script that keeps your headphones from disconnecting by playing a near-inaudible sound whenever they're connected.

## Why I Made This

My headphones kept disconnecting from my PC whenever there was no active audio source — even if the silence only lasted a moment. This script works around that by continuously checking for a headphone output device and playing a very quiet, high-frequency tone to keep the connection alive.

## How It Works

- Scans your audio devices for anything matching `headphone`, `headset`, `earphone`, or `earbud`. If none are found, it falls back to the default output device.
- If a valid output device is available, it plays a short, very quiet 18 kHz sine wave.
- If no headphones are detected, it closes the audio stream and waits.
- Repeats the check every 2 seconds.

The tone is designed to be barely audible to most people (18 kHz at 1% volume), so it shouldn't be annoying during normal use.

## Requirements

- Python 3.x
- [PyAudio](https://pypi.org/project/PyAudio/)
- NumPy

Install dependencies with:

```bash
pip install pyaudio numpy