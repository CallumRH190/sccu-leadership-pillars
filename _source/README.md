# Build source for the Leadership Pillars tool

Everything used to build the tool, the two videos and the PDF for James.
It is kept here so the work can be rebuilt from scratch. It is excluded from the public site by `.vercelignore` in the repository root. Checked on 13 November 2026: `/_source/README.md` returns "not found" on the live site.

The full explanation is in `SCCU-LEADERSHIP-PILLARS-HANDOVER.md` in the SCCU DEVELOPMENT project.

## What is where

| Folder | What it holds |
|---|---|
| `tool/` | `src.html` is the readable source of the tool. `build.py` embeds the fonts and writes the published pages. `shots.py` is the full click-through test. `pdf.py` makes the sample summary PDF |
| `videos/how/` | `film3.py` films the how video to Callum's recording. `cut_how.py` cuts his recording into lines. `asr.py` transcribes with word timings. `chk.py` transcribes a finished video to check it. `film2.py` is the earlier stand-in voice version |
| `videos/why/` | `build_html_voice.py` builds the slides. `film_voice2.py` films them. `cut_original_recording.py` and `cut_four_new_lines.py` cut the two recordings |
| `pdf/` | `make2.py` builds the two-page PDF for James, with its three thumbnails |
| `review/` | The review pack and the prompts for the five reviewers |
| `recordings/` | Callum's three original voice recordings |

## To rebuild

- Fonts come from the `@fontsource` packages listed in `tool/package.json` (`npm install`).
- The scripts expect Python with Playwright, a system Chrome, ffmpeg, numpy and soundfile.
- The stand-in voice used Kokoro. Transcription used sherpa-onnx with the Parakeet model. Both models were downloaded from GitHub releases and are not stored here.
- Paths inside the scripts point at the folders used when they were written (`/home/claude/...`). Change them to match where you put the files.
