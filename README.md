# AI Project Memory Universal v1.1

ระบบ Project Memory (ความจำโปรเจ็กต์) แบบใช้ร่วมกันสำหรับ **Codex + Claude Code**

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
- Claude Code Bash: ตรวจ pattern เขียนไฟล์ (`>`, `>>`, `cp`, `mv`, `tee`, `touch`, `sed -i`)
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

## ติดตั้งใน Project ใหม่

1. แตกไฟล์ทั้งหมดลง **root ของ Project**
2. แก้ `.ai/state.md` ให้ตรงกับสถานะจริง
3. แก้ `.ai/plan.md` ให้ตรงกับ Goal/Phase/Tasks จริง
4. แก้ `.ai/decisions.md` เฉพาะ Decision สำคัญ
5. ตรวจ Python:

```powershell
python --version
```

6. ตรวจ Memory:

```powershell
python scripts/validate_memory.py
```

ต้องได้:

```text
MEMORY VALIDATION PASSED
```

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

Bash pattern เป็น regex แบบ best-effort ไม่ใช่ shell parser จริง จุดที่ยังพลาดได้:
- คำสั่งเขียนไฟล์ผ่านตัวแปร/subshell ที่ regex จับปลายทางไม่ได้ (เช่น `$OUT > $(f)`)
- PowerShell หรือ external tool อื่นที่ไม่ผ่าน Bash tool ของ Claude Code
- คำสั่งเขียนไฟล์แบบ custom ที่ไม่อยู่ใน pattern list (นอกเหนือ `>`, `>>`, `cp`, `mv`, `tee`, `touch`, `sed -i`)

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
