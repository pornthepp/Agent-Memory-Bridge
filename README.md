# Agent Memory Bridge

ระบบ Project Memory (ความจำโปรเจ็กต์) แบบใช้ร่วมกันสำหรับ **Codex + Claude Code**
(เดิมชื่อ AI Project Memory Universal v1.1 — core เดียวกัน แค่เปลี่ยนชื่อโปรเจ็ค)

## แนวคิด

ทั้งสอง Agent ใช้ Memory Core ชุดเดียว:

```text
Codex --------┐
              ├── .ai/state.md
Claude Code --┤   .ai/plan.md
              └── .ai/decisions.md
```

`AGENTS.md` และ `CLAUDE.md` เป็นเพียง Guidance (คำแนะนำรูปแบบการทำงาน)
ส่วนการโหลด/ตรวจ/บังคับ Checkpoint ใช้ Runtime Hooks จริง

## โครงสร้าง

```text
project/
├── .ai/
│   ├── state.md
│   ├── plan.md
│   └── decisions.md
│
├── .codex/
│   └── hooks.json
│
├── .claude/
│   └── settings.json
│
├── scripts/
│   ├── memory_common.py
│   ├── session_start.py
│   ├── track_changes.py
│   ├── checkpoint_guard.py
│   ├── precompact_guard.py
│   └── validate_memory.py
│
├── AGENTS.md
├── CLAUDE.md
├── .gitignore
└── README.md
```

## สิ่งที่ระบบทำ

### SessionStart
เปิด/Resume/Clear/Compact แล้วโหลด:
- `state.md`
- `plan.md`
- `decisions.md`
- recovery notice ถ้ามี

Claude Code รองรับ `startup`, `resume`, `clear`, `compact`, `fork`
ส่วน Codex ใช้ matcher ที่รองรับใน adapter ของ Codex

### Project change detection
- Codex: ตรวจ `apply_patch`
- Claude Code: ตรวจ `Write`, `Edit`, `NotebookEdit`
- Claude Code Bash: ตรวจแบบ 3 ชั้น (ดูเหตุผลแต่ละชั้นในหัวข้อ "ข้อจำกัด v1.1" /
  `.ai/decisions.md` D-005)
  1. **ตัด heredoc body ออกก่อน** (`strip_heredocs()`) — แบบ quote-aware คือรู้ว่า
     `<<'EOF'` ที่อยู่ใน quote (เช่นข้อความ commit message) ไม่ใช่ heredoc จริง
  2. **tokenize ด้วย `shlex.split()`** แทน regex scan string ดิบ — ข้อความใน quote
     กลายเป็น token เดียว ไม่มีทางถูกอ่านเป็น shell syntax ผิดๆ แล้วหา pattern เขียนไฟล์
     (`>`, `>>`, `cp`, `mv`, `tee`, `touch`, `sed -i`) จาก token ที่ได้
  3. **skip การสแกนทั้งหมดสำหรับ git subcommand ที่ไม่มีทางเขียนไฟล์ project**
     (`status`, `log`, `diff`, `show`, `branch`, `tag`, `remote`, `config`, `blame`,
     `reflog`, `fetch`, `add`, `commit`, `push`) — commit message ยาวๆ จะได้ไม่ถูกสแกนเลย
  ส่วนคำสั่งที่ระบุไฟล์ปลายทางไม่ได้ตรงๆ (`git apply`, `patch`, `rsync -a`, `npm/pip install`)
  จะ fallback เป็น dirty ทันทีแบบไม่เจาะจงไฟล์
- เมื่อไฟล์ Project เปลี่ยน จะสร้าง `.ai/.dirty`
- การแก้ไฟล์ภายใน `.ai/` ไม่สร้าง dirty ใหม่ (ยกเว้น fallback ด้านบน ซึ่งไม่เช็คปลายทาง)

