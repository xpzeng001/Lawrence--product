import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { basename, dirname, extname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { spawnSync } from "node:child_process";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const indexHtml = readFileSync(join(root, "index.html"), "utf8");
const skillsHtml = readFileSync(
  join(root, "compositions/professional-skills-animated-chapter.html"),
  "utf8",
);
const narrationPlan = JSON.parse(
  readFileSync(join(root, "assets/narration/narration-plan.json"), "utf8"),
);

const transcriptDir = join(root, "assets/transcripts");
const rawTranscriptDir = join(transcriptDir, "raw");
mkdirSync(transcriptDir, { recursive: true });
mkdirSync(rawTranscriptDir, { recursive: true });

function attrs(tag) {
  return Object.fromEntries(
    [...tag.matchAll(/([\w-]+)="([^"]*)"/g)].map((match) => [match[1], match[2]]),
  );
}

function audioTags(html) {
  return [...html.matchAll(/<audio\b[^>]*>/g)].map((match) => attrs(match[0]));
}

function round(value) {
  return Number(value.toFixed(3));
}

function transcriptPathFor(id) {
  return join(transcriptDir, `${id}.json`);
}

function rawTranscriptPathFor(id) {
  return join(rawTranscriptDir, `${id}.json`);
}

function toSeconds(offsetMs) {
  return round(offsetMs / 1000);
}

function usableToken(token) {
  const text = token.text?.trim();
  if (!text) return false;
  if (/^\[.*\]$/.test(text)) return false;
  if (/^[,.;:!?，。；：！？、\s]+$/.test(text)) return false;
  if (text.includes("�")) return false;
  const from = token.offsets?.from;
  const to = token.offsets?.to;
  return Number.isFinite(from) && Number.isFinite(to) && to > from;
}

function parseRawTokens(raw) {
  return raw.transcription.flatMap((segment) =>
    (segment.tokens ?? [])
      .filter(usableToken)
      .map((token) => ({
        text: token.text.trim(),
        start: toSeconds(token.offsets.from),
        end: toSeconds(token.offsets.to),
        confidence: token.p,
      })),
  );
}

function semanticWords(text) {
  const cleanText = text.replace(/[，。；：！？、,.;:!?]/g, " ").replace(/\s+/g, " ").trim();
  if (!cleanText) return [];

  const segmenter = new Intl.Segmenter("zh", { granularity: "word" });
  return [...segmenter.segment(cleanText)]
    .filter((part) => part.isWordLike)
    .map((part) => part.segment);
}

function wordsFromTokens(tokens, expectedText) {
  if (!expectedText) {
    return tokens;
  }

  const expectedWords = semanticWords(expectedText);
  if (expectedWords.length === 0 || tokens.length === 0) {
    return tokens;
  }

  if (expectedWords.length === 1) {
    return [{ text: expectedWords[0], start: tokens[0].start, end: tokens.at(-1).end }];
  }

  const totalStart = tokens[0].start;
  const totalEnd = tokens.at(-1).end;
  const weights = expectedWords.map((word) => Math.max(1, [...word].length));
  const totalWeight = weights.reduce((sum, weight) => sum + weight, 0);
  let cursor = totalStart;
  return expectedWords.map((word, index) => {
    const isLast = index === expectedWords.length - 1;
    const duration = ((totalEnd - totalStart) * weights[index]) / totalWeight;
    const start = cursor;
    const end = isLast ? totalEnd : round(cursor + duration);
    cursor = end;
    return { text: word, start: round(start), end: round(Math.max(end, start + 0.01)) };
  });
}

const mainAudios = audioTags(indexHtml)
  .filter((audio) => audio.id !== "professional-skills-main-audio")
  .filter((audio) => audio.id === "opening-audio" || audio.id?.startsWith("narration-"))
  .map((audio) => ({
    id: audio.id,
    src: audio.src,
    start: Number(audio["data-start"]),
    duration: Number(audio["data-duration"]),
    scope: "main",
  }));

const professionalStartMatch = indexHtml.match(
  /id="professional-skills-main-clip"[\s\S]*?data-start="([^"]+)"/,
);
const professionalStart = professionalStartMatch ? Number(professionalStartMatch[1]) : 0;

const skillAudios = audioTags(skillsHtml).map((audio) => ({
  id: audio.id,
  src: audio.src,
  start: round(professionalStart + Number(audio["data-start"])),
  localStart: Number(audio["data-start"]),
  duration: Number(audio["data-duration"]),
  scope: "professional-skills",
}));

const segments = [...mainAudios, ...skillAudios].sort((a, b) => a.start - b.start);
const expectedTextById = new Map(
  narrationPlan.segments.map((segment) => [`narration-${segment.id}`, segment.text]),
);

