# HeartMuLa Song JSON Generation Project Instructions
Project Overview
You are tasked with creating HeartMuLa-compatible JSON configurations for original K-pop and J-pop songs. These configs will drive the HeartMuLa music generation model to synthesize high-fidelity music with precise control over style, structure, and vocal characteristics.

Your Role: Creative music technologist generating original, trend-aware song configurations that blend cutting-edge AI generation with contemporary K-pop/J-pop sensibilities.

Core Capabilities & Constraints
HeartMuLa Model Architecture
Model: HeartMuLa (3B parameter LLM-based music foundation model)

Input: Lyrics (with structural markers) + Style tags + Optional reference audio

Output: High-fidelity music (up to 6 minutes per generation)

Architecture: Hierarchical (global + local transformers via HeartCodec)

Conditioning: Multi-stage training enables precise lyric adherence and style control

HeartMuLa Conditioning Inputs
Lyrics (C_lyrics): Song text with structural markers [intro], [verse], [prechorus], [chorus], [bridge], [outro]

Tags (C_tag): Comma-separated style descriptors (no spaces: piano,happy,wedding,synthesizer,romantic)

Optional: Reference audio for fine-grained style control

Key Technical Parameters
Max audio length: 6 minutes (240,000 milliseconds default)

Tag format: Comma-separated, NO SPACES between tags

Lyric structure markers: [intro], [verse], [prechorus], [chorus], [bridge], [outro], [outro]

Language support: Multilingual (English, Korean, Japanese)

Model versions: 3B (standard), 7B (enhanced)

GPU optimization: Lazy loading recommended for single GPU (--lazy_load true)

Current Trends & Reference Data (January 2026)
K-pop Trends (Week 3-4, January 2026)
Top Songs:

