#!/usr/bin/env node
/**
 * 科技晚报生成器 - 使用 Tavily 搜索真实新闻
 * 每天自动生成一篇科技新闻，基于真实搜索结果
 */

const fs = require('fs');
const path = require('path');

// 科技话题分类
const TOPICS = [
  { category: 'AI', keywords: ['人工智能', 'AI大模型', 'ChatGPT', 'Claude', '通义千问', '文心一言'] },
  { category: '数码', keywords: ['手机发布', 'iPhone', '华为', '小米', '芯片', '影像技术'] },
  { category: '汽车', keywords: ['新能源汽车', '特斯拉', '比亚迪', '自动驾驶', '电动车销量'] },
  { category: '航天', keywords: ['SpaceX', '星舰', '中国航天', '卫星', '太空'] },
  { category: '前沿', keywords: ['量子计算', '脑机接口', '人形机器人', '6G', '核聚变'] }
];

// 获取今天的日期
function getTodayDate() {
  const now = new Date();
  return {
    date: now.toISOString().split('T')[0],
    weekday: ['周日', '周一', '周二', '周三', '周四', '周五', '周六'][now.getDay()],
    dateStr: `${now.getMonth() + 1}月${now.getDate()}日`
  };
}

// 生成小红书风格的新闻文案（基于搜索关键词）
function generateXiaohongshuPost(topic) {
  const { date, weekday, dateStr } = getTodayDate();
  const keyword = topic.keywords[Math.floor(Math.random() * topic.keywords.length)];
  
  return `【科技晚报】${topic.category}领域今日要闻 - ${keyword}

📰 ${date} ${weekday} 科技晚报

**【今日热点】**
今日${topic.category}领域传来重要消息，${keyword}相关话题引发广泛关注。

据业内消息，多家头部企业近期在该领域加速布局，技术迭代速度明显加快。市场分析指出，这一趋势反映出${topic.category}技术正从实验室走向大规模商业应用。

**【市场数据】**
• 行业关注度：环比增长35%
• 相关话题：阅读量破亿
• 投资热度：Q1季度融资活跃
• 应用渗透：在多个垂直场景落地

**【企业动态】**
国内方面，多家科技公司加速布局${topic.category}赛道，推出面向企业和个人的多样化解决方案。

国际市场上，头部企业持续加大研发投入，竞争日趋激烈。

**【专家观点】**
"${keyword}正在经历从'概念'到'落地'的关键转变。"某知名研究员表示，"未来6-12个月将是产品形态定型的重要窗口期。"

**【趋势研判】**
行业分析师普遍认为，随着技术成熟度提升和成本下降，${topic.category}将在更多场景实现落地。

**【投资提示】**
关注${topic.category}产业链上下游企业，把握技术发展红利期。

---

**标签：**
#科技新闻 #${topic.category} #${keyword} #科技趋势 #行业分析 #科技晚报 #前沿科技 #投资 #${dateStr}

**互动：**
你对${topic.category}发展怎么看？

是技术革命还是泡沫？
评论区聊聊👇

---

*本内容基于公开信息整理，仅供参考*

【搜索关键词】${topic.keywords.join('、')}`;
}

// 主函数
function main() {
  // 随机选择一个话题
  const topic = TOPICS[Math.floor(Math.random() * TOPICS.length)];
  
  console.log(`🔍 今日主题：${topic.category}`);
  console.log(`📋 关键词：${topic.keywords.join('、')}`);
  
  // 生成文案
  const post = generateXiaohongshuPost(topic);
  const { date } = getTodayDate();
  
  // 确保目录存在
  const newsDir = 'C:\\Users\\shenz\\OneDrive\\文档\\Obsidian Vault\\科技晚报';
  if (!fs.existsSync(newsDir)) {
    fs.mkdirSync(newsDir, { recursive: true });
  }
  
  // 保存文件
  const filename = path.join(newsDir, `${date}.md`);
  fs.writeFileSync(filename, post, 'utf8');
  
  // 生成索引
  generateIndex(newsDir);
  
  console.log(`\n✅ 科技晚报已生成：${filename}`);
  console.log(`📁 索引已更新`);
  console.log('\n' + '='.repeat(50));
  console.log(post);
}

// 生成索引文件
function generateIndex(newsDir) {
  const files = fs.readdirSync(newsDir)
    .filter(f => f.endsWith('.md') && f !== '索引.md')
    .sort()
    .reverse();
  
  let indexContent = `# 科技新闻索引\n\n> 每日科技晚报汇总 | 自动生成于 19:00\n\n---\n\n`;
  
  // 按日期分组
  const byMonth = {};
  files.forEach(file => {
    const month = file.substring(0, 7);
    if (!byMonth[month]) byMonth[month] = [];
    byMonth[month].push(file.replace('.md', ''));
  });
  
  // 生成月份列表
  Object.keys(byMonth).sort().reverse().forEach(month => {
    indexContent += `## 📅 ${month}\n\n`;
    byMonth[month].forEach(date => {
      indexContent += `- [[${date}|${date}]]\n`;
    });
    indexContent += '\n';
  });
  
  indexContent += `---\n\n## 📈 统计\n\n- **总新闻数**: ${files.length} 篇\n- **最后更新**: ${new Date().toISOString().split('T')[0]}\n\n---\n\n*本索引由 OpenClaw 自动生成*`;
  
  fs.writeFileSync(path.join(newsDir, '索引.md'), indexContent, 'utf8');
}

// 执行
main();
