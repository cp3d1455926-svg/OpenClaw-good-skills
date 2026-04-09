const axios = require('axios');

async function test() {
    try {
        const response = await axios.post('http://localhost:3000/aligenie', {
            header: { name: 'IntentRequest' },
            payload: {
                intent: 'general_chat',
                query: '你好，测试天猫精灵连接'
            }
        });
        console.log('✅ Response:', JSON.stringify(response.data, null, 2));
    } catch (error) {
        console.log('❌ Error:', error.message);
        if (error.response) {
            console.log('Status:', error.response.status);
            console.log('Data:', error.response.data);
        }
    }
}

test();