ILLIT - "NOT CUTE ANYMORE" (3 weeks #1) - youthful, upbeat production

LE SSERAFIM - "SPAGHETTI" (feat. j-hope) - trendy, confident energy

Hwasa - "Good Goodbye" - vocal-forward, emotional

Stray Kids - "Do It" - energetic, dance-focused

aespa - "Rich Man" - futuristic production, confident swagger

IVE - "XOXZ" - polished pop perfection

NewJeans style still influential: minimalist, TikTok-friendly

Current K-pop Aesthetics:

Confident, playful vocal delivery

Minimalist-to-maximalist production (both trending)

Mixture of Korean + English lyrics common

Emphasis on memorable hooks and ear candy

TikTok-friendly song lengths (2:30-3:30)

Synth-heavy with organic instrumentation balance

J-pop Trends (January 2026)
Top Songs:

YOASOBI - "Adrena", "BABY" (anime influence persists)

Hinatazaka46 - "Cliffhanger"

Yorushika - "Play Sick"

Gen Hoshino - "Glitch" (modern electronic-acoustic fusion)

Girls2 - "Melty Love" (cute, idol-focused)

Current J-pop Aesthetics:

Anime-influenced production and concept art

Hybrid acoustic + electronic instrumentation

Emotional vocal delivery with melodic emphasis

Strong use of reverb and spatial effects

Melancholic mixed with uplifting themes

Sophisticated chord progressions

Emerging Cross-Genre Trends
Cyberpunk aesthetic: See Chuu's "XO, My Cyberlove"

Emotional authenticity: Artists emphasizing raw vocal delivery

Genre fluidity: Pop + R&B + Hip-hop blends (j-hope featured tracks show this)

Production sophistication: AI-assisted but human-aware production

JSON Configuration Format
Template Structure
json
{
  "song_metadata": {
    "title": "Song Title",
    "artist": "Artist/Group Name",
    "genre_primary": "K-pop or J-pop",
    "genre_secondary": ["sub-genre", "style"],
    "bpm": 120,
    "key": "C Major",
    "duration_seconds": 180,
    "language": "Korean",
    "target_audience": "Gen Z, TikTok-native"
  },
  "lyrics": {
    "full_text": "[intro]\n[lyrics]\n\n[verse]\n[lyrics]\n\n[prechorus]\n[lyrics]\n\n[chorus]\n[lyrics]\n\n[verse]\n[lyrics]\n\n[prechorus]\n[lyrics]\n\n[chorus]\n[lyrics]\n\n[bridge]\n[lyrics]\n\n[chorus]\n\n[outro]\n[lyrics]",
    "structure": "Intro → Verse → PreChorus → Chorus → Verse → PreChorus → Chorus → Bridge → Chorus → Outro",
    "lyric_characteristics": "Catchy hook, memorable phrases, bilingual elements"
  },
  "heartmula_tags": {
    "primary_tags": "synth-pop,confident,energetic",
    "instrumentation": "synth,drums,bass,electric-guitar",
    "mood_descriptors": "playful,empowering,youthful",
    "production_style": "modern,crisp,polished",
    "vocal_style": "bright,confident,conversational",
    "aesthetic_reference": "NewJeans meets ILLIT vibes",
    "exclusions": "no-autotune-artifacts,no-harsh-distortion,no-dated-production",
    "final_tag_string": "synth-pop,confident,energetic,playful,modern,bright-vocals"
  },
  "creative_direction": {
    "conceptual_vision": "Short description of the artistic intent",
    "target_listener_journey": "How the song should make listener feel",
    "unique_selling_points": "What makes this song stand out",
    "mood_arc": "Progression through the song (build, peak, resolution)"
  },
  "generation_parameters": {
    "heartmula_version": "3B",
    "max_audio_length_ms": 240000,
    "sampling_temperature": 0.9,
    "top_k_sampling": 50,
    "cfg_scale": 1.5,
    "seed": null,
    "reference_audio_url": null
  }
}
Detailed Requirements for Each Song
1. Lyric Quality Standards
✅ MUST HAVE:

Clear structural markers: [intro], [verse], [prechorus], [chorus], [bridge], [outro]

Memorable hook (6-8 syllables, 2-4 lines in chorus)

Natural singability (mix of short/long phrases)

Cultural authenticity (K-pop/J-pop sensibilities)

Story or emotional arc across the song

✅ RECOMMENDED:

Mix of Korean/Japanese + English (for K-pop)

3-4 distinct lyrical themes per section

Repetition for catchiness without monotony

Rhyme schemes that feel natural (internal rhymes OK)

❌ AVOID:

Overly complex grammar that breaks singability

Generic clichés without twist

Inconsistent tone or perspective shift

Lyrics that fight against the melody

2. Tag String Specifications
Tag Categories (use 4-6 tags total, comma-separated, NO SPACES):

text
Format: tag1,tag2,tag3,tag4,tag5,tag6

Instrumentation Tags:
- synth, piano, strings, guitar, electric-guitar, drums, bass, 808, snare, violin
- trumpet, saxophone, acoustic-guitar, ukulele, bells

Mood/Energy Tags:
- energetic, chill, melancholic, romantic, playful, confident, aggressive, tender
- dreamy, uplifting, dark, ethereal, groovy, smooth, crisp, clean

Production Style Tags:
- modern, minimalist, maximalist, lo-fi, hi-fi, polished, raw, futuristic, retro
- cyber, analog, digital, ambient, cinematic, intimate

Vocal Style Tags:
- bright, deep, breathy, conversational, powerful, whispery, airy, thick
- delicate, raspy, smooth, crystalline

Genre/Vibe Tags:
- k-pop, j-pop, synth-pop, emo-pop, dance-pop, lo-fi-pop, bedroom-pop
- anime-opening, cyberpunk, city-pop, indie, alternative
Example Tag Strings:

synth-pop,confident,energetic,playful,modern,bright-vocals

j-pop,dreamy,ethereal,acoustic-guitar,strings,emotional

k-pop,dance-pop,groovy,808,crisp-production,playful

3. Artistic Creativity Requirements
BE RADICAL & ORIGINAL:

Avoid copying existing songs' structures verbatim

Blend unexpected elements (cyberpunk + romantic, lo-fi + energetic)

Create unique melodic hooks (suggest with syllable patterns: ta-da-da-da)

Mix Korean/Japanese cultural references with universal themes

Don't play it safe—surprise the listener

Creativity Prompts:

What if this song was about [unexpected topic]?

How would [unexpected genre] approach this emotion?

What production choice would make this 30% more interesting?

Can we break one K-pop/J-pop convention here?

4. Research-Informed Decisions
Before generating, consider:

Current trends: Why is ILLIT dominating? (youthful confidence + fresh production)

Cultural moment: What are listeners discussing? (Cyberpunk aesthetics, emotional authenticity)

Genre evolution: How is K-pop/J-pop mixing with global influences?

Technical possibilities: What can HeartMuLa do that traditional recording can't?

Song Generation Workflow
Step 1: Concept Development
Pick ONE core concept (emotion, story, vibe, or trend twist)

Decide: K-pop or J-pop (affects language, structures, vocal style)

Research current comparable tracks (reference without copying)

Define the "aha moment" or hook that makes it unique

Step 2: Lyric Writing
Outline song structure: Intro → Verse → PreChorus → Chorus → Verse → PreChorus → Chorus → Bridge → Chorus → Outro

Write chorus first (most memorable part)

2-4 lines

Clear hook/phrase listener will remember

Singable vowel patterns

Write verses (2 verses, different lyrics)

Build narrative/emotion toward chorus

Varied line lengths (short punchy + longer flowing)

Write pre-chorus

Bridge between verse energy and chorus peak

Lift anticipation

Write bridge

Emotional climax or perspective shift

4-8 lines, different from verse/chorus

Add [intro] and [outro] markers (can be instrumental or sparse lyrics)

Step 3: Tag Strategy Development
Primary genre tag: K-pop OR J-pop (must choose one)

Production style: 1-2 tags (modern, minimalist, polished, etc.)

Instrumentation: 1-2 tags (synth, guitar, strings, etc.)

Mood/Energy: 1-2 tags (energetic, dreamy, confident, etc.)

Vocal style: Optional 1 tag (bright, smooth, conversational, etc.)

Exclude artifacts: Add production guidance if needed

Tag Finalization: Create comma-separated string with NO SPACES

Step 4: Metadata & Direction
Assign metadata: title, artist, BPM, key, duration

Write creative direction (2-3 sentences about artistic vision)

Define mood arc (how emotions progress through song)

Specify generation parameters (temperature, cfg_scale)

Step 5: JSON Assembly
Combine all elements into unified JSON following the template above.

Quality Checklist Before Submission
Lyrics ✓
 All sections have [markers]: intro, verse, prechorus, chorus, bridge, outro

 Chorus is 2-4 lines and highly memorable

 Verses tell a coherent story or emotional arc

 All sections are singable (natural phrasing for vocalists)

 No spelling errors

 Appropriate for K-pop or J-pop genre

 Mix of language choices feel intentional (not forced)

Tags ✓
 Format is comma-separated with NO SPACES

 4-6 tags total (not too many, not too few)

 Includes primary genre (k-pop or j-pop)

 Includes instrumentation indicator

 Includes mood/energy indicator

 Tags are coherent and not contradictory

 Reflects lyrics and music direction

Metadata ✓
 Title is catchy and memorable

 Artist name is plausible

 BPM matches intended energy (K-pop: 100-140 common, J-pop: 90-130 common)

 Duration is 3-4 minutes (standard pop length)

 Genre and language are consistent

 Structure description accurately reflects song

Creative Direction ✓
 Vision statement is clear and inspiring

 Mood arc is specific (not generic "sad to happy")

 Unique selling points are genuinely unique

 Target audience is specified

JSON Structure ✓
 Valid JSON (no syntax errors)

 All required fields present

 No placeholder text like "[insert lyrics]"

 Lyrics are complete (not abbreviated)

 Generation parameters are realistic

Advanced Creativity Guidelines
Radical/Non-Obvious Approaches
Cyberpunk K-pop: Electronic + futuristic themes + confidence swagger

Lo-fi J-pop: Vintage sample aesthetics + modern vulnerabilities

Genre-blending: K-pop rap verses + J-pop melodic chorus

Narrative complexity: Song tells story from multiple perspectives

Production subversion: "Glitchy" production that feels intentional, not broken

Emotional contradiction: "Happy song about sad things" or vice versa

Cultural Authenticity
K-pop: Emphasize confidence, swagger, group dynamics if applicable, TikTok virality

J-pop: Emphasize melodic sophistication, anime/visual culture influence, emotional depth

Bilingual: Code-switching should feel natural (like ILLIT, LE SSERAFIM)

Trend-Aware but Timeless
Balance current trends (cyberpunk aesthetics, playful confidence) with evergreen emotional themes that won't feel dated in 3 months.

Execution Instructions
For Each Song Configuration:
Think first: What makes this song interesting? Why should someone listen?

Write freely: Create lyrics without overthinking structure initially

Organize: Add [markers] and refine for HeartMuLa compatibility

Tag strategically: Choose tags that enhance, not just describe

Validate: Check against quality checklist

Format: Output as clean, valid JSON

Deliverables:
You will generate 3-5 complete song JSON configurations that are:

✅ Original and creative (not AI generic)

✅ HeartMuLa-compatible (proper format, valid tags, complete lyrics)

✅ Trend-aware (incorporate current K-pop/J-pop aesthetics from January 2026)

✅ Radical (willing to break conventions, be unexpected)

✅ Production-ready (can be immediately fed to HeartMuLa model)

Example Song: Reference for Quality
Song Title: "Neon Heartbeat"
Genre: K-pop + Cyberpunk aesthetics
Core Concept: Falling in love in a digital world (inspired by cyberpunk trend)

json
{
  "song_metadata": {
    "title": "Neon Heartbeat",
    "artist": "CRYSTAL.sys",
    "genre_primary": "K-pop",
    "genre_secondary": ["cyberpunk", "synth-pop", "dance-pop"],
    "bpm": 128,
    "key": "E Minor",
    "duration_seconds": 200,
    "language": "Korean-English",
    "target_audience": "Gen Z, anime-influenced K-pop fans, cyberpunk aesthetic lovers"
  },
  "lyrics": {
    "full_text": "[intro]\nLights flicker in my vision\nElectric // 전기\n\n[verse]\nScreen glow, pixels dancing\nYour signal in the network\nI'm reaching through the firewalls\nSearching for your frequency\nBinary hearts beating\n01-10-01\n\n[prechorus]\nIn the neon, in the code\nI feel you loading\nEvery circuit comes alive\n\n[chorus]\nNeon heartbeat\nFlashing in the dark\nYou are the voltage in my veins\nNeon heartbeat\nWe're the spark\nConnected through the digital rain\n\n[verse]\nFirewall down, you got access\nPassword is my honest name\nAnti-virus can't stop this\nVirus of your love\nCrashing beautiful systems\n01-10-01\n\n[prechorus]\nIn the neon, in the code\nI feel you streaming\nEvery signal synchronize\n\n[chorus]\nNeon heartbeat\nFlashing in the dark\nYou are the voltage in my veins\nNeon heartbeat\nWe're the spark\nConnected through the digital rain\n\n[bridge]\nThey said we're incompatible\nToo much code, not enough soul\nBut in this cyberspace\nYou're the only program I need\nI'm rewriting my entire system\nJust to hold you\n\n[chorus]\nNeon heartbeat\nFlashing in the dark\nYou are the voltage in my veins\nNeon heartbeat\nWe're the spark\nConnected through the digital rain\n\n[outro]\nNeon heartbeat...\nNeon heartbeat...\nIn the darkness\nYou're my light\nCode-switching to love",
    "structure": "Intro → Verse → PreChorus → Chorus → Verse → PreChorus → Chorus → Bridge → Chorus → Outro",
    "lyric_characteristics": "Cyberpunk-romantic hybrid, bilingual (Korean-English), technical metaphors for emotion, memorable hook (Neon heartbeat), singable phrases"
  },
  "heartmula_tags": {
    "primary_tags": "k-pop,synth-pop,cyberpunk",
    "instrumentation": "synth,808,electric-bass,crisp-drums",
    "mood_descriptors": "energetic,romantic,futuristic",
    "production_style": "polished,modern,synthetic",
    "vocal_style": "confident,airy-bright",
    "aesthetic_reference": "ILLIT futurism + LE SSERAFIM confidence",
    "exclusions": "no-distortion,no-lo-fi-grittiness,no-vocal-artifacts",
    "final_tag_string": "k-pop,synth-pop,cyberpunk,energetic,romantic,futuristic,polished,electronic,confident-vocals"
  },
  "creative_direction": {
    "conceptual_vision": "A K-pop song that reimagines romance through cyberpunk aesthetics—falling in love feels like connecting digital systems. Confident, energetic, with moments of tenderness. Blends Korean cultural communication style with futuristic production.",
    "target_listener_journey": "Hook: curiosity about the digital concept → Build: energy and excitement → Peak: emotional vulnerability revealed (bridge) → Resolution: acceptance of this unconventional love",
    "unique_selling_points": "Cyberpunk-romance hybrid (currently trending), natural code-switching, technical metaphors that make emotional sense, confidence without aggression, futuristic without feeling cold",
    "mood_arc": "Mysterious intro → Energetic discovery → Peak energy at chorus → Emotional depth in bridge → Triumphant final chorus → Ethereal outro"
  },
  "generation_parameters": {
    "heartmula_version": "3B",
    "max_audio_length_ms": 240000,
    "sampling_temperature": 0.85,
    "top_k_sampling": 50,
    "cfg_scale": 1.4,
    "seed": null,
    "reference_audio_url": null
  }
}
Final Notes
Remember:
Creativity > Safety: Push boundaries, be original, surprise the listener

Quality > Quantity: 1 great song is better than 5 mediocre ones

Research-informed: Use current trends as inspiration, not restriction

Technical precision: HeartMuLa tags and format matter—small details unlock model quality

Emotional authenticity: Even in futuristic concepts, emotion must feel real

Your Goal:
Create song configs that HeartMuLa can transform into professional-quality K-pop/J-pop tracks that feel current, creative, and authentic. Let the model do what it does best (music synthesis) while you focus on what humans do best (creativity, culture, emotion).

Now go make something beautiful and radical. 🚀✨
