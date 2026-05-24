# Gemini API Configuration Guide

## Overview

InsightIQ uses Google's Gemini AI API to generate advanced business insights and power the AI chat interface. The system gracefully falls back to local analytics if the Gemini API is not configured, but for full functionality, you'll need to set up the API key.

## Local Analytics Fallback

Even without Gemini configured, the system provides actionable insights based on the data:

- **Profitable Regions**: Identifies top-performing regions by profit
- **Discount Impact**: Analyzes correlation between discounts and profitability
- **Loss-Making Products**: Highlights products requiring pricing review
- **Category Performance**: Shows highest-performing product categories

## Steps to Configure Gemini API

### 1. Get Your API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account (create one if needed - it's free)
3. Click **"Create API Key"**
4. Select **"Create API Key in new project"** or existing project
5. Copy the generated API key

### 2. Add to .env File

Update the `.env` file in `backend/` directory:

```env
GEMINI_API_KEY=your_actual_api_key_here
GEMINI_MODEL=gemini-2.0-flash
DATABASE_URL=sqlite:///insightiq.db
```

Replace `your_actual_api_key_here` with your actual API key from step 1.

### 3. Verify Configuration

Restart the backend server and test the `/api/insights` endpoint:

```bash
# From backend/ directory
python -m flask run
```

Then in your browser or via curl:

```bash
curl http://localhost:5000/api/insights
```

**With Gemini configured**: Response will include `"source": "gemini-2.0-flash"` with narrative insights.

**Without Gemini**: Response will include `"source": "local-analytics"` with fallback insights.

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GEMINI_API_KEY` | (empty) | Your Google Gemini API key |
| `GEMINI_MODEL` | `gemini-2.0-flash` | Gemini model version to use |
| `DATABASE_URL` | `sqlite:///insightiq.db` | SQLite database path |

## Available Models

- **gemini-2.0-flash** (recommended) - Latest, fastest model
- **gemini-1.5-flash** - Alternative, slightly older but reliable
- **gemini-1.5-pro** - More capable, slower response time

## Troubleshooting

### "Gemini API is not configured yet"

**Cause**: `GEMINI_API_KEY` is missing or empty in `.env`

**Solution**: 
1. Verify you've added the API key to `.env`
2. Restart the backend server
3. Check that the `.env` file is in the `backend/` directory

### API Key Not Working

**Cause**: Invalid or revoked API key

**Solution**:
1. Go back to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Delete and create a new API key
3. Update `.env` with the new key
4. Restart server

### Slow Responses

**Cause**: Network latency or model overload

**Solution**:
1. Try `gemini-1.5-flash` instead of `gemini-2.0-flash` (update `GEMINI_MODEL` in `.env`)
2. Check your internet connection
3. The service automatically falls back to local analytics on timeout

## Features Enabled with Gemini

### 1. Advanced Insights Endpoint

**GET** `/api/insights`

Returns AI-powered strategic recommendations for:
- Executive business insights
- Profitability analysis
- Growth opportunities
- Risk observations

### 2. AI Chat Interface

**POST** `/api/chat`

Request:
```json
{
  "question": "Which region is most profitable?",
  "history": []
}
```

Allows natural language questions about sales data with AI-powered responses.

## Security Considerations

⚠️ **Never commit `.env` to Git**

1. `.env` is listed in `.gitignore` (should be)
2. Do not share your API key publicly
3. Treat API keys like passwords
4. Consider using GitHub Secrets for CI/CD pipelines

## Cost Information

Google Gemini API is **free** under the following conditions:
- First 50 requests per day: Free
- After that: Usage-based pricing (check [Google AI Pricing](https://ai.google.dev/pricing))
- Estimate: ~$0.075 per 1M input tokens, $0.30 per 1M output tokens

For a typical dashboard with 10-50 insight requests per day, you'll stay within free tier.

## Next Steps

1. ✅ Set up your Gemini API key
2. ✅ Update `backend/.env`
3. ✅ Restart backend server
4. ✅ Test `/api/insights` endpoint
5. ✅ Try the chat interface in the dashboard
