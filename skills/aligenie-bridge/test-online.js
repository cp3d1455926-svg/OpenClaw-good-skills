const axios = require('axios');

async function test() {
    try {
        console.log('Testing health check...');
        const health = await axios.get('https://aligenie-bridge.vercel.app/health');
        console.log('✅ Health:', health.data);
        
        console.log('\nTesting webhook...');
        const response = await axios.post('https://aligenie-bridge.vercel.app/aligenie', {
            header: { name: 'IntentRequest' },
            payload: {
                intent: 'general_chat',
                query: '你好，测试天猫精灵'
            }
        });
        console.log('✅ Webhook Response:', JSON.stringify(response.data, null, 2));
    } catch (error) {
        console.log('❌ Error:', error.message);
        if (error.response) {
            console.log('Status:', error.response.status);
            console.log('Data:', error.response.data);
        }
    }
}

test();
