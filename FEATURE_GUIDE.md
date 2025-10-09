# 🎯 Split-Screen Interface Guide

## New Feature: Enhanced Document Filling Experience

### Overview
The new split-screen interface provides a **dual-panel experience** where users can:
1. **Fill fields systematically** on the left
2. **Chat with AI assistant** on the right

---

## 📍 Left Panel: Field Filling

### Current Field Section
- **Large, focused input** for the current field
- **Field name** prominently displayed
- **Progress indicator** (e.g., "Field 3 of 15")

### Quick Action Buttons (Preset Prompts)
Two powerful buttons that trigger AI responses **automatically**:

#### 🔍 **"Explain this field"**
- **What it does**: AI explains the legal meaning of the current field
- **Example response**: 
  ```
  "The 'Valuation Cap' is the maximum company valuation at which your 
  investment will convert to equity. It protects investors by ensuring 
  they get a minimum ownership percentage, even if the company's value 
  increases significantly before the next funding round."
  ```

#### 💡 **"Give example"**
- **What it does**: AI provides a realistic example
- **Example response**: 
  ```
  "For a 'Valuation Cap', you might enter something like:
  - $5,000,000 (for early-stage startups)
  - $10,000,000 (for more established companies)
  - $15,000,000 (for high-growth startups)
  
  A typical SAFE agreement might use: $8,000,000"
  ```

### Navigation Controls
- **Previous** ← Go back to previous unfilled field
- **Save & Continue** → Save value and move to next field
- **Skip** → Skip this field and come back later

### Field Overview List
- **Completed fields** (✅ Green) - Shows saved value
- **Current field** (🔵 Blue) - Highlighted with blue border
- **Pending fields** (⚪ Gray) - Not yet filled
- **Click any field** to jump to it

---

## 💬 Right Panel: AI Chat

### Features
- **Always-active conversation** with Lexsy AI
- **Document analysis** shown at start
- **Ask anything**:
  - "What does 'Post-Money Valuation' mean?"
  - "Is a $10M cap too high for a seed round?"
  - "Can you explain the difference between SAFE and convertible note?"
- **Context-aware**: AI knows which field you're working on
- **Auto-scrolling**: Always see the latest message

### Message Types
- **Bot messages** (Purple avatar, gray background)
- **User messages** (Blue avatar, blue background)
- **Timestamps** on all messages

---

## 🎨 Visual Design

### Color Coding
- **Blue** = Current/Active state
- **Green** = Completed
- **Purple** = AI/Bot
- **Gray** = Pending/Neutral

### Progress Bar
- Shows **overall completion** percentage
- Updates in real-time as you fill fields

### Gradient Headers
- Left panel: Blue → Purple gradient
- Right panel: Purple → Blue gradient
- Creates visual harmony and separation

---

## 🚀 How to Use

### Basic Workflow
1. **Upload document** → Fields are extracted
2. **Read document analysis** in chat
3. **Start with first field**:
   - Click "Explain" to understand it
   - Click "Example" to see a sample value
   - Type your value and click "Save & Continue"
4. **Repeat** for all fields
5. **Ask questions** in chat anytime
6. **Generate document** when complete

### Advanced Tips
- **Jump around**: Click any unfilled field to work on it
- **Skip fields**: Use "Skip" to come back later
- **Get help anytime**: Chat is always available
- **Use presets**: Faster than typing questions

---

## 🎯 User Benefits

### For First-Time Users
- **"Explain this field"** teaches legal concepts
- **"Give example"** shows what to enter
- **No guessing** required

### For Experienced Users
- **Quick navigation** between fields
- **Visual progress** tracking
- **Skip routine fields**, focus on complex ones

### For Everyone
- **Conversational AI** makes complex docs approachable
- **Split-screen** = fill fields AND get help simultaneously
- **No context switching** between filling and asking questions

---

## 💡 Example User Journey

1. **Upload** "SAFE Agreement" document
2. **Chat shows**: "This is a Simple Agreement for Future Equity (SAFE)..."
3. **First field**: "Investor Name"
   - User clicks **"Give example"**
   - AI: "Enter the full legal name, like: 'John Smith' or 'Acme Ventures LLC'"
   - User types: "Jane Doe"
   - Clicks **"Save & Continue"**
4. **Second field**: "Valuation Cap"
   - User clicks **"Explain this field"**
   - AI explains concept in simple terms
   - User asks in chat: "Is $8M reasonable for a seed stage startup?"
   - AI provides guidance
   - User enters: "$8,000,000"
5. **Process continues** until all fields complete
6. **Generate document** → Done! ✅

---

## 🔧 Technical Implementation

### Components
- **SplitScreenChat.tsx** - Main component
- **Left panel**: Field form + navigation
- **Right panel**: Conversational chat
- **Backend**: Gemini AI for explanations and examples

### API Integration
- Same `/chat/conversational` endpoint
- Context includes:
  - Current field being filled
  - Document text
  - Conversation history
  - All placeholders and filled values

### Responsive Design
- **Desktop (lg+)**: Side-by-side panels
- **Mobile**: Stacked (field form on top, chat below)
- **Sticky positioning** for field panel on desktop

---

## 🎊 Success Metrics

This interface aims to:
- ✅ **Reduce time** to fill documents
- ✅ **Increase confidence** in legal understanding
- ✅ **Eliminate errors** through AI guidance
- ✅ **Improve user satisfaction** with conversational UX
- ✅ **Make legal docs accessible** to non-lawyers

---

**Happy document filling! 🚀**

