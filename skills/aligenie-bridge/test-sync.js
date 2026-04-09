const axios = require('axios');

async function test() {
    console.log('🧪 测试同步回复模式...\n');
    
    const OPENCLAW_URL = 'https://proventricular-adan-hugeously.ngrok-free.dev';
    const WEBHOOK_URL = 'http://localhost:3000/aligenie';
    
    console.log('OpenClaw Gateway:', OPENCLAW_URL);
    console.log('Webhook:', WEBHOOK_URL);
    console.log('');
    
    try {
        // 测试 1: 检查 OpenClaw Gateway
        console.log('1️⃣ 测试 OpenClaw Gateway 连接...');
        try {
            const gatewayRes = await axios.get(`${OPENCLAW_URL}/health`, { timeout: 10000 });
            console.log('✅ Gateway 在线');
        } catch (error) {
            console.log('⚠️ Gateway 无法访问（可能是 ngrok 免费版限制）');
        }
        
        // 测试 2: 测试 Webhook
        console.log('\n2️⃣ 测试 Webhook 响应...');
        const response = await axios.post(WEBHOOK_URL, {
            header: { name: 'IntentRequest' },
            payload: {
                intent: 'general_chat',
                query: '你好，测试同步回复'
            }
        }, { timeout: 30000 });
        
        const text = response.data.response?.output?.text || '无响应';
        console.log('✅ 响应:', text.substring(0, 100) + (text.length > 100 ? '...' : ''));
        
        console.log('\n✅ 测试完成！');
        
    } catch (error) {
        console.log('❌ 错误:', error.message);
    }
}

test();
