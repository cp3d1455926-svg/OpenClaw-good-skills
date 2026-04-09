#!/usr/bin/env node
/**
 * 科技晚报生成器
 * 每天自动生成一篇科技新闻，适合小红书发布
 */

const fs = require('fs');
const path = require('path');

// 科技话题库
const TOPICS = [
  {
    category: 'AI',
    themes: [
      '大模型竞争',
      'AI应用落地',
      'AI安全与监管',
      'AI芯片发展',
      'AI编程助手',
      'AI绘画工具',
      'AI视频生成',
      'AI音乐创作'
    ]
  },
  {
    category: '数码',
    themes: [
      '手机新品发布',
      '芯片技术突破',
      '折叠屏技术',
      '影像技术升级',
      '快充技术',
      '操作系统更新',
      '智能穿戴设备',
      '平板电脑市场'
    ]
  },
  {
    category: '汽车',
    themes: [
      '新能源汽车销量',
      '自动驾驶技术',
      '电池技术突破',
      '智能座舱',
      '充电基础设施',
      '汽车芯片',
      '飞行汽车',
      'Robotaxi'
    ]
  },
  {
    category: '航天',
    themes: [
      'SpaceX星舰',
      '中国空间站',
      '月球探测',
      '火星计划',
      '卫星互联网',
      '商业航天',
      '太空旅游',
      '小行星采矿'
    ]
  },
  {
    category: '前沿',
    themes: [
      '量子计算',
      '脑机接口',
      '人形机器人',
      '6G通信',
      '元宇宙',
      'Web3',
      '合成生物学',
      '核聚变能源'
    ]
  }
];

// 获取今天的日期
function getTodayDate() {
  const now = new Date();
  return {
    date: now.toISOString().split('T')[0],
    weekday: ['周日', '周一', '周二', '周三', '周四', '周五', '周六'][now.getDay()]
  };
}

// 根据日期选择话题（循环）或随机选择
function selectTopic(random = false) {
  if (random) {
    // 随机选择
    const topicIndex = Math.floor(Math.random() * TOPICS.length);
    const themeIndex = Math.floor(Math.random() * TOPICS[topicIndex].themes.length);
    return {
      category: TOPICS[topicIndex].category,
      theme: TOPICS[topicIndex].themes[themeIndex]
    };
  }
  
  // 按日期循环
  const dayOfYear = Math.floor((new Date() - new Date(new Date().getFullYear(), 0, 0)) / (1000 * 60 * 60 * 24));
  const topicIndex = dayOfYear % TOPICS.length;
  const themeIndex = (dayOfYear * 3) % TOPICS[topicIndex].themes.length;
  
  return {
    category: TOPICS[topicIndex].category,
    theme: TOPICS[topicIndex].themes[themeIndex]
  };
}

// 生成新闻标题
function generateTitle(topic) {
  const templates = [
    `【科技晚报】${topic.theme}迎来新突破，行业格局或将重塑`,
    `【今日科技】${topic.theme}市场激战，头部玩家纷纷加码`,
    `【科技前沿】${topic.theme}技术迭代加速，商业化进程提速`,
    `【行业观察】${topic.theme}成投资热点，资本涌入赛道`,
    `【科技动态】${topic.theme}用户规模破纪录，渗透率持续提升`
  ];
  
  const date = new Date();
  const index = (date.getDate() + date.getMonth()) % templates.length;
  return templates[index];
}

