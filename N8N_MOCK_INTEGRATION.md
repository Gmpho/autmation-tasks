# 🔗 n8n Mock API Integration Guide

This guide shows you how to integrate your mock API server with n8n workflows for **completely free** Instagram automation testing.

## 🎯 Overview

Your mock API server provides all the endpoints you need to build and test complete Instagram automation workflows without any API costs.

## 📡 Available Mock Endpoints

| Endpoint | Method | Purpose | Cost |
|----------|--------|---------|------|
| `/health` | GET | Server health check | FREE |
| `/ai/claude/generate` | POST | Mock Claude content generation | FREE |
| `/ai/openai/generate` | POST | Mock OpenAI content generation | FREE |
| `/ai/compare` | POST | Compare both AI providers | FREE |
| `/ai/stories` | POST | Generate Instagram Stories | FREE |
| `/instagram/post` | POST | Mock Instagram posting | FREE |
| `/analytics` | GET | Usage analytics | FREE |

## 🚀 Setting Up n8n Workflows

### **Step 1: Start Your Services**

```bash
# Terminal 1: Start n8n
docker-compose up -d

# Terminal 2: Start Mock API Server
python mock_api_server.py

# Access Points:
# n8n: http://localhost:5678
# Mock API Dashboard: http://localhost:8000
```

### **Step 2: Create Basic Content Generation Workflow**

1. **Open n8n**: Go to `http://localhost:5678`
2. **Create New Workflow**
3. **Add Nodes**:

#### **Node 1: Schedule Trigger**
- **Type**: Schedule Trigger
- **Interval**: Every 1 hour (for testing)
- **Purpose**: Automatically trigger content generation

#### **Node 2: Set Content Parameters**
- **Type**: Set Node
- **Purpose**: Define content generation parameters
- **Values**:
  ```json
  {
    "topic": "Instagram Growth Tips",
    "power_words": "proven, explosive, secret, ultimate",
    "emotion": "excitement and motivation",
    "cta": "Save this post!",
    "niche": "social media marketing"
  }
  ```

#### **Node 3: Generate with Claude (Mock)**
- **Type**: HTTP Request
- **Method**: POST
- **URL**: `http://localhost:8000/ai/claude/generate`
- **Headers**: `Content-Type: application/json`
- **Body**: Use data from previous node
- **Purpose**: Generate content with mock Claude AI

#### **Node 4: Generate with OpenAI (Mock)**
- **Type**: HTTP Request  
- **Method**: POST
- **URL**: `http://localhost:8000/ai/openai/generate`
- **Headers**: `Content-Type: application/json`
- **Body**: Use data from Set node
- **Purpose**: Generate content with mock OpenAI

#### **Node 5: Compare Results**
- **Type**: HTTP Request
- **Method**: POST
- **URL**: `http://localhost:8000/ai/compare`
- **Headers**: `Content-Type: application/json`
- **Body**: Use data from Set node
- **Purpose**: Get comparison of both AI providers

#### **Node 6: Choose Best Content**
- **Type**: Function Node
- **Purpose**: Select the best content based on criteria
- **Code**:
  ```javascript
  // Get comparison results
  const comparison = items[0].json.data;
  
  // Simple selection logic (you can make this more sophisticated)
  const claudeContent = comparison.providers.claude;
  const openaiContent = comparison.providers.openai;
  
  // For demo, randomly choose or use Claude as default
  const selectedContent = claudeContent;
  
  return [{
    json: {
      selected_provider: "claude",
      content: selectedContent.content,
      model: selectedContent.model,
      cost: selectedContent.cost
    }
  }];
  ```

#### **Node 7: Post to Instagram (Mock)**
- **Type**: HTTP Request
- **Method**: POST
- **URL**: `http://localhost:8000/instagram/post`
- **Headers**: `Content-Type: application/json`
- **Body**:
  ```json
  {
    "content": "{{ $json.content }}",
    "hashtags": ["#InstagramGrowth", "#SocialMedia", "#AI", "#Automation"]
  }
  ```

