/**
 * 天猫精灵 Webhook 测试脚本
 * 模拟天猫精灵云平台发送的请求
 */

const axios = require('axios');

const WEBHOOK_URL = process.argv[2] || 'http://localhost:3000/aligenie';
const query = process.argv[3] || '你好';

const testCases = [
    {
        name: '天气查询',
        payload: {
            header: { name: 'IntentRequest', namespace: 'AliGenie.IoT.Control' },
            payload: {
                intent: 'weather_query',
                slots: { city: '北京' },
                query: '查一下北京天气'
            }
        }
    },
    {
        name: '创建日程',
        payload: {
            header: { name: 'IntentRequest' },
            payload: {
                intent: 'schedule_create',
                slots: { time: '下午三点', content: '开会' },
                query: '提醒我下午三点开会'
            }
        }
    },
    {
        name: '监控检查',
        payload: {
            header: { name: 'IntentRequest' },
            payload: {
                intent: 'monitor_check',
                slots: {},
                query: 'DeepSeek 有新模型吗'
            }
        }
    },
    {
        name: '通用聊天',
        payload: {
            header: { name: 'IntentRequest' },
            payload: {
                intent: 'general_chat',
                slots: {},
                query: query
            }
        }
    }
];

async function testWebhook(testCase) {
    console.log(`\n🧪 测试：${testCase.name}`);
    console.log('请求:', JSON.stringify(testCase.payload, null, 2));
    
    try {
        const response = await axios.post(WEBHOOK_URL, testCase.payload, {
            headers: { 'Content-Type': 'application/json' },
            timeout: 10000
        });
        
        console.log('✅ 响应:', JSON.stringify(response.data, null, 2));
        return response.data;
    } catch (error) {
        console.log('❌ 错误:', error.message);
        if (error.response) {
            console.log('响应状态:', error.response.status);
            console.log('响应内容:', error.response.data);
        }
        return null;
    }
}

async function runTests() {
    console.log('🚀 天猫精灵 Webhook 测试工具');
    console.log('Webhook URL:', WEBHOOK_URL);
    console.log('='.repeat(50));
    
    // 先检查服务是否运行
    try {
        await axios.get(WEBHOOK_URL.replace('/aligenie', '/health'), { timeout: 3000 });
        console.log('✅ Webhook 服务运行中\n');
    } catch (error) {
        console.log('❌ Webhook 服务未运行，请先执行：npm start\n');
        process.exit(1);
    }
    
    // 运行所有测试
    for (const testCase of testCases) {
        await testWebhook(testCase);
        console.log('='.repeat(50));
    }
    
    console.log('\n✅ 所有测试完成！');
}

runTests().catch(console.error);