// 生成新闻正文
function generateContent(topic) {
  const { date, weekday } = getTodayDate();
  
  const contents = {
    'AI': `
**【行业动态】**
${topic.theme}领域今日迎来重要进展。据业内消息，多家头部企业近期密集发布相关产品更新，技术迭代速度明显加快。市场分析指出，这一趋势反映出AI技术正从实验室走向大规模商业应用。

**【市场数据】**
• 用户规模：月活跃用户同比增长120%
• 市场规模：预计本年度将达到千亿级别
• 投资热度：Q1季度融资总额超过去年同期3倍
• 应用渗透：在办公、教育、创作等领域渗透率超40%

**【企业动态】**
国内方面，多家科技公司加速布局${topic.theme}赛道，推出面向企业和个人的多样化解决方案。国际市场上，OpenAI、Google等巨头持续加大研发投入，竞争日趋激烈。

**【专家观点】**
"${topic.theme}正在经历从'能用'到'好用'的关键转变。"某知名AI研究员表示，"未来6-12个月将是产品形态定型的重要窗口期。"

**【趋势研判】**
行业分析师普遍认为，随着技术成熟度提升和成本下降，${topic.theme}将在更多垂直场景实现落地。预计到2025年底，相关应用将覆盖80%以上的知识工作者。`,

    '数码': `
**【产品动态】**
${topic.theme}领域今日传来重要消息。据供应链消息，多家厂商正在加速推进相关技术研发，新品发布节奏明显加快。市场观察人士指出，这一趋势预示着行业正迎来新一轮技术升级周期。

**【技术亮点】**
• 性能提升：相比上一代产品提升约30%
• 功耗优化：续航能力延长20%以上
• 成本控制：规模化生产后成本下降15%
• 用户体验：用户满意度达85%以上

**【市场反应】**
从预售数据来看，消费者对${topic.theme}表现出强烈兴趣。多家电商平台数据显示，相关产品预约量创近期新高。线下渠道反馈，咨询量较上月增长超50%。

**【行业分析】**
"${topic.theme}代表了消费电子行业的重要发展方向。"某券商分析师表示，"随着技术成熟和成本下降，预计将在未来2-3年内实现大规模普及。"

**【消费建议】**
对于普通消费者而言，建议关注产品的实际使用体验而非单纯参数。同时，考虑到技术迭代速度，可根据自身需求合理选择购买时机。`,

    '汽车': `
**【市场动态】**
${topic.theme}领域今日发布重要数据。据行业协会统计，相关技术应用规模持续扩大，市场渗透率稳步提升。业内专家表示，这标志着新能源汽车产业正进入高质量发展新阶段。

**【数据看点】**
• 装车量：本月装车量环比增长25%
• 续航里程：平均续航突破600公里
• 充电速度：快充时间缩短至30分钟以内
• 安全记录：事故率较传统汽车降低40%

**【企业布局】**
头部车企纷纷加大在${topic.theme}领域的投入。特斯拉、比亚迪、蔚来等企业近期均有重要技术发布或产品更新。传统车企也在加速转型，推出多款搭载相关技术的新车型。

**【政策支持】**
相关部门近期出台多项支持政策，包括基础设施建设补贴、技术研发奖励等。地方政府积极响应，多个城市公布${topic.theme}产业发展规划。

**【未来展望】**
行业预测，到2025年，${topic.theme}将成为新能源汽车的标配功能。随着技术不断成熟和成本持续下降，消费者接受度有望进一步提升。`,

    '航天': `
**【任务进展】**
${topic.theme}项目今日传来最新消息。据航天部门通报，相关任务按计划稳步推进，关键技术指标均达到预期。这一进展标志着我国航天事业在相关领域取得重要突破。

**【技术突破】**
• 运载能力：单次运载能力提升至新高度
• 可靠性：成功率保持在98%以上
• 成本控制：单次发射成本下降30%
• 应用拓展：应用场景从科研向商业扩展

**【国际对比】**
在全球范围内，${topic.theme}技术呈现多国竞争态势。美国SpaceX保持领先地位，中国、欧洲、俄罗斯等也在加速追赶。商业航天领域竞争尤为激烈，多家创业公司获得大额融资。

**【商业应用】**
随着技术成熟，${topic.theme}的商业价值逐渐显现。卫星通信、太空旅游、太空制造等领域展现出巨大潜力。多家投资机构预测，相关市场规模将在未来10年内达到万亿级别。

**【专家解读】**
"${topic.theme}代表了人类探索太空的新阶段。"某航天专家表示，"从技术验证走向商业应用，这是航天产业发展的重要转折点。"`,

    '前沿': `
**【科研进展】**
${topic.theme}研究今日取得重要突破。据权威期刊报道，科研团队在相关领域实现关键技术验证，实验数据表现优异。这一成果为技术实用化奠定了重要基础。

**【技术参数】**
• 性能指标：关键性能提升10倍以上
• 稳定性：连续运行时间突破新纪录
• 成本控制：单位成本下降至可接受范围
• 应用前景：在多个场景展现应用潜力

**【产业动态】**
科技巨头纷纷布局${topic.theme}领域。Google、IBM、微软等国际企业持续投入研发，国内华为、阿里、腾讯等也在积极跟进。创业公司活跃，多家相关企业获得大额融资。

**【应用场景】**
专家预测，${topic.theme}将在以下领域率先实现应用：金融建模、药物研发、材料设计、人工智能训练等。随着技术成熟，应用范围有望进一步扩展。

**【发展预测】**
"${topic.theme}正处于从实验室走向产业化的关键期。"某科技投资人表示，"未来3-5年将是技术落地的重要窗口期，也是投资布局的黄金时期。"`
  };
  
  return contents[topic.category] || contents['AI'];
}

// 生成完整的小红书文案
function generateXiaohongshuPost(topic) {
  const { date, weekday } = getTodayDate();
  const title = generateTitle(topic);
  const content = generateContent(topic);
  
  return `${title}

📰 ${date} ${weekday} 科技晚报

${content}

---

**标签：**
#科技新闻 #${topic.category} #${topic.theme} #科技趋势 #行业分析 #科技晚报 #前沿科技 #投资

**互动：**
你对${topic.theme}怎么看？

是技术革命还是概念炒作？
评论区聊聊👇

---

*本内容由AI自动生成，仅供参考*`;
}

// 主函数
function main() {
  const topic = selectTopic(true); // 使用随机主题
  const post = generateXiaohongshuPost(topic);
  const { date } = getTodayDate();
  
  // 确保目录存在
  const newsDir = 'X:\\小红书科技新闻';
  if (!fs.existsSync(newsDir)) {
    fs.mkdirSync(newsDir, { recursive: true });
  }
  
  // 保存文件
  const filename = path.join(newsDir, `${date}.md`);
  fs.writeFileSync(filename, post, 'utf8');
  
  console.log(`✅ 科技晚报已生成：${filename}`);
  console.log(`📋 主题：${topic.category} - ${topic.theme}`);
  console.log('\n' + post);
}

// 执行
main();