#### **Node 8: Log Results**
- **Type**: Function Node
- **Purpose**: Log the complete workflow results
- **Code**:
  ```javascript
  const postResult = items[0].json.data;
  
  console.log('🎉 Workflow completed successfully!');
  console.log('📊 Post ID:', postResult.post_id);
  console.log('💰 Total Cost: $0.00 (Mock)');
  
  return [{
    json: {
      workflow_status: "completed",
      post_id: postResult.post_id,
      timestamp: new Date().toISOString(),
      total_cost: "$0.00"
    }
  }];
  ```

### **Step 3: Create Instagram Stories Workflow**

#### **Workflow: Daily Stories Generation**

1. **Schedule Trigger**: Daily at 9 AM
2. **Set Parameters**:
   ```json
   {
     "topic": "Daily Motivation",
     "style": "casual"
   }
   ```
3. **Generate Stories**: POST to `/ai/stories`
4. **Process Stories**: Parse and format the response
5. **Mock Post Stories**: POST to `/instagram/post` (adapted for stories)

### **Step 4: Create Analytics Monitoring Workflow**

#### **Workflow: Hourly Analytics Check**

1. **Schedule Trigger**: Every hour
2. **Get Analytics**: GET from `/analytics`
3. **Process Data**: Extract key metrics
4. **Alert if Needed**: Send notifications for important events

## 🧪 Testing Your Workflows

### **Manual Testing**
1. **Execute Workflow**: Click "Execute Workflow" in n8n
2. **Check Results**: View output in each node
3. **Verify Mock API**: Check dashboard at `http://localhost:8000`

### **Automated Testing**
```bash
# Run comprehensive API tests
python test_mock_api.py
```

## 📊 Monitoring and Debugging

### **Mock API Dashboard**
- **URL**: `http://localhost:8000`
- **Features**:
  - Real-time request counter
  - Generated content history
  - Mock Instagram posts
  - Zero-cost analytics

### **n8n Execution Log**
- View in n8n interface
- Check each node's output
- Monitor workflow execution times

## 🔄 Advanced Workflow Patterns

### **Pattern 1: Content A/B Testing**
```
Trigger → Generate Content (Both AIs) → Compare → Split Test → Post Best → Analyze Results
```

### **Pattern 2: Multi-Platform Posting**
```
Generate Content → Format for Instagram → Format for Stories → Post to Both → Track Engagement
```

### **Pattern 3: Content Calendar**
```
Schedule → Check Calendar → Generate Themed Content → Queue for Posting → Update Calendar
```

## 💡 Best Practices

### **Workflow Design**
- ✅ Use descriptive node names
- ✅ Add error handling nodes
- ✅ Log important steps
- ✅ Test with small intervals first

### **Mock API Usage**
- ✅ Monitor the dashboard regularly
- ✅ Check response times
- ✅ Validate data formats
- ✅ Test error scenarios

### **Development Process**
1. **Build workflows with mock APIs**
2. **Test thoroughly with free endpoints**
3. **Perfect your automation logic**
4. **Only then add real API keys**

## 🚀 Next Steps

Once your workflows are perfect with mock APIs:

1. **Replace mock endpoints** with real API URLs
2. **Add real API keys** to environment variables
3. **Update n8n HTTP nodes** to use production endpoints
4. **Monitor costs** and usage carefully

## 💰 Cost Comparison

| Development Phase | Mock API | Real APIs |
|-------------------|----------|-----------|
| **Workflow Building** | $0.00 | $0.00 |
| **Testing (100 requests)** | $0.00 | ~$2-5 |
| **Content Generation** | $0.00 | ~$0.01-0.10 per request |
| **Instagram Posting** | $0.00 | Free (but requires approval) |

**Total Development Cost: $0.00 with Mock APIs!**

---

🎉 **You can now build, test, and perfect your entire Instagram automation system without spending a penny!**