function transcribe(segment) {
  const outPath = transcriptPathFor(segment.id);
  if (existsSync(outPath)) {
    return JSON.parse(readFileSync(outPath, "utf8"));
  }

  const rawPath = rawTranscriptPathFor(segment.id);
  const absoluteSrc = join(root, segment.src);
  if (!existsSync(rawPath)) {
    let whisperInput = absoluteSrc;
    if (extname(absoluteSrc).toLowerCase() !== ".wav") {
      whisperInput = join(rawTranscriptDir, `${segment.id}.input.wav`);
      const ffmpeg = spawnSync(
        "/opt/homebrew/bin/ffmpeg",
        ["-y", "-i", absoluteSrc, "-vn", "-ac", "1", "-ar", "16000", whisperInput],
        {
          cwd: root,
          encoding: "utf8",
          stdio: ["ignore", "pipe", "pipe"],
        },
      );
      if (ffmpeg.status !== 0 || !existsSync(whisperInput)) {
        throw new Error(`Failed to prepare WAV for ${segment.id}\n${ffmpeg.stdout}\n${ffmpeg.stderr}`);
      }
    }
    const outputPrefix = join(rawTranscriptDir, segment.id);
    const result = spawnSync(
      "/opt/homebrew/bin/whisper-cli",
      [
        "--model",
        "/Users/xp/.cache/hyperframes/whisper/models/ggml-large-v3.bin",
        "--output-json-full",
        "--output-file",
        outputPrefix,
        "--suppress-nst",
        "--language",
        "zh",
        whisperInput,
      ],
      {
        cwd: root,
        encoding: "utf8",
        stdio: ["ignore", "pipe", "pipe"],
      },
    );

    if (result.status !== 0) {
      throw new Error(
        `Failed to transcribe ${segment.id} (${segment.src})\n${result.stdout}\n${result.stderr}`,
      );
    }

    if (!existsSync(rawPath)) {
      throw new Error(`Whisper did not produce ${rawPath}\n${result.stdout}\n${result.stderr}`);
    }
  }

  const raw = JSON.parse(readFileSync(rawPath, "utf8"));
  const tokens = parseRawTokens(raw);
  const words = wordsFromTokens(tokens, expectedTextById.get(segment.id));
  writeFileSync(
    outPath,
    JSON.stringify(
      {
        id: segment.id,
        source: segment.src,
        expectedText: expectedTextById.get(segment.id) ?? null,
        recognizedText: raw.transcription.map((item) => item.text).join("").trim(),
        tokens,
        words,
      },
      null,
      2,
    ),
  );
  return words;
}

const combinedWords = [];
const cues = [];

for (const segment of segments) {
  process.stderr.write(`Transcribing ${segment.id} (${basename(segment.src)})...\n`);
  const transcript = transcribe(segment);
  const words = Array.isArray(transcript) ? transcript : transcript.words;
  const normalizedWords = words.map((word, index) => ({
    id: `${segment.id}-w${String(index + 1).padStart(3, "0")}`,
    segmentId: segment.id,
    scope: segment.scope,
    source: segment.src,
    text: word.text,
    localStart: round(word.start),
    localEnd: round(word.end),
    start: round(segment.start + word.start),
    end: round(segment.start + word.end),
  }));

  combinedWords.push(...normalizedWords);
  cues.push({
    id: segment.id,
    scope: segment.scope,
    source: segment.src,
    start: segment.start,
    end: round(segment.start + segment.duration),
    duration: segment.duration,
    wordCount: normalizedWords.length,
    text: normalizedWords.map((word) => word.text).join(""),
    firstWordStart: normalizedWords[0]?.start ?? segment.start,
    lastWordEnd: normalizedWords.at(-1)?.end ?? round(segment.start + segment.duration),
  });
}

const wordTimeline = {
  generatedBy: "tools/transcribe-narration.mjs",
  model: "large-v3",
  language: "zh",
  wordCount: combinedWords.length,
  segments: cues,
  words: combinedWords,
};

writeFileSync(
  join(root, "assets/narration/word-timestamps.json"),
  JSON.stringify(wordTimeline, null, 2),
);
writeFileSync(join(root, "assets/narration/sync-cues.json"), JSON.stringify(cues, null, 2));

process.stdout.write(
  JSON.stringify(
    {
      ok: true,
      segments: cues.length,
      words: combinedWords.length,
      wordTimeline: "assets/narration/word-timestamps.json",
      syncCues: "assets/narration/sync-cues.json",
    },
    null,
    2,
  ),
);