### Stop checkpoint
ถ้ามี `.dirty`:
1. ตรวจว่า `state.md` ใหม่กว่าการเปลี่ยน Project
2. ตรวจว่า `plan.md` ใหม่กว่าการเปลี่ยน Project
3. รัน `validate_memory.py`
4. ถ้าไม่ผ่าน ให้ Agent ทำต่อ
5. Validation ผิดได้สูงสุด 2 รอบก่อนปล่อย Turn และคง `.dirty` ไว้สำหรับตรวจเอง

### PreCompact recovery
ถ้า Context กำลัง Compact ขณะที่ `.dirty` ยังอยู่:
- สร้าง `.ai/precompact-recovery.md`
- หลัง Compact, SessionStart จะโหลด recovery กลับเข้า Context
- Stop checkpoint จะบังคับ reconcile Memory ก่อนจบงาน

### Manual checkpoint (ไม่ต้องรอ hook)

สั่งบันทึกความจำเองได้ทุกเมื่อ ไม่ต้องรอจบ Turn — บอก agent ว่า:

```text
บันทึกความจำตอนนี้เลย ทำตามขั้นตอนใน .ai/CHECKPOINT.md
```

ไฟล์ `.ai/CHECKPOINT.md` เป็น runbook บอกขั้นตอนบันทึกแบบเป็นขั้นเป็นตอน (เช็คว่าเปลี่ยน
อะไรไปบ้าง → อัพเดท state/plan → validate → commit) ใช้ได้กับ agent ไหนก็ได้ที่อ่านไฟล์
ได้ — มีประโยชน์เป็นพิเศษกับ agent ที่ไม่มี Stop hook (เช่น Antigravity ดู "ข้อจำกัด v1.1")

ถ้าใช้ Claude Code พิมพ์ `/checkpoint` ได้เลย (มี slash command ให้แล้วที่
`.claude/commands/checkpoint.md`)

## ติดตั้งใน Project ใหม่

1. แตกไฟล์ทั้งหมดลง **root ของ Project**
2. ตรวจ Python:

```powershell
python --version
```

3. เปิด Claude Code หรือ Codex จาก root ของ Project แล้วสั่งให้ AI กรอกความจำเอง
   (ไม่ต้องแก้ `.ai/*.md` ด้วยมือ) — เลือก prompt ตามสถานการณ์:

**กรณี A — โปรเจ็คว่าง ยังไม่เริ่มงาน:**

```text
เริ่ม project memory ของโปรเจ็คนี้ ตอนนี้ยังว่างอยู่ ไม่มีโค้ด ให้ตั้ง .ai/state.md
และ .ai/plan.md เป็นค่าเริ่มต้นที่สื่อว่ายังอยู่ช่วงเริ่มต้น ยังไม่มี Goal ที่ชัดเจน
แล้วถามฉันว่าเป้าหมายโปรเจ็คคืออะไร ก่อนกรอกอะไรที่เดาเอง
```

**กรณี B — โปรเจ็คเริ่มมาแล้ว มีโค้ด/ประวัติงานอยู่ก่อน:**

```text
เริ่ม project memory ของโปรเจ็คนี้ อ่านโค้ด, README, git log (ถ้ามี) ให้ทั่วก่อน แล้วสรุป
สถานะจริงลง .ai/state.md, เป้าหมาย/milestone ที่เห็นได้จริงลง .ai/plan.md ห้ามเดาสิ่งที่
ไม่มีหลักฐาน ถ้าข้อมูลไม่พอต้องสรุป Goal หรือ Phase ให้ถามฉันก่อน อย่ากรอกมั่ว
```

4. ตรวจ Memory:

```powershell
python scripts/validate_memory.py
```

ต้องได้:

```text
MEMORY VALIDATION PASSED
```

`.ai/decisions.md` ไม่ต้องกรอกตอนติดตั้ง ปล่อยว่างไว้ก่อน — เก็บเฉพาะ Decision สำคัญที่เกิดขึ้นจริงระหว่างทำงาน (ดูหัวข้อ Memory Format ด้านล่าง)

