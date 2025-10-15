# Scheduling Alternatives for Tutoring Website

## 🗓️ **Easy Scheduling Solutions**

### **Option 1: Calendly (Recommended)**
**Setup Steps:**
1. Sign up at [calendly.com](https://calendly.com) (free plan available)
2. Create an event type called "Tutoring Session" 
3. Set your availability (days/times you're available)
4. Configure session length (30min, 1hr, etc.)
5. Add buffer times between sessions
6. Get your Calendly link
7. Replace `your-calendly-username` in tutoring.html with your actual username

**Benefits:**
- ✅ Free plan available
- ✅ Automatic time zone conversion
- ✅ Email confirmations and reminders
- ✅ Google Calendar sync
- ✅ Professional appearance
- ✅ Easy reschedule/cancel options

### **Option 2: Acuity Scheduling**
Similar to Calendly but with more customization options.
- Replace Calendly script with Acuity's embed code
- More advanced features but steeper learning curve

### **Option 3: Simple Time Slot Selection (No External Service)**

Here's a basic time slot picker that works without external services:

```html
<!-- Replace the Calendly section with this -->
<div class="time-slots-section">
    <h4>📅 Select Your Preferred Time</h4>
    <p>Choose your preferred time slot. I'll confirm availability within 24 hours.</p>
    
    <div class="grid">
        <div>
            <label for="preferred_date">Preferred Date</label>
            <input type="date" id="preferred_date" name="preferred_date" min="" required>
        </div>
        <div>
            <label for="preferred_time">Preferred Time</label>
            <select id="preferred_time" name="preferred_time" required>
                <option value="">Select time</option>
                <option value="9:00 AM">9:00 AM</option>
                <option value="10:00 AM">10:00 AM</option>
                <option value="11:00 AM">11:00 AM</option>
                <option value="2:00 PM">2:00 PM</option>
                <option value="3:00 PM">3:00 PM</option>
                <option value="4:00 PM">4:00 PM</option>
                <option value="6:00 PM">6:00 PM</option>
                <option value="7:00 PM">7:00 PM</option>
            </select>
        </div>
    </div>
</div>

<script>
// Set minimum date to today
document.getElementById('preferred_date').min = new Date().toISOString().split('T')[0];
</script>
```

### **Option 4: WhatsApp Scheduling**
Simple link that opens WhatsApp with pre-filled message:

```html
<a href="https://wa.me/1234567890?text=Hi%20Michael,%20I'd%20like%20to%20schedule%20a%20tutoring%20session.%20My%20preferred%20subject%20is%20___%20and%20I'm%20available%20___" 
   target="_blank" 
   role="button">
   📱 Schedule via WhatsApp
</a>
```

### **Option 5: Email Template Scheduler**
Enhanced mailto with pre-filled scheduling information:

```html
<a href="mailto:michael.sm.cho@email.com?subject=Tutoring%20Session%20Request&body=Hi%20Michael,%0D%0A%0D%0AI'd%20like%20to%20schedule%20a%20tutoring%20session.%0D%0A%0D%0AStudent%20Name:%20%0D%0ASubject%20Area:%20%0D%0AExperience%20Level:%20%0D%0APackage%20Preference:%20%0D%0APreferred%20Date/Time:%20%0D%0ATime%20Zone:%20%0D%0A%0D%0AAdditional%20Notes:%20%0D%0A%0D%0AThank%20you!" 
   role="button">
   📧 Schedule via Email
</a>
```

## 🔧 **Implementation Instructions**

### **For Calendly (Easiest):**
1. Create Calendly account
2. Set up "Tutoring Session" event type
3. Copy your Calendly link
4. Replace `your-calendly-username` in the tutoring.html file
5. Test the booking process

### **For Simple Time Slots:**
1. Replace the Calendly section in tutoring.html
2. Add the time slots HTML above
3. Customize available times to match your schedule
4. Students select times, you confirm via email

### **For WhatsApp:**
1. Replace `1234567890` with your WhatsApp number (with country code)
2. Customize the pre-filled message
3. Add the WhatsApp button to your scheduling section

## 📱 **Mobile-Friendly Options**

All solutions work well on mobile devices. Calendly is particularly good for mobile users as it has responsive design and native app integration.

## 💰 **Cost Comparison**

- **Calendly Free:** Up to 1 event type, basic features
- **Calendly Paid:** $8-12/month for multiple event types, integrations
- **Simple Time Slots:** Free, but manual confirmation required
- **WhatsApp/Email:** Free, but less professional appearance

## 🎯 **Recommendation**

**Start with Calendly's free plan** - it's the most professional and user-friendly option. If you need more features later, you can upgrade or switch to alternatives.

The current tutoring.html is set up for Calendly - just replace the username and you're ready to go!