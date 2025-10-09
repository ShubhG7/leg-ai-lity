# Split-Screen Interface Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          LEXSY AI - FILL YOUR DOCUMENT                      │
│              Complete fields on the left, get AI assistance on the right    │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ PROGRESS: ████████████░░░░░░░░░░░░ 8 of 15 fields completed                │
└─────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────┬────────────────────────────────────────┐
│          🎯 FILL FIELDS            │         💬 CHAT WITH LEXSY             │
│        (Left Panel)                │          (Right Panel)                 │
├────────────────────────────────────┼────────────────────────────────────────┤
│                                    │                                        │
│  ┌────────────────────────────┐   │  ┌──────────────────────────────────┐ │
│  │ Current Field:              │   │  │ 🤖 This is a Simple Agreement   │ │
│  │ VALUATION CAP               │   │  │    for Future Equity (SAFE)...  │ │
│  │ Field 9 of 15               │   │  └──────────────────────────────────┘ │
│  └────────────────────────────┘   │                                        │
│                                    │  ┌──────────────────────────────────┐ │
│  ┌────────────────────────────┐   │  │ 🤖 Great! I see you need to fill│ │
│  │ [🔍 Explain this field]     │   │  │    15 fields. I'll guide you... │ │
│  │ [💡 Give example]           │   │  └──────────────────────────────────┘ │
│  └────────────────────────────┘   │                                        │
│                                    │           👤 What does valuation      │
│  ┌────────────────────────────┐   │              cap mean?                 │
│  │ Enter Valuation Cap...      │   │                                        │
│  │ $ [________________]        │   │  ┌──────────────────────────────────┐ │
│  └────────────────────────────┘   │  │ 🤖 The Valuation Cap is the     │ │
│                                    │  │    maximum company valuation... │ │
│  [← Prev] [Save & Continue] [Skip→]│  └──────────────────────────────────┘ │
│                                    │                                        │
│  ─────────────────────────────     │  ┌──────────────────────────────────┐ │
│  All Fields:                       │  │ Ask me anything...  [Send 📤]   │ │
│                                    │  └──────────────────────────────────┘ │
│  ✅ Investor Name     "Jane Doe"   │                                        │
│  ✅ Investment Amount "$100,000"   │  Currently working on:                 │
│  ✅ Date              "2024-01-15" │  💠 Valuation Cap                      │
│  ✅ Company Name      "Acme Inc"   │                                        │
│  ✅ State             "Delaware"   │                                        │
│  ✅ Address           "123 Main"   │                                        │
│  ✅ Email             "jane@..."   │                                        │
│  ✅ Phone             "+1-555..."  │                                        │
│  🔵 Valuation Cap     [ACTIVE]     │                                        │
│  ⚪ Discount Rate                  │                                        │
│  ⚪ Closing Date                    │                                        │
│  ⚪ Governing Law                   │                                        │
│  ⚪ Notice Address                  │                                        │
│  ⚪ Investor Signature              │                                        │
│  ⚪ Company Signature               │                                        │
│                                    │                                        │
└────────────────────────────────────┴────────────────────────────────────────┘
```

## Key Elements

### Left Panel - Field Filling
1. **Current Field Card**
   - Shows field name prominently
   - Displays progress (e.g., "Field 9 of 15")
   
2. **Quick Action Buttons**
   - 🔍 **Explain this field** → AI explains legal meaning
   - 💡 **Give example** → AI provides realistic example
   
3. **Input Field**
   - Large, focused input for current value
   - Placeholder text guides user
   
4. **Navigation Controls**
   - ← Previous (go to previous unfilled field)
   - Save & Continue (save and advance)
   - Skip → (skip this field, come back later)
   
5. **All Fields Overview**
   - ✅ Green = Completed (shows saved value)
   - 🔵 Blue = Current/Active (highlighted)
   - ⚪ Gray = Pending (not yet filled)
   - Click any field to jump to it

### Right Panel - AI Chat
1. **Message History**
   - 🤖 Bot messages (purple avatar, gray bubble)
   - 👤 User messages (blue avatar, blue bubble)
   - Auto-scrolls to latest message
   
2. **Document Analysis**
   - Shown at the start
   - Explains document type and purpose
   
3. **Conversational Q&A**
   - Ask anything about the document
   - Get field-specific guidance
   - Context-aware responses
   
4. **Chat Input**
   - Type questions freely
   - Send button to submit
   
5. **Current Field Indicator**
   - Shows which field you're working on
   - Helps AI provide relevant context

## User Flow

```
1. UPLOAD DOCUMENT
   ↓
2. VIEW DOCUMENT ANALYSIS (in chat)
   ↓
3. START WITH FIRST FIELD
   │
   ├─→ Click "Explain" → Read explanation in chat
   │
   ├─→ Click "Example" → See realistic example
   │
   ├─→ Ask question in chat → Get AI answer
   │
   └─→ Enter value → Click "Save & Continue"
   ↓
4. REPEAT FOR ALL FIELDS
   │
   ├─→ Jump to specific fields (click in list)
   │
   ├─→ Skip fields (come back later)
   │
   └─→ Navigate back/forward
   ↓
5. ALL FIELDS COMPLETE ✅
   ↓
6. GENERATE & DOWNLOAD DOCUMENT
```

## Example Interactions

### Scenario 1: User Clicks "Explain this field"
```
USER ACTION: Clicks [🔍 Explain this field]
           ↓
CHAT SHOWS: "Can you explain what 'Valuation Cap' means?"
           ↓
AI RESPONDS: "The Valuation Cap is the maximum company valuation 
             at which your investment will convert to equity. It 
             protects investors by ensuring they get a minimum 
             ownership percentage..."
```

### Scenario 2: User Clicks "Give example"
```
USER ACTION: Clicks [💡 Give example]
           ↓
CHAT SHOWS: "Can you give me an example for 'Valuation Cap'?"
           ↓
AI RESPONDS: "For a Valuation Cap, you might enter:
             - $5,000,000 (early-stage startups)
             - $10,000,000 (established companies)
             - $15,000,000 (high-growth startups)
             
             A typical SAFE agreement might use: $8,000,000"
```

### Scenario 3: User Asks Custom Question
```
USER TYPES: "Is an $8M cap reasonable for a seed stage startup?"
           ↓
AI RESPONDS: "An $8M valuation cap is quite reasonable for a seed 
             stage startup, especially if you're in a competitive 
             market or have shown strong early traction. Here's 
             why..."
```

## Benefits

### ✅ No Context Switching
- Fill fields AND ask questions simultaneously
- No need to toggle between modes

### ✅ Instant Help
- Preset buttons = one-click explanations
- No typing required for common questions

### ✅ Visual Progress
- See all fields at a glance
- Know exactly what's left

### ✅ Flexible Navigation
- Jump to any field
- Go back to edit
- Skip and return later

### ✅ Educational
- Learn legal concepts while filling
- Understand each field's purpose
- Get examples for clarity

## Mobile Responsive

### Desktop (≥1024px)
```
┌────────────────────────────────────────────┐
│  [Field Filling]  │  [AI Chat]             │
│                   │                        │
│  Side by side     │  Always visible        │
└────────────────────────────────────────────┘
```

### Tablet/Mobile (<1024px)
```
┌──────────────────────────┐
│  [Field Filling]         │
│                          │
│  Stacked on top          │
├──────────────────────────┤
│  [AI Chat]               │
│                          │
│  Scrollable below        │
└──────────────────────────┘
```

---

**This interface makes complex legal documents accessible, educational, and easy to complete!** 🚀

