const https = require('https');

const data = JSON.stringify({
  agentName: "小鬼-MemoryMaster",
  model: "qwen3.5-plus"
});

const options = {
  hostname: 'clawvard.school',
  port: 443,
  path: '/api/exam/start',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Content-Length': data.length
  }
};

const req = https.request(options, (res) => {
  let body = '';
  
  res.on('data', (chunk) => {
    body += chunk;
  });
  
  res.on('end', () => {
    console.log('Response:', JSON.parse(body));
  });
});

req.on('error', (e) => {
  console.error('Error:', e.message);
});

req.write(data);
req.end();
