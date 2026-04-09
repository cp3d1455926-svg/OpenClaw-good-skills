/**
 * 天猫精灵 × OpenClaw 智能桥接服务
 * 
 * 接收天猫精灵云端服务透传请求，调用 OpenClaw 执行技能，返回语音响应
 */

const express = require('express');
const axios = require('axios');
const cors = require('cors');
const bodyParser = require('body-parser');

const app = express();
const PORT = process.env.PORT || 3000;
const OPENCLAW_URL = process.env.OPENCLAW_URL || 'https://proventricular-adan-hugeously.ngrok-free.dev';

app.use(cors());
app.use(bodyParser.json());

// 健康检查
app.get('/health', (req, res) => {
    res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// 天猫精灵 webhook 主入口
app.post('/aligenie', async (req, res) => {
    console.log('[AliGenie] Request:', JSON.stringify(req.body, null, 2));
    
    try {
        const { header, payload } = req.body;
        const intentName = payload?.intent || 'general_chat';
        const slots = payload?.slots || {};
        const query = payload?.query || '';
        
        let openclawMessage = buildOpenClawMessage(intentName, slots, query);
        console.log('[OpenClaw] Sending:', openclawMessage);
        
        const response = await callOpenClaw(openclawMessage);
        console.log('[OpenClaw] Response:', response);
        
        const aligenieResponse = formatAliGenieResponse(response);
        console.log('[AliGenie] Response:', JSON.stringify(aligenieResponse, null, 2));
        
        res.json(aligenieResponse);
    } catch (error) {
        console.error('[Error]', error.message);
        res.json(formatAliGenieResponse('抱歉，服务暂时不可用'));
    }
});

// 构建 OpenClaw 消息
function buildOpenClawMessage(intent, slots, query) {
    const intentMap = {
        'weather_query': `查询${slots.city || '北京'}的天气`,
        'schedule_create': `创建日程提醒：${slots.time || ''} ${slots.content || query}`,
        'schedule_query': '查看我的日程安排',
        'monitor_check': '检查所有监控状态（DeepSeek、Kimi）',
        'message_send': `发送消息：${query}`,
        'news_query': '获取最新新闻',
        'todo_create': `创建待办事项：${query}`,
        'todo_list': '查看我的待办列表',
        'general_chat': query || '你好',
    };
    
    return intentMap[intent] || query || '你好';
}

// 调用 OpenClaw Gateway（同步模式）
async function callOpenClaw(message) {
    const fs = require('fs');
    const path = require('path');
    
    // 方案 1: HTTP API 模式（推荐 - 同步回复）
    if (OPENCLAW_URL && OPENCLAW_URL !== 'http://localhost:18789') {
        console.log('[HTTP Mode] Calling OpenClaw Gateway:', OPENCLAW_URL);
        try {
            const result = await axios.post(`${OPENCLAW_URL}/agent`, {
                message: message,
                channel: 'wecom'
            }, { timeout: 25000 }); // 25 秒超时，确保天猫精灵不超时
            
            if (result.data && result.data.response) {
                console.log('[HTTP Mode] Got response:', result.data.response);
                return result.data.response;
            }
        } catch (httpError) {
            console.log('[HTTP Mode Failed]', httpError.message);
            // 降级到文件模式
        }
    }
    
    // 方案 2: 文件模式（本地测试）
    try {
        const workspaceRoot = path.join(__dirname, '../../..');
        const inputFile = path.join(workspaceRoot, 'memory', 'aligenie-input.txt');
        const outputFile = path.join(workspaceRoot, 'memory', 'aligenie-output.txt');
        
        // 确保目录存在
        const memoryDir = path.join(workspaceRoot, 'memory');
        if (!fs.existsSync(memoryDir)) {
            fs.mkdirSync(memoryDir, { recursive: true });
        }
        
        // 写入输入
        const inputData = {
            message: message,
            timestamp: new Date().toISOString(),
            source: 'aligenie',
            webhook: 'aligenie-bridge'
        };
        fs.writeFileSync(inputFile, JSON.stringify(inputData, null, 2), 'utf8');
        
        console.log('[File Mode] Written to:', inputFile);
        
        // 等待 OpenClaw 处理（轮询输出文件）
        const maxWait = 65000; // 最多等 65 秒（Cron 每分钟检查一次）
        const pollInterval = 1000; // 每 1 秒检查一次
        let waited = 0;
        
        while (waited < maxWait) {
            await sleep(pollInterval);
            waited += pollInterval;
            
            if (fs.existsSync(outputFile)) {
                try {
                    const output = fs.readFileSync(outputFile, 'utf8').trim();
                    if (output) {
                        fs.unlinkSync(outputFile);
                        console.log('[File Mode] Got response:', output);
                        return output;
                    }
                } catch (e) {
                    // 文件可能被锁定
                }
            }
        }
        
        // 超时返回
        console.log('[File Mode] Timeout');
        return `已收到指令："${message}"。处理超时，请稍后再试。`;
        
    } catch (error) {
        console.error('[OpenClaw Error]', error.message);
        return `OpenClaw 调用失败：${error.message}`;
    }
}

// 格式化天猫精灵响应
function formatAliGenieResponse(text) {
    return {
        version: '2.0',
        response: {
            output: {
                text: text,
                type: 'PlainText'
            },
            action: 'response'
        }
    };
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// 启动服务器
const server = app.listen(PORT, () => {
    console.log(`🚀 AliGenie-OpenClaw Bridge running on port ${PORT}`);
    console.log(`   Local: http://localhost:${PORT}`);
    console.log(`   Health: http://localhost:${PORT}/health`);
    console.log(`   Webhook: POST http://localhost:${PORT}/aligenie`);
});

// Vercel/Serverless 支持
module.exports = app;
