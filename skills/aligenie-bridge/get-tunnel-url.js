const axios = require('axios');

async function getTunnel() {
    try {
        const res = await axios.get('http://localhost:4040/api/tunnels');
        console.log('Ngrok 隧道信息:');
        console.log(JSON.stringify(res.data, null, 2));
    } catch (error) {
        console.log('错误:', error.message);
    }
}

getTunnel();