## ใช้กับ Codex

เปิด Codex จาก Project root:

```powershell
codex
```

ตรวจ Hook ด้วย `/hooks`

## ใช้กับ Claude Code

เปิด Claude Code จาก Project root:

```powershell
claude
```

Project hooks อยู่ที่:

```text
.claude/settings.json
```

ตรวจ Hook ด้วย:

```text
/hooks
```

ถ้า Project มี `.claude/settings.json` อยู่แล้ว **อย่า overwrite แบบไม่ตรวจ**
ให้ merge เฉพาะ key `hooks` เข้ากับ settings เดิม

## Memory Format

### state.md
เก็บ "ความจริงปัจจุบัน" เท่านั้น:
- Current Phase
- Current Status
- In Progress
- Current Issues
- Last Completed
- Next Action

### plan.md
เก็บ Direction (ทิศทาง) และงานระดับ Milestone:
- Goal
- Current Phase
- Completed Milestones
- Current Tasks
- Next Milestone

อย่าเก็บทุกการแก้เล็ก ๆ เป็น permanent history

### decisions.md
Decision Log (บันทึกการตัดสินใจ):
- เก็บ Decision สำคัญ
- เก็บเหตุผล
- ไม่แก้ย้อนหลังโดยไม่มีเหตุผล
- ถ้า Decision เก่าถูกแทนที่ ให้บันทึก Decision ใหม่ว่า supersedes ตัวใด

## Memory size

Claude Code จำกัด Hook output ประมาณ 10,000 characters
ดังนั้น Validator v1.1 จำกัด Memory ที่ Inject ทุก Session ไว้ค่อนข้างเล็ก:

- `state.md` ≤ 3,500 chars
- `plan.md` ≤ 3,500 chars
- `decisions.md` ≤ 2,500 chars
- รวม ≤ 8,500 chars

ถ้า Decision โตมาก ควรทำ Archive แยก และเก็บเฉพาะ Decision ที่ยัง relevant ในไฟล์ที่ Inject ทุก Session

## Runtime files

ระบบสร้างและลบเอง:

```text
.ai/.dirty
.ai/.checkpoint-retry
.ai/precompact-recovery.md
```

ห้าม Agent ลบเองเพื่อ bypass Checkpoint

## ข้อจำกัด v1.1

Change Detection จับเครื่องมือแก้ไฟล์หลัก (`Write`, `Edit`, `NotebookEdit`, Codex `apply_patch`)
และ pattern เขียนไฟล์ที่พบบ่อยใน Claude Code `Bash` (ดูหัวข้อ Project change detection ด้านบน)

Bash detection ผ่านการแก้บั๊กจริงมาแล้ว 2 รอบ ระหว่างพัฒนา (ดู `.ai/decisions.md` D-005
สำหรับรายละเอียดเต็ม):
1. regex ล้วนๆ อ่าน `->` ใน commit message ผิดเป็น redirect → แก้ด้วย lookbehind
2. lookbehind นั้นไม่พอ — `>` เดี่ยวๆ ในประโยคอื่นก็ยังอ่านผิดอีก → รากปัญหาจริงคือ regex
   scan string ดิบ แยกไม่ออกว่าข้อความไหนอยู่ใน quote → **แก้ด้วยการเปลี่ยนมาใช้
   `shlex.split()` tokenize ก่อน** ข้อความใน quote จะกลายเป็น token เดียว ไม่มีทางถูก
   ตีความเป็น shell syntax ผิดๆ อีก

นอกจากนี้มีการเสริมความแข็งแรงเพิ่มอีก 2 จุด (เป็นการป้องกันเชิงรุก ไม่ใช่บั๊กที่ยืนยันว่า
เกิดจริง — อ่านทั้งเรื่องได้ใน D-005):
- `strip_heredocs()` แบบ quote-aware: ตัด heredoc body ออกก่อน tokenize เพราะ shlex ไม่มี
  concept เรื่อง heredoc เลย ถ้าไม่ตัดออกก่อน ข้อความในนั้นอาจไปรบกวนการ tokenize ส่วนอื่น
