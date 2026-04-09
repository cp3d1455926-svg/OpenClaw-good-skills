const axios = require('axios');

async function testWebhook() {
    console.log('🧪 测试天猫精灵 Webhook...\n');
    
    const testCases = [
        {
            name: '天气查询',
            intent: 'weather_query',
            query: '查询北京天气'
        },
        {
            name: '创建日程',
            intent: 'schedule_create',
            query: '提醒我下午三点开会'
        },
        {
            name: '监控检查',
            intent: 'monitor_check',
            query: 'DeepSeek 有新模型吗'
        }
    ];
    
    const url = 'https://aligenie-bridge.vercel.app/aligenie';
    
    for (const test of testCases) {
        console.log(`测试：${test.name}`);
        console.log(`指令：${test.query}\n`);
        
        try {
            const response = await axios.post(url, {
                header: { name: 'IntentRequest' },
                payload: {
                    intent: test.intent,
                    query: test.query
                }
            }, {
                timeout: 10000
            });
            
            const text = response.data.response?.output?.text || '无响应';
            console.log(`✅ 响应：${text}\n`);
            console.log('---\n');
        } catch (error) {
            console.log(`❌ 错误：${error.message}\n`);
            console.log('---\n');
        }
    }
    
    console.log('✅ 测试完成！');
}

testWebhook();
