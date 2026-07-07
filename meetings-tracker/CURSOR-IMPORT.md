# Import Meetings from Cursor

To pull your real Teams meetings into Meeting Hub, use Cursor with the Teams MCP:

## Prompt to use in Cursor Chat

```
Get my Teams meetings for the next 14 days using the teams_get_meetings tool. 
Return the result as a JSON array that I can copy and paste into Meeting Hub. 
Each meeting should include: subject, startTime, endTime, organizer (with name and email), 
attendees (array of {name, email} if available), joinUrl, and location.
```

Cursor will call the Teams MCP and return the data. Copy the JSON array from the response, then in Meeting Hub:

1. Click **Import from Teams**
2. Paste the JSON
3. Click **Import JSON**

---

**Note:** The Teams MCP returns `organizer` and may not include `attendees` in all cases. Meeting Hub will still work; the "large meeting" badge and notifications rely on attendee count when available.
