/**
 * 天猫精灵 Webhook 完整测试套件
 * 测试所有支持的语音指令场景
 */

const axios = require('axios');

const WEBHOOK_URL = 'http://localhost:3000/aligenie';

const testCases = [
    {
        name: '🌤️ 天气查询 - 北京',
        payload: {
            header: { name: 'IntentRequest', namespace: 'AliGenie.IoT.Control' },
            payload: {
                intent: 'weather_query',
                slots: { city: '北京' },
                query: '查一下北京天气'
            }
        },
        expected: '查询北京的天气'
    },
    {
        name: '🌤️ 天气查询 - 上海',
        payload: {
            header: { name: 'IntentRequest' },
            payload: {
                intent: 'weather_query',
                slots: { city: '上海' },
                query: '上海今天天气怎么样'
            }
        },
        expected: '查询上海的天气'
    },
    {
        name: '📅 创建日程 - 会议提醒',
        payload: {
            header: { name: 'IntentRequest' },
            payload: {
                intent: 'schedule_create',
                slots: { time: '下午三点', content: '开会' },
                query: '提醒我下午三点开会'
            }
        },
        expected: '创建日程提醒'
    },
    {
        name: '📅 创建日程 - 约会',
        payload: {
            header: { name: 'IntentRequest' },
            payload: {
                intent: 'schedule_create',
                slots: { time: '明天上午十点', content: '看医生' },
                query: '明天上午十点提醒我看医生'
            }
        },
        expected: '创建日程提醒'
    },
    {
        name: '📅 查询日程',
        payload: {
            header: { name: 'IntentRequest' },
            payload: {
                intent: 'schedule_query',
                slots: {},
                query: '查看我的日程安排'
            }
        },
        expected: '查看我的日程安排'
    },
    {
        name: '🔍 监控检查 - DeepSeek',
        payload: {
            header: { name: 'IntentRequest' },
            payload: {
                intent: 'monitor_check',
                slots: { target: 'DeepSeek' },
                query: 'DeepSeek 有新模型吗'
            }
        },
        expected: '检查所有监控状态'
    },
    {
        name: '🔍 监控检查 - Kimi',
        payload: {
            header: { name: 'IntentRequest' },
            payload: {
                intent: 'monitor_check',
                slots: { target: 'Kimi' },
                query: 'Kimi 发布 K3 了吗'
            }
        },
        expected: '检查所有监控状态'
    },
    {
        name: '💬 发送消息',
        payload: {
            header: { name: 'IntentRequest' },
            payload: {
                intent: 'message_send',
                slots: { recipient: 'Jake' },
                query: '给 Jake 发消息说晚上一起吃饭'
            }
        },
        expected: '发送消息'
    },
    {
        name: '✅ 创建待办',
        payload: {
            header: { name: 'IntentRequest' },
            payload: {
                intent: 'todo_create',
                slots: {},
                query: '创建一个待办：买牛奶'
            }
        },
        expected: '创建待办事项'
    },
    {
        name: '✅ 查询待办',
        payload: {
            header: { name: 'IntentRequest' },
            payload: {
                intent: 'todo_list',
                slots: {},
                query: '查看我的待办列表'
            }
        },
        expected: '查看我的待办列表'
    },
    {
        name: '📰 查询新闻',
        payload: {
            header: { name: 'IntentRequest' },
            payload: {
                intent: 'news_query',
                slots: { category: '科技' },
                query: '今天有什么科技新闻'
            }
        },
        expected: '获取最新新闻'
    },
    {
        name: '🤖 通用聊天 - 问候',
        payload: {
            header: { name: 'IntentRequest' },
            payload: {
                intent: 'general_chat',
                slots: {},
                query: '你好'
            }
        },
        expected: '你好'
    },
    {
        name: '🤖 通用聊天 - 感谢',
        payload: {
            header: { name: 'IntentRequest' },
            payload: {
                intent: 'general_chat',
                slots: {},
                query: '谢谢你'
            }
        },
        expected: '谢谢你'
    },
    {
        name: '🤖 通用聊天 - 问题',
        payload: {
            header: { name: 'IntentRequest' },
            payload: {
                intent: 'general_chat',
                slots: {},
                query: '你会做什么'
            }
        },
        expected: '你会做什么'
    }
];

async function testWebhook(testCase, index) {
    const startTime = Date.now();
    
    console.log(`\n${index + 1}. ${testCase.name}`);
    console.log('   输入:', testCase.payload.payload.query);
    
    try {
        const response = await axios.post(WEBHOOK_URL, testCase.payload, {
            headers: { 'Content-Type': 'application/json' },
            timeout: 10000
        });
        
        const duration = Date.now() - startTime;
        const text = response.data.response?.output?.text || '无响应';
        
        console.log('   ✅ 响应:', text.substring(0, 60) + (text.length > 60 ? '...' : ''));
        console.log('   ⏱️ 耗时:', duration + 'ms');
        
        return {
            success: true,
            name: testCase.name,
            duration,
            text
        };
    } catch (error) {
        const duration = Date.now() - startTime;
        console.log('   ❌ 错误:', error.message);
        
        return {
            success: false,
            name: testCase.name,
            duration,
            error: error.message
        };
    }
}

async function runAllTests() {
    console.log('🚀 天猫精灵 Webhook 完整测试套件');
    console.log('Webhook URL:', WEBHOOK_URL);
    console.log('测试用例数:', testCases.length);
    console.log('='.repeat(60));
    
    // 先检查服务是否运行
    try {
        await axios.get(WEBHOOK_URL.replace('/aligenie', '/health'), { timeout: 3000 });
        console.log('✅ Webhook 服务运行中\n');
    } catch (error) {
        console.log('❌ Webhook 服务未运行！');
        console.log('请先执行：npm start\n');
        process.exit(1);
    }
    
    // 运行所有测试
    const results = [];
    for (let i = 0; i < testCases.length; i++) {
        const result = await testWebhook(testCases[i], i);
        results.push(result);
    }
    
    // 统计结果
    console.log('\n' + '='.repeat(60));
    console.log('📊 测试结果统计');
    console.log('='.repeat(60));
    
    const successCount = results.filter(r => r.success).length;
    const failCount = results.filter(r => !r.success).length;
    const avgDuration = results.reduce((sum, r) => sum + r.duration, 0) / results.length;
    
    console.log(`总用例数：${results.length}`);
    console.log(`✅ 成功：${successCount}`);
    console.log(`❌ 失败：${failCount}`);
    console.log(`⏱️ 平均耗时：${Math.round(avgDuration)}ms`);
    
    if (failCount > 0) {
        console.log('\n❌ 失败用例:');
        results.filter(r => !r.success).forEach(r => {
            console.log(`   - ${r.name}: ${r.error}`);
        });
    }
    
    console.log('\n✅ 所有测试完成！');
    
    // 保存测试报告
    const fs = require('fs');
    const report = {
        timestamp: new Date().toISOString(),
        total: results.length,
        success: successCount,
        failed: failCount,
        avgDuration: Math.round(avgDuration),
        results
    };
    
    fs.writeFileSync(
        './test-report.json',
        JSON.stringify(report, null, 2)
    );
    console.log('\n📄 测试报告已保存到：test-report.json');
}

runAllTests().catch(console.error);