- skip การสแกนทั้งหมดสำหรับ git subcommand ที่ไม่มีทางเขียนไฟล์ project (`add`, `commit`,
  `push`, `status` ฯลฯ) เพราะ commit message เป็นจุดที่เสี่ยงสุด (เป็น prose ยาวๆ ที่มักพูด
  ถึง code/syntax ตรงๆ) และ subcommand พวกนี้ไม่มีทางเขียนไฟล์ project อยู่แล้วไม่ว่าข้อความ
  จะเป็นอะไร

ยังไม่ใช่ shell parser เต็มรูปแบบ จุดที่ยังพลาดได้:
- คำสั่งเขียนไฟล์ผ่านตัวแปร/subshell ที่ tokenizer จับปลายทางไม่ได้ (เช่น `$OUT > $(f)`)
- PowerShell หรือ external tool อื่นที่ไม่ผ่าน Bash tool ของ Claude Code
- คำสั่งเขียนไฟล์แบบ custom ที่ไม่อยู่ใน pattern list (นอกเหนือ `>`, `>>`, `cp`, `mv`, `tee`, `touch`, `sed -i`)
- git subcommand อื่นที่ไม่อยู่ใน safe-list (เช่น `merge`, `pull`, `rebase`) ยังถูกสแกนตามปกติ
  ด้วย pattern เดิม — ยังไม่ได้แยกว่าคำสั่งพวกนี้เขียนไฟล์แบบกว้างๆ ได้เหมือนกัน

จุดนี้ยังควรพัฒนาต่อเป็น v2 ด้วย Git diff / file watcher / repository snapshot เพื่อความแม่นยำเต็มรูปแบบ

## ใช้คู่กับ Git (ส่งงานต่อข้าม Agent / ข้ามวัน)

`.ai/state.md`, `.ai/plan.md`, `.ai/decisions.md` **ไม่ได้ถูก ignore** — git track ปกติ
(ดู `.gitignore`, ที่ ignore มีแค่ไฟล์ runtime อย่าง `.ai/.dirty`)

แต่ระบบ**ไม่ได้บังคับ**ให้ commit ไฟล์ความจำเข้า git อัตโนมัติ — Stop hook บังคับแค่
"อัพเดทไฟล์ให้ตรงความจริง" ไม่ได้บังคับ "commit/push" ถ้าลืม commit ไฟล์ `.ai/` พร้อมโค้ด
Agent ตัวถัดไป (คนละเครื่อง คนละวัน หรือคนละ Agent) จะ pull ได้แค่โค้ด ไม่ได้ความจำล่าสุด
ทำให้ระบบ hook ทั้งชุดไม่มีประโยชน์ในจุดต่อคนพอดี

**กฎที่ต้องทำเอง** (เขียนไว้ใน `AGENTS.md`/`CLAUDE.md` แล้ว):
ก่อนจบเซสชั่นหรือ push ให้ commit `.ai/state.md`, `.ai/plan.md`, `.ai/decisions.md`
พร้อมกับโค้ดที่มันอธิบายเสมอ อย่าปล่อยแยกกัน

## หมายเหตุ Claude Code

Claude Code `Stop` Hook มี protection (การป้องกัน) ไม่ให้ block ต่อเนื่องไม่รู้จบ และมี cap ภายในของ Claude Code
ระบบนี้จึงใช้ Validation retry เพียง 2 รอบ

`PreCompact` ของ Claude Code ไม่ได้ใช้ systemMessage เพื่อ Inject context หลังย่อโดยตรง
ตัว recovery จึงถูกเก็บเป็นไฟล์ แล้ว `SessionStart(source=compact)` โหลดกลับเข้ามาแทน
